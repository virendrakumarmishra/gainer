from enum import Enum

class ChannelStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    SUSPICIOUS = "suspicious"
    DEFAULTER = "defaulter"