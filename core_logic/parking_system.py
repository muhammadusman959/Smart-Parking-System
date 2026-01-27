import time
from core_logic.zone import Zone
from core_logic.allocation_engine import AllocationEngine
from core_logic.rollback_manager import RollbackManager
from core_logic.parking_request import ParkingRequest

class ParkingSystem:
    def __init__(self):
        self.zones = {}
        self.request_history = []
        self.allocation_engine = AllocationEngine(self.zones)
        self.rollback_manager = RollbackManager()
        
        # --- TIMER LOGIC ---
        self.active_timers = {} 
        self.completed_durations = [] 

    def add_zone(self, zone_id, name):
        new_zone = Zone(zone_id, name)
        new_zone.add_parking_area(1, 5)
        new_zone.add_parking_area(2, 5)
        new_zone.add_parking_area(3, 5)
        self.zones[zone_id] = new_zone

    def request_parking(self, vehicle_id, preferred_zone_id):
        req = ParkingRequest(vehicle_id, preferred_zone_id)
        success, slot = self.allocation_engine.allocate_slot(req)
        
        if success:
            self.rollback_manager.log_allocation(req, slot)
            # START TIMER
            self.active_timers[vehicle_id] = time.time()
        
        self.request_history.append(req)
        return success

    def release_parking(self, vehicle_id):
        for zone in self.zones.values():
            for area in zone.parking_areas:
                for slot in area.slots:
                    if slot.vehicle_id == vehicle_id:
                        slot.free_slot()
                        
                        # STOP TIMER & CALCULATE
                        if vehicle_id in self.active_timers:
                            start_time = self.active_timers.pop(vehicle_id)
                            duration_mins = (time.time() - start_time) / 60.0
                            self.completed_durations.append(duration_mins)
                        
                        return True
        return False

    def get_stats_counts(self):
        completed = sum(1 for r in self.request_history if r.state.name == 'COMPLETED')
        cancelled = sum(1 for r in self.request_history if r.state.name == 'CANCELLED')
        return {'completed': completed, 'cancelled': cancelled}

    def get_peak_zone(self):
        if not self.zones: return "N/A"
        return max(self.zones.values(), key=lambda z: z.calculate_utilization()).name

    def get_average_parking_duration(self):
        # IF EMPTY, RETURN 0.0 (The old code returned 15.5 here)
        if not self.completed_durations:
            return 0.0
        return sum(self.completed_durations) / len(self.completed_durations)