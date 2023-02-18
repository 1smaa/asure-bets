import urllib.parse
from packages.decorators import catch

API = "http://127.0.0.1:5000"


class Url(object):
    '''
    An object to represent an api url.
    '''

    def __init__(self, endpoint: str, params: dict, get: bool = True) -> None:
        if not isinstance(params, dict):
            try:
                params = dict(params)
            except:
                raise Exception("Parameters must be a dictionary.")
        self.base, self.endpoint, self.__params = API, endpoint, self.__build_params(
            params)
        print(params, self.__params)
        self.url = "{api}/{endpoint}{params}".format(
            api=self.base, endpoint=self.endpoint, params="?"+self.__params if get else "")

    @catch
    def __build_params(self, params: dict) -> str:
        '''
        Builds a parameter string for requests.
        '''
        return urllib.parse.urlencode(params)

    def get_data(self) -> bytes:
        '''
        Returns byte data for post requests.
        '''
        return self.__params.encode("ascii")
