from abc import ABCMeta, abstractmethod
from collections import defaultdict

import twitter_backend as tw

class Backend:

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, ref_list):
        pass

    @abstractmethod
    def store(self, data):
        pass

class NullBackend(Backend):

    """Backend that supports lookup by passing in the data you want to look up."""

    def get(self, ref_list):
        return "".join(ref_list)

    def store(self, data):
        return data

