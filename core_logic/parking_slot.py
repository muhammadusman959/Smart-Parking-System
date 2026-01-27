class ParkingSlot:
    def __init__(self, slot_id):
        self.slot_id = slot_id
        self.is_occupied = False
        self.vehicle_id = None

    def occupy_slot(self, vehicle_id):
        if not self.is_occupied:
            self.is_occupied = True
            self.vehicle_id = vehicle_id
            return True
        return False

    def free_slot(self):
        self.is_occupied = False
        self.vehicle_id = None