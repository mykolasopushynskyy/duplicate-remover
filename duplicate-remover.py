from controller.controller import ApplicationController
from configs import ConfigManager
from controller.duplicate_scanner import DuplicateScanner
from model.pubsub import PubSubBroker
from view.view import ApplicationView
from model.model import ApplicationModel


class App:
    def __init__(self):
        super().__init__()

        self.pubsub = PubSubBroker()
        self.config = ConfigManager(self.pubsub)
        self.model = ApplicationModel(self.pubsub)
        self.view = ApplicationView(self.pubsub)
        self.service = DuplicateScanner(self.model)
        self.controller = ApplicationController(self.pubsub, self.config, self.model, self.view, self.service)

    def start(self):
        self.view.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
