"""
This Agent is able to monitor the status of the services running in the Server.
"""
from notify.models import Chat
from parrot.scheduler import schedule, ScheduleType
from parrot.bots.agent import Agent
from parrot.registry import register_agent


@register_agent(name="devops_agent", at_startup=True)
class DevOps(Agent):
    """A simple minion agent."""
    agent_id: str = "devops_agent"
