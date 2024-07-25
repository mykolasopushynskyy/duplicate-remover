from controller.controller import ApplicationController
from configs import ConfigManager
from view.view import ApplicationView
from model.model import ApplicationModel


class App:
    def __init__(self):
        super().__init__()

        self.config = ConfigManager("Duplicate Remover")
        self.model = ApplicationModel()
        self.view = ApplicationView()
        self.controller = ApplicationController(self.config, self.model, self.view)

    def start(self):
        self.view.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
