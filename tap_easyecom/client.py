"""REST client handling, including EasyEcomStream base class."""
from urllib.parse import urlparse, parse_qs
from functools import cached_property
from singer_sdk.streams import RESTStream

from tap_easyecom.auth import BearerTokenAuthenticator

class EasyEcomStream(RESTStream):
    """EasyEcom stream class."""

    records_jsonpath = "$.data[*]"
    # limit is maxed out at 10 :/
    page_size = 10

    def get_next_page_token(
        self, response, previous_token
    ):
        """Return a token for identifying next page or None if no more pages."""
        res_json = response.json()
        next_url = res_json.get("nextUrl", res_json.get("data", {}).get("nextUrl"))
        if next_url:
            return parse_qs(urlparse(next_url).query)['cursor']

        return None

    @property
    def url_base(self) -> str:
        return "https://api.easyecom.io"

    @cached_property
    def authenticator(self) -> BearerTokenAuthenticator:
        return BearerTokenAuthenticator(
            self, self._tap.config, f"{self.url_base}/access/token"
        )

    @property
    def http_headers(self) -> dict:
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers


    def get_url_params(self,context,next_page_token):
        params: dict = {}
        if next_page_token:
            params["cursor"] = next_page_token
        if self.page_size:
            params["limit"] = self.page_size
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params
