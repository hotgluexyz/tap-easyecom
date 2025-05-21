"""EasyEcom tap class."""

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
import logging

from tap_easyecom.streams import (
    ProductsStream,
    ProductCompositionsStream,
    SuppliersStream,
    SellOrdersStream,
    BuyOrdersStream,
    ReceiptsStream,
    ReturnsStream,
)

STREAM_TYPES = [
     ProductsStream,
     ProductCompositionsStream,
     SuppliersStream,
    SellOrdersStream,
     BuyOrdersStream,
     ReceiptsStream,
     ReturnsStream,
]


class TapEasyEcom(Tap):
    """EasyEcom tap class."""

    name = "tap-easyecom"

    def __init__(
        self,
        config=None,
        catalog=None,
        state=None,
        parse_env_config=False,
        validate_config=True,
    ) -> None:
        super().__init__(config, catalog, state, parse_env_config, validate_config)
        self.config_file = config[0]
        self.logger.info("Initializing TapEasyEcom")

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property("start_date", th.DateTimeType,),
    ).to_dict()

    def discover_streams(self):
        """Return a list of discovered streams."""
        self.logger.info("Discovering streams")
        streams = [stream(self) for stream in STREAM_TYPES]
        self.logger.info(f"Discovered {len(streams)} streams: {[s.name for s in streams]}")
        return streams

    def sync_all(self):
        """Sync all streams."""
        self.logger.info("Starting sync of all streams")
        try:
            super().sync_all()
            self.logger.info("Successfully completed sync of all streams")
        except Exception as e:
            self.logger.error(f"Error during sync: {str(e)}")
            raise


if __name__ == "__main__":
    TapEasyEcom.cli()
