from enum import Enum

class CustomerStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class CampaignsStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "paused"
    COMPLETED = "completed"