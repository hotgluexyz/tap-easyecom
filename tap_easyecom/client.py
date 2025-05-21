"""REST client handling, including EasyEcomStream base class."""
from typing import Callable, Iterable
from singer_sdk.exceptions import RetriableAPIError
from urllib.parse import urlparse, parse_qs
from functools import cached_property
import singer
from singer import StateMessage
from singer_sdk.streams import RESTStream
import logging

from tap_easyecom.auth import BearerTokenAuthenticator
from pendulum import parse
import backoff
import requests

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
        next_url = res_json.get("nextUrl")

        if not next_url and isinstance(res_json.get("data", {}), dict):
            next_url = res_json.get("data", {}).get("nextUrl")

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

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date

    def get_url_params(self,context,next_page_token):
        params: dict = {}
        if next_page_token:
            params["cursor"] = next_page_token
        if self.page_size:
            params["limit"] = self.page_size
        if hasattr(self, "additional_params"):
            params.update(self.additional_params)
        if self.replication_key:
            start_date = self.get_starting_time(context)
            date_filter = self.date_filter_param if hasattr(self, "date_filter_param") else "updated_after"
            params[date_filter] = start_date.strftime('%Y-%m-%d %H:%M:%S')
        
        self.logger.info(f"Request parameters for {self.name}: {params}")
        return params

    def _write_state_message(self) -> None:
        """Write out a STATE message with the latest state."""
        tap_state = self.tap_state

        if tap_state and tap_state.get("bookmarks"):
            for stream_name in tap_state.get("bookmarks").keys():
                if stream_name in [
                    "gl_entries_dimensions",
                ] and tap_state["bookmarks"][stream_name].get("partitions"):
                    tap_state["bookmarks"][stream_name] = {"partitions": []}

        singer.write_message(StateMessage(value=tap_state))
        self.logger.info(f"State message written for {self.name}")

    def request_decorator(self, func: Callable) -> Callable:
        decorator: Callable = backoff.on_exception(
            self.backoff_wait_generator,
            (
                RetriableAPIError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
            ),
            max_tries=10,
            on_backoff=self.backoff_handler,
        )(func)
        return decorator
    
    def parse_response(self, response) -> Iterable[dict]:
        try:
            if response.json().get("data") == "No Data Found":
                self.logger.info(f"No data found in response for {self.name}")
                yield from []
            else:
                self.logger.info(f"Parsing response for {self.name} with status code {response.status_code}")
                yield from super().parse_response(response)
        except Exception as e:
            self.logger.error(f"Error parsing response for {self.name}: {str(e)}")
            self.logger.error(f"Response content: {response.text}")
            raise

    def prepare_request(self, context, next_page_token):
        """Prepare the request object."""
        try:
            request = super().prepare_request(context, next_page_token)
            self.logger.info(f"Prepared request for {self.name} to URL: {request.url}")
            return request
        except Exception as e:
            self.logger.error(f"Error preparing request for {self.name}: {str(e)}")
            raise

    def backoff_handler(self, details):
        """Handle backoff retry."""
        self.logger.warning(
            f"Backing off {details['wait']} seconds after {details['tries']} tries "
            f"calling {details['target'].__name__} due to {details['exception']}"
        )