from model.pubsub import PubSubBroker, Topic


class ApplicationModel:
    def __init__(self, pubsub: PubSubBroker):
        super().__init__()
        self.pubsub = pubsub

        # model data
        self.merge_folder = ""
        self.folders_to_scan = {}

        # subscribe for config change
        self.pubsub.subscribe(Topic.MODEL_LOAD, self.from_configs)

    def from_configs(self, configs):
        self.merge_folder = configs["merge_folder"]
        self.folders_to_scan = configs["folders_to_scan"]

    def to_configs(self):
        return dict(
            merge_folder=self.merge_folder,
            folders_to_scan=self.folders_to_scan
        )

    def set_merge_folder(self, path):
        self.merge_folder = path

    def add_folder_to_scan(self, record: dict):
        self.folders_to_scan[record.get("path")] = record

    def remove_folder_to_scan(self, path):
        self.folders_to_scan.pop(path)
