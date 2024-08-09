class FolderDTO:
    def __init__(self, **kwargs):
        self.path = kwargs.get("path")
        self.size = kwargs.get("size")
        self.date = kwargs.get("date")
        self.exclude = kwargs.get("exclude")

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(**dict_obj)
