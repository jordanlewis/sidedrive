from collections import defaultdict

class Backend(object):

    @abstractmethod
    def get(self, name, pw, ref_list):
        raise Exception

    @abstractmethod
    def store(self, name, pw, data):
        raise Exception

class NullBackend(Backend):

    """Backend that supports lookup by passing in the data you want to look up."""

    def get(self, name, pw, ref_list):
        return "".join(ref_list)

    def store(self, name, pw, data):
        pass
