class ParkingSlot:
    def __init__(self, slot_id: int, zone_id: int):
        """
        Represents a single parking slot.
        Ref: [cite: 28]
        """
        self.slot_id = slot_id
        self.zone_id = zone_id
        self.is_available = True  # Ref: [cite: 31]
        self.vehicle_id = None    # Tracks which car is here

    def occupy(self, vehicle_id: str):
        """Mark slot as occupied."""
        if self.is_available:
            self.is_available = False
            self.vehicle_id = vehicle_id
            return True
        return False

    def free(self):
        """Mark slot as free."""
        self.is_available = True
        self.vehicle_id = None

    def __repr__(self):
        status = "Free" if self.is_available else f"Occupied by {self.vehicle_id}"
        return f"<Slot {self.slot_id} (Zone {self.zone_id}): {status}>"