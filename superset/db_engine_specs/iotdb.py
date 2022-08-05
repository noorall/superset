from datetime import datetime
from typing import Optional, TYPE_CHECKING, Dict, Any

from superset.db_engine_specs.base import BaseEngineSpec
from superset.utils import core as utils

if TYPE_CHECKING:
    from superset.connectors.sqla.models import TableColumn


class CrateEngineSpec(BaseEngineSpec):
    engine = "iotdb"
    engine_name = "Apache IoTDB"

    allows_hidden_ordeby_agg = False
    allows_joins = False

    @classmethod
    def alter_new_orm_column(cls, orm_col: "TableColumn") -> None:
        if orm_col.column_name == "Time":
            orm_col.python_date_format = "epoch_ms"
            orm_col.is_dttm = True

    @classmethod
    def convert_dttm(
        cls, target_type: str, dttm: datetime, db_extra: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        tt = target_type.upper()
        if tt == utils.TemporalType.TIMESTAMP:
            return f"{dttm.timestamp() * 1000}"
        return None

    @classmethod
    def epoch_to_dttm(cls) -> str:
        return "{col} * 1000"

    @classmethod
    def epoch_ms_to_dttm(cls) -> str:
        return "{col}"
