"""freshbooks Authentication."""
from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase
from typing import Optional
from datetime import datetime
import requests
import json


class BearerTokenAuthenticator(APIAuthenticatorBase):
    """API Authenticator for OAuth 2.0 flows."""

    def __init__(
        self,
        stream: RESTStreamBase,
        config_file: Optional[str] = None,
        auth_endpoint: Optional[str] = None,
    ) -> None:
        super().__init__(stream=stream)
        self._auth_endpoint = auth_endpoint
        self._config_file = config_file
        self._tap = stream._tap
        self.expires_in = self._tap.config.get("expires_in", 0)

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied.

        These will be merged with any `http_headers` specified in the stream.

        Returns:
            HTTP headers for authentication.
        """
        if not self.is_token_valid():
            self.update_access_token()
        result = super().auth_headers
        result[
            "Authorization"
        ] = f"Bearer {self._tap._config.get('access_token')}"
        return result

    @property
    def auth_endpoint(self) -> str:
        """Get the authorization endpoint.

        Returns:
            The API authorization endpoint if it is set.

        Raises:
            ValueError: If the endpoint is not set.
        """
        if not self._auth_endpoint:
            raise ValueError("Authorization endpoint not set.")
        return self._auth_endpoint

    @property
    def request_body(self) -> dict:
        """Define the OAuth request body for the API."""
        return {
            "email": self.config.get("email"),
            "password": self.config.get("password"),
            "location_key": self.config.get("location_key"),
        }

    def is_token_valid(self) -> bool:
        now = round(datetime.utcnow().timestamp())
        created_at = self._tap._config.get(
            "created_at", 0
        )

        return now < (created_at + self.expires_in - 60)

    # Authentication and refresh
    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        auth_request_payload = self.request_body
        token_response = requests.post(self.auth_endpoint, data=auth_request_payload)
        try:
            token_last_refreshed = round(datetime.utcnow().timestamp())
            token_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
            token_json = token_response.json()
            token = token_json["data"]["token"]
        except Exception as ex:
            raise RuntimeError(
                f"Failed login, response was '{token_response.json()}'. {ex}"
            )
        self.access_token = token["jwt_token"]
        self.expires_in = token["expires_in"]

        self._tap._config["created_at"] = token_last_refreshed
        self._tap._config["access_token"] = self.access_token
        self._tap._config["expires_in"] = self.expires_in
        with open(self._tap.config_file, "w") as outfile:
            json.dump(self._tap._config, outfile, indent=4)
