from microsoft_agents.hosting.core import AgentAuthConfiguration

from teams_agent.app import AGENT_APP
from teams_agent.start_server import start_server

if __name__ == "__main__":
    auth_config = AgentAuthConfiguration(anonymous_allowed=True)
    start_server(AGENT_APP, auth_config)
