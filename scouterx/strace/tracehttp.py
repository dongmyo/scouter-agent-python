import requests
from contextlib import ContextDecorator


class StartApiCall(ContextDecorator):
    def __init__(self, host, url):
        self.host = host
        self.url = url

    def __enter__(self):
        print(f"Starting API call to {self.host} {self.url}")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value:
            print(f"API call to {self.host} failed with error: {exc_value}")
        else:
            print(f"API call to {self.host} completed successfully")


class ScouterSession(requests.Session):
    def __init__(self, proxied_session=None):
        super().__init__()
        self.proxied = proxied_session or requests.Session()

    def send(self, request, **kwargs):
        with StartApiCall(request.host, request.url):
            response = self.proxied.send(request, **kwargs)
        return response

    def request(self, method, url, **kwargs):
        req = requests.Request(method, url, **kwargs)
        prepared_req = self.prepare_request(req)
        prepared_req.host = url.split('://')[1].split('/')[0]
        return self.send(prepared_req)
