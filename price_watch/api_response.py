from typing import Dict, Optional

import requests


class APIResponse:
    def __init__(self, protocol: str, hostname: str):
        self.protocol = protocol
        self.hostname = hostname

    def _url_constructor(self, pathname: str) -> str:
        return self.protocol + "://" + self.hostname + "/" + pathname

    def make_request(
        self, path_name: str, query_params: Optional[Dict[str, str]] = None
    ) -> None:
        url = self._url_constructor(path_name)
        self.r = requests.get(url=url, params=query_params)

    @property
    def status_code(self) -> int:
        return self.r.status_code

    @property
    def reason(self) -> str:
        return self.r.reason

    @property
    def url(self) -> Optional[str]:
        return self.r.request.url

    @property
    def text(self) -> Optional[str]:
        return self.r.text
