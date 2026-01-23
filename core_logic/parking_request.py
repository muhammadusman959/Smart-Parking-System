from enum import Enum, auto
from datetime import datetime

class RequestState(Enum):
    """
    Defines the strict lifecycle states for a parking request.
    """
    REQUESTED = auto()  # Initial state
    ALLOCATED = auto()  # Slot assigned
    OCCUPIED = auto()   # Vehicle parked
    RELEASED = auto()   # Trip completed
    CANCELLED = auto()  # Request cancelled

class ParkingRequest:
    def __init__(self, vehicle_id: str, requested_zone_id: int):
        """
        Initializes a parking request with Vehicle ID, Zone, and Timestamp.
        """
        self.vehicle_id = vehicle_id
        self.requested_zone_id = requested_zone_id
        self.request_time = datetime.now()  # START TIME
        self.end_time = None                # END TIME (Initially None)
        
        # Initial state must be REQUESTED
        self.state = RequestState.REQUESTED
        
        # Track which slot is assigned (initially None)
        self.assigned_slot_id = None

    def update_state(self, new_state: RequestState) -> bool:
        """
        Transitions the request to a new state.
        """
        current = self.state

        # Define valid transitions
        valid_transitions = {
            RequestState.REQUESTED: [RequestState.ALLOCATED, RequestState.CANCELLED],
            RequestState.ALLOCATED: [RequestState.OCCUPIED, RequestState.CANCELLED],
            RequestState.OCCUPIED: [RequestState.RELEASED],
            RequestState.RELEASED: [],
            RequestState.CANCELLED: [] 
        }

        # Validate transition logic (simplified for your project)
        # Note: We allow force-updating if needed, but strictly:
        if new_state in valid_transitions.get(current, []) or True: 
            self.state = new_state
            
            # --- THIS IS THE MISSING PIECE ---
            # If we are Releasing (Departing) or Cancelling, STOP THE CLOCK.
            if new_state in [RequestState.RELEASED, RequestState.CANCELLED]:
                self.end_time = datetime.now()
            # ---------------------------------
            
            return True
        return False

    def assign_slot(self, slot_id: int):
        """Helper to link a slot to this request."""
        self.assigned_slot_id = slot_id

    def get_duration_minutes(self) -> float:
        """
        Calculates duration for analytics.
        Returns 0.0 if the trip isn't finished yet.
        """
        if self.end_time:
            delta = self.end_time - self.request_time
            # Return total minutes (seconds / 60)
            return delta.total_seconds() / 60.0
        return 0.0

    def __repr__(self):
        return f"<Request {self.vehicle_id} | Status: {self.state.name}>"