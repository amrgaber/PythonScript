from abc import ABC, abstractmethod

class BaseURL(ABC):
    def __init__(self, url):
        self._url = url

    @property
    def url(self):
        return self._url

    @property
    def category(self):
        raise NotImplementedError

class BuyURL(BaseURL):

    @property
    def category(self):
        return 'buy'

class RentURL(BaseURL):

    @property
    def category(self):
        return 'rent'

class CommercialRentURL(BaseURL):

    @property
    def category(self):
        return 'commercial-rent'
