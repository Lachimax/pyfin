import utils as u

class Generic():
    params = {
        "name": None
    }
    def __init__(
            self,
            path: str,
            **kwargs
        ):
        self.path: str = None
        for key, item in self.params.items():
            setattr(self, key, item)
        for key, item in kwargs.items():
            setattr(self, key, item)


    def to_file(self):
        u.write_yaml(self.__dict__.copy())

    @classmethod
    def from_file(cls, file: str):
        params = u.read_yaml(file=file)
        return cls(**params)
    
    @classmethod
    def template_yaml(cls, path: str):
        u.write_yaml(path, cls.params)