"""freshbooks Authentication."""
from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase
from typing import Optional
from datetime import datetime
import requests
import json
import logging


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
        self.logger = logging.getLogger(__name__)

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied.

        These will be merged with any `http_headers` specified in the stream.

        Returns:
            HTTP headers for authentication.
        """
        if not self.is_token_valid():
            self.logger.info("Token expired or invalid, updating access token")
            self.update_access_token()
        else:
            self.logger.debug("Using existing valid token")
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

    def update_access_token(self) -> None:
        """Update the access token."""
        try:
            self.logger.info("Attempting to update access token")
            response = requests.post(
                self.auth_endpoint,
                json=self.request_body,
            )
            response.raise_for_status()
            token_data = response.json()
            
            # Extract token from nested structure
            if not token_data.get("data", {}).get("token", {}).get("jwt_token"):
                self.logger.error(f"Invalid token response: {token_data}")
                raise ValueError("No access token in response")
                
            self._tap._config["access_token"] = token_data["data"]["token"]["jwt_token"]
            self._tap._config["expires_in"] = token_data["data"]["token"].get("expires_in", 3600)
            self._tap._config["token_created_at"] = datetime.now().timestamp()
            self.logger.info("Successfully updated access token")
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to update access token: {str(e)}")
            if hasattr(e.response, 'text'):
                self.logger.error(f"Response content: {e.response.text}")
            raise

    def is_token_valid(self) -> bool:
        """Check if the current token is valid."""
        if not self._tap._config.get("access_token"):
            self.logger.debug("No access token found")
            return False
            
        if not self._tap._config.get("expires_in"):
            self.logger.debug("No expiration time found for token")
            return False
            
        # Add some buffer time (5 minutes) before actual expiration
        expires_at = self._tap._config.get("token_created_at", 0) + self._tap._config.get("expires_in", 0) - 300
        is_valid = datetime.now().timestamp() < expires_at
        
        if not is_valid:
            self.logger.debug("Token has expired")
        return is_valid
