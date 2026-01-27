# CORRECTED IMPORT
from core_logic.parking_area import ParkingArea

class Zone:
    def __init__(self, zone_id, name):
        self.zone_id = zone_id
        self.name = name
        self.parking_areas = []

    def add_parking_area(self, area_id, capacity):
        area = ParkingArea(area_id, capacity)
        self.parking_areas.append(area)

    def calculate_utilization(self):
        total_slots = 0
        occupied_slots = 0
        for area in self.parking_areas:
            for slot in area.slots:
                total_slots += 1
                if slot.is_occupied:
                    occupied_slots += 1
        
        if total_slots == 0: return 0.0
        return (occupied_slots / total_slots) * 100