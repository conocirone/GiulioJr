class Agent:
    def __init__(self, gateway, timeout, color):
        self.gateway = gateway
        self.gateway.set_agent(self)
        self.color = color

        # while True:
        self.gateway.get_state()
