"""EasyEcom tap class."""

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

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

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property("start_date", th.DateTimeType,),
    ).to_dict()

    def discover_streams(self):
        return [stream(self) for stream in STREAM_TYPES]


if __name__ == "__main__":
    TapEasyEcom.cli()
