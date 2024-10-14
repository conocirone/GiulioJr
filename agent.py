class Agent:
    def __init__(self, gateway):
        self.gateway = gateway
        self.gateway.set_agent(self)

        while True:
            self.gateway.get_state()
