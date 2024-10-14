from gateway import Gateway
from agent import Agent

team = "WHITE"
name = "boh"
timeout = 60
ip = "localhost"

gateway = Gateway(team, name, timeout, ip)
agent = Agent(gateway)
gateway.set_agent(agent)
