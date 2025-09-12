import utils as u

class Generic():
    def __init__(
            self,
            **kwargs
        ):
        for key, item in kwargs.items():
            setattr(self, key, item)

    @classmethod
    def from_file(cls, file: str):
        params = u.read_yaml(file=file)
        return cls(**params)