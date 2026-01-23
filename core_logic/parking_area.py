from parking_slot import ParkingSlot

class ParkingArea:
    def __init__(self, area_id: int, zone_id: int, capacity: int):
        """
        A specific area within a zone containing multiple slots.
        Ref: [cite: 22-23]
        """
        self.area_id = area_id
        self.zone_id = zone_id
        self.slots = [] # List to hold ParkingSlot objects

        # Initialize slots for this area
        # We generate unique Slot IDs like '101', '102' based on Area ID
        start_id = area_id * 100
        for i in range(capacity):
            self.slots.append(ParkingSlot(start_id + i, zone_id))

    def get_available_slots(self):
        """Returns a list of all free slots in this area."""
        # Simple list filtering (Source requirement: Array/List usage)
        return [slot for slot in self.slots if slot.is_available]

    def __repr__(self):
        return f"<Area {self.area_id} | Total Slots: {len(self.slots)}>"