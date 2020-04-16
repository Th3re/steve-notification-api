import os


class EnvClass:
    def get(self, name: str) -> str:
        env_name = f'{self.__class__.__name__.upper()}_{name.upper()}'
        return os.environ[env_name]


class Google(EnvClass):
    def __init__(self):
        super()
        self.apikey_fcm = self.get('apikey_fcm')


class Environment(EnvClass):
    def __init__(self):
        self.google = Google()


def read_environment() -> Environment:
    return Environment()
