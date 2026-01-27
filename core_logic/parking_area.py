# CORRECTED IMPORT: Must include 'core_logic.'
from core_logic.parking_slot import ParkingSlot

class ParkingArea:
    def __init__(self, area_id, capacity):
        self.area_id = area_id
        self.capacity = capacity
        self.slots = []
        self._initialize_slots()

    def _initialize_slots(self):
        # Create slots with IDs based on area (e.g., 101, 102...)
        start_id = self.area_id * 100
        for i in range(self.capacity):
            self.slots.append(ParkingSlot(start_id + i + 1))