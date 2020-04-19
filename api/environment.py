from api.libs.representation.pretty import PrettyPrint
from api.libs.environment.environmentreader import EnvironmentReader


class Google(EnvironmentReader):
    def __init__(self):
        super()
        self.apikey_fcm = self.get('apikey_fcm')


class Environment(PrettyPrint):
    def __init__(self):
        self.google = Google()

    @staticmethod
    def read():
        return Environment()
