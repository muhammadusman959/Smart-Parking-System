class Vehicle:
    def __init__(self, vehicle_id: str, preferred_zone_id: int):
        """
        Represents a vehicle requesting parking.
        [cite_start]Ref: [cite: 33-35]
        """
        self.vehicle_id = vehicle_id
        self.preferred_zone_id = preferred_zone_id

    def __repr__(self):
        return f"<Vehicle {self.vehicle_id} | Pref: {self.preferred_zone_id}>"