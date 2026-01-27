from enum import Enum, auto

class RequestState(Enum):
    REQUESTED = auto()
    ALLOCATED = auto()
    COMPLETED = auto()
    CANCELLED = auto()

class ParkingRequest:
    def __init__(self, vehicle_id, preferred_zone_id):
        self.vehicle_id = vehicle_id
        self.preferred_zone_id = preferred_zone_id
        self.state = RequestState.REQUESTED
        self.allocated_slot_id = None

    def update_state(self, new_state):
        self.state = new_state

    def allocate(self, slot_id):
        self.allocated_slot_id = slot_id
        self.update_state(RequestState.ALLOCATED)

    def complete(self):
        self.update_state(RequestState.COMPLETED)