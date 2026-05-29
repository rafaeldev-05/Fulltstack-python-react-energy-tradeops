from enum import Enum


class OperationType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class TradeStatus(str, Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    IN_TRANSIT = "IN_TRANSIT"
    SETTLED = "SETTLED"
    CANCELLED = "CANCELLED"


class TransportMode(str, Enum):
    SHIP = "SHIP"
    PIPELINE = "PIPELINE"
    TRUCK = "TRUCK"
    RAIL = "RAIL"


class ShipmentStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_TRANSIT = "IN_TRANSIT"
    DELAYED = "DELAYED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
