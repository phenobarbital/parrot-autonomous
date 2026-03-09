# AI-Parrot Autonomous Server

This repository provides the setup to run AI-Parrot agents as **autonomous services**. Unlike the A2A server (which exposes agents over HTTP for agent-to-agent communication), the autonomous server launches agents that **listen on messaging platforms** (Telegram, Slack, WhatsApp, MS Teams) and **execute scheduled operations** via a built-in scheduler.

## Installation & Environment Setup

Follow these steps to set up the environment using `uv`:

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Create a virtual environment**:
   ```bash
   uv venv --python 3.11 .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   Run `uv sync` to install the required packages from `pyproject.toml`.
   ```bash
   uv sync
   ```

4. **Prepare the project structure**:
   Create the required configuration and environment folders:
   ```bash
   # Create the environment directory
   mkdir env

   # Initialize NavConfig project structure
   kardex create

   # Create empty environment file
   touch env/.env

   # Create a folder for templates
   mkdir templates/
   ```

## Architecture Overview

The autonomous server is built on top of `navigator-api` (an `aiohttp`-based framework) and integrates the following core components:

- **BotManager**: Manages chatbot instances across messaging platforms (Telegram, Slack, WhatsApp, MS Teams). Each bot connects to a configured agent and listens for user messages.
- **AgentSchedulerManager**: Schedules and executes agent tasks on a recurring or cron-based basis, enabling autonomous operations without user prompts.
- **BackgroundQueue**: Handles background task execution with configurable worker pools.
- **Redis RQ / Job Manager**: Manages long-running or deferred jobs via Redis queues.
- **AuthHandler**: Provides authentication for both the web API and messaging platform users.

## Configuring Your Autonomous Agent

### 1. Define the Bot Integration

Create or edit `env/integrations_bots.yaml` to configure your messaging platform bot:

```yaml
agents:
  OperationsBot:
    chatbot_id: devops_agent
    kind: telegram
    welcome_message: "Hello! I'm your Operations Assistant."
    bot_token: YOUR_TELEGRAM_BOT_TOKEN
    enable_group_mentions: true
    enable_group_commands: true
    reply_in_thread: true
    enable_channel_posts: false
    # Authentication settings
    auth_url: https://your-api.example.com/api/v1/login
    login_page_url: https://your-api.example.com/static/telegram/login.html
    enable_login: true
    force_authentication: true
```

Supported `kind` values: `telegram`, `slack`, `whatsapp`, `msteams`.

### 2. Define the Agent

Place your agent definitions in the `agents/` directory. Each agent is a Python module that defines its role, goal, language model, and tools:

```python
from parrot.bots import Agent

agent = Agent(
    name="OperationsAgent",
    llm="anthropic:claude-sonnet-4-20250514",
    tools=[YourCustomTool(), AnotherTool()]
)
```

### 3. Application Entrypoint

The `app.py` file defines the main `AppHandler` that wires everything together:

```python
from app import Main
from navigator import Application

app = Application(Main, enable_jinja2=True)
app.add_websockets()

if __name__ == '__main__':
    app.run()
```

## Running the Server

### Development

```bash
source .venv/bin/activate
python run.py
```

### Production with Gunicorn

For production deployments, use `gunicorn` with the provided configuration:

```bash
source .venv/bin/activate
gunicorn nav:navigator -c gunicorn_config.py
```

The `gunicorn_config.py` is pre-configured to use the `aiohttp.worker.GunicornUVLoopWebWorker` worker class with automatic worker scaling based on available CPU cores.

### Running with Supervisor and Systemd

To ensure the application runs continuously in the background and restarts automatically via SystemD's standard process management, you can configure it with `supervisor`.

1. Generate and install the supervisord configuration file:
   ```bash
   # From your project root
   python scripts/setup_supervisord.py --user your_linux_user --reload
   ```
2. The script will dynamically generate `parrot-autonomous.conf` in `/etc/supervisor/conf.d/` and reload the supervisor daemon to start the app.
3. You can monitor or restart the service using `supervisorctl`:
   ```bash
   sudo supervisorctl status parrot-autonomous
   sudo supervisorctl restart parrot-autonomous
   ```

*(See [docs/supervisord.md](docs/supervisord.md) for detailed configuration options.)*

## How It Works


```
┌─────────────────────────────────────────────────┐
│              Parrot Autonomous Server           │
│                                                 │
│  ┌─────────────┐    ┌──────────────────────┐    │
│  │ BotManager  │───▸│   Agent (LLM+Tools)  │    │
│  │ (Telegram,  │    └──────────────────────┘    │
│  │  Slack, etc)│              ▲                  │
│  └─────────────┘              │                  │
│                               │                  │
│  ┌─────────────────┐         │                  │
│  │ Scheduler        │────────┘                  │
│  │ (Cron / Interval)│                           │
│  └─────────────────┘                            │
│                                                 │
│  ┌─────────────────┐  ┌──────────────────┐      │
│  │ BackgroundQueue  │  │  Redis RQ / Jobs │      │
│  └─────────────────┘  └──────────────────┘      │
└─────────────────────────────────────────────────┘
```

1. **User sends a message** via Telegram (or other platform) → `BotManager` receives it → routes to the configured `Agent` → Agent processes with LLM + Tools → response sent back to the user.
2. **Scheduler triggers a task** on a cron/interval basis → Agent executes the operation autonomously → results are optionally reported via the messaging bot.
3. **Long-running jobs** are queued via Redis RQ and executed by background workers.

## Security

- **Bot Authentication**: Users can be required to authenticate before interacting with the bot (`force_authentication: true`).
- **Auth System**: The `AuthHandler` integrates with Navigator's authentication middleware for API-level security.
- **Token Management**: Bot tokens and API keys should be stored in `env/.env` and never committed to version control.

## 🤝 Community & Support

*   **Issues**: [GitHub Tracker](https://github.com/phenobarbital/parrot-autonomous/issues)
*   **Discussion**: [GitHub Discussions](https://github.com/phenobarbital/parrot-autonomous/discussions)
*   **Contribution**: Pull requests are welcome! Please read `CONTRIBUTING.md`.

---
*Built with ❤️ by the AI-Parrot Team*
