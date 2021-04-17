from typing import Dict, Optional

import requests


def url_constructor(protocol: str, hostname: str, pathname: str) -> str:
    return protocol + "://" + hostname + "/" + pathname


class APIResponse:
    def __init__(self, url: str, query_parameters: Dict[str, str] = None):
        self.r = requests.get(url=url, params=query_parameters)

    def get_status_code(self) -> int:
        return self.r.status_code

    def get_url(self) -> Optional[str]:
        return self.r.request.url

    def get_text(self) -> str:
        return self.r.text
