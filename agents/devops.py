"""
This Agent is able to monitor the status of the services running in the Server.
"""
from notify.models import Chat
from parrot.bots.agent import Agent
# Supported Tools:
from parrot.tools.system_health import SystemHealthTool
from parrot.tools.docker import DockerToolkit
from parrot.tools.shell_tool import ShellTool
from parrot.tools.pulumi import PulumiToolkit
from parrot.tools.sandboxtool import SandboxTool
# Registry
from parrot.registry import register_agent
# Scheduler:
from parrot.scheduler import schedule, ScheduleType


@register_agent(name="devops_agent", at_startup=True)
class DevOps(Agent):
    """A simple minion agent."""
    agent_id: str = "devops_agent"

    def agent_tools(self):
        """Return the agent-specific tools."""
        pulumi = PulumiToolkit()
        dkr = DockerToolkit()
        return [
            SystemHealthTool(),
            ShellTool(),
            SandboxTool()
        ] + pulumi.get_tools() + dkr.get_tools()
