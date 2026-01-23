from parking_area import ParkingArea

class Zone:
    def __init__(self, zone_id: int, name: str):
        """
        Represents a city zone / sector.
        Ref: [cite: 21]
        """
        self.zone_id = zone_id
        self.name = name
        self.parking_areas = []  # List of ParkingArea objects [cite: 22]
        self.adjacent_zone_ids = [] # Custom adjacency structure 

    def add_parking_area(self, area_id: int, capacity: int):
        """Adds a new parking area to this zone."""
        new_area = ParkingArea(area_id, self.zone_id, capacity)
        self.parking_areas.append(new_area)

    def add_neighbor(self, neighbor_zone_id: int):
        """
        Defines a logical connection to another zone.
        Ref: [cite: 24-25]
        """
        if neighbor_zone_id not in self.adjacent_zone_ids:
            self.adjacent_zone_ids.append(neighbor_zone_id)

    def find_first_available_slot(self):
        """
        Scans all areas in this zone for the first available slot.
        Ref: 
        """
        for area in self.parking_areas:
            available_slots = area.get_available_slots()
            if available_slots:
                return available_slots[0] # Return the first found slot
        return None

    def calculate_utilization(self):
        """
        Helper for analytics: Calculates % occupied.
        Ref: [cite: 75]
        """
        total_slots = 0
        occupied_slots = 0
        
        for area in self.parking_areas:
            for slot in area.slots:
                total_slots += 1
                if not slot.is_available:
                    occupied_slots += 1
        
        if total_slots == 0:
            return 0.0
        return (occupied_slots / total_slots) * 100

    def __repr__(self):
        return f"<Zone {self.zone_id} ({self.name}) | Neighbors: {self.adjacent_zone_ids}>"