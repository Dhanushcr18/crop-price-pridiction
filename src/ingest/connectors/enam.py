"""ENAMConnector: National Agriculture Market (e-NAM) connector with strict policy gating."""

import logging
from typing import List, Optional
from src.ingest.base import BaseConnector, RawPayload, ParsedRow, PolicyBlockedError

logger = logging.getLogger("farmer_advisor.ingest.enam")


class ENAMConnector(BaseConnector):
    """Connector for e-NAM public price board.
    
    STRICT POLICY GATING:
    Automated access to e-NAM is prohibited without written API authorization from SFAC.
    This connector enforces policy gating and always refuses unauthorized automated crawling.
    """

    def fetch(
        self, start_date: str, end_date: str, last_stored_date: Optional[str] = None
    ) -> List[RawPayload]:
        """Strictly enforces policy check and raises PolicyBlockedError."""
        # This will raise PolicyBlockedError because enabled=False and robots_allowed=False
        self.check_policy()
        raise PolicyBlockedError(
            f"Automated access to e-NAM is forbidden by portal policy. "
            f"Use official API credentials or disable this connector."
        )

    def parse(self, payload: RawPayload) -> List[ParsedRow]:
        """Not reachable unless policy clearance is granted."""
        raise NotImplementedError("Parsing disallowed without authorized payload.")
