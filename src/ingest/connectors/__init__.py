"""Connector registry and factory for all data sources."""

from typing import Dict, Any, Type, Optional
from src.ingest.base import BaseConnector
from src.ingest.connectors.data_gov import DataGovConnector
from src.ingest.connectors.agmarknet import AgmarknetConnector
from src.ingest.connectors.raita_mitra import RaitaMitraConnector
from src.ingest.connectors.enam import ENAMConnector
from src.ingest.connectors.open_meteo import OpenMeteoConnector
from src.ingest.connectors.ppac_diesel import PPACDieselConnector
from src.ingest.connectors.user_download import UserDownloadConnector, UserDownloadImporter
from src.ingest.connectors.ksamb_pdf import KsambPdfImporter, ParsedPdfRow, DateGateError, CompletenessError

CONNECTOR_MAP: Dict[str, Type[BaseConnector]] = {
    "data_gov_in": DataGovConnector,
    "agmarknet_portal": AgmarknetConnector,
    "raita_mitra_karnataka": RaitaMitraConnector,
    "enam_portal": ENAMConnector,
    "weather_open_meteo": OpenMeteoConnector,
    "weather_nasa_power": OpenMeteoConnector,
    "diesel_ppac": PPACDieselConnector,
    "user_download": UserDownloadConnector,
}


def get_connector(source_config: Dict[str, Any], global_config: Optional[Dict[str, Any]] = None) -> BaseConnector:
    """Instantiates appropriate connector class based on source ID."""
    source_id = source_config["id"]
    cls = CONNECTOR_MAP.get(source_id)
    if not cls:
        raise ValueError(f"No connector registered for source '{source_id}'")
    return cls(source_config, global_config)
