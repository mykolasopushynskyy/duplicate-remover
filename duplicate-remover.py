from controller.controller import ApplicationController
from configs import ConfigManager
from controller.duplicate_scanner import DuplicateScanner
from model import events
from model.pubsub import PubSubBroker
from view.view import ApplicationView
from model.model import ApplicationModel


class DuplicateRemover:
    def __init__(self):
        super().__init__()

        self.pubsub = PubSubBroker()
        self.config = ConfigManager(self.pubsub)
        self.model = ApplicationModel(self.pubsub)
        self.view = ApplicationView(self.pubsub)
        self.service = DuplicateScanner(self.model, self.pubsub)
        self.controller = ApplicationController(
            self.pubsub, self.model, self.view, self.service
        )

    def load_application_state(self):
        # publish data from settings
        self.pubsub.publish(
            events.MODEL_LOAD,
            dict(
                merge_folder=self.config.get("merge_folder", default=""),
                folders_to_scan=self.config.get("folders_to_scan", default={}),
            ),
        )
        self.pubsub.publish(
            events.MERGE_FOLDER_CHANGED, self.config.get("merge_folder", default="")
        )
        self.pubsub.publish(
            events.FOLDERS_TO_SCAN_CHANGED,
            self.config.get("folders_to_scan", default={}),
        )

    def start(self):
        self.load_application_state()
        self.view.mainloop()


if __name__ == "__main__":
    duplicate_remover = DuplicateRemover()
    duplicate_remover.start()
