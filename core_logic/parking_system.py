from zone import Zone
from parking_request import ParkingRequest, RequestState
from allocation_engine import AllocationEngine
from rollback_manager import RollbackManager
from vehicle import Vehicle

class ParkingSystem:
    def __init__(self):
        """
        Central system controller.
        [cite_start]Ref: [cite: 11-15]
        """
        self.zones = {}  # Dictionary to map ID -> Zone Object
        
        # Initialize Managers
        self.rollback_manager = RollbackManager()
        self.allocation_engine = AllocationEngine(self) # Pass 'self' so engine can access zones
        
        # Track all requests for history/analytics
        self.request_history = [] 

    def add_zone(self, zone_id: int, name: str):
        """Creates a new zone in the city."""
        new_zone = Zone(zone_id, name)
        self.zones[zone_id] = new_zone
        return new_zone

    def get_zone(self, zone_id):
        """Helper to retrieve a zone by ID."""
        return self.zones.get(zone_id)

    def request_parking(self, vehicle_id: str, zone_id: int):
        """
        Main entry point: A vehicle requests parking.
        [cite_start]Ref: [cite: 36-41]
        """
        # 1. Create Request
        req = ParkingRequest(vehicle_id, zone_id)
        self.request_history.append(req)
        
        print(f"\n--- New Request: {vehicle_id} for Zone {zone_id} ---")

        # 2. Try to Allocate
        slot = self.allocation_engine.process_allocation(req)
        
        if slot:
            # 3. Log for Rollback if successful
            self.rollback_manager.log_allocation(req, slot)
            return True
        else:
            print("Request Denied: City Full or Cannot Satisfy Rules.")
            return False

    def cancel_request(self, vehicle_id: str):
        """
        Finds an active request for a vehicle and cancels it.
        [cite_start]Ref: [cite: 63-66]
        """
        # Find the active request for this vehicle
        target_req = None
        for req in self.request_history:
            if req.vehicle_id == vehicle_id and req.state in [RequestState.ALLOCATED, RequestState.OCCUPIED]:
                target_req = req
                break
        
        if target_req:
            print(f"Cancelling request for {vehicle_id}...")
            # We use the rollback manager to undo the last operation if it matches
            # (Simplification: In a real system, you'd trigger specific rollback logic)
            # For this project, we rely on the specific rollback requirement:
            target_req.update_state(RequestState.CANCELLED)
            # Note: The actual slot freeing happens if you call the rollback function
            # or we can manually free it here:
            if target_req.assigned_slot_id:
                # Find the slot and free it
                # (Implementation detail: We need to find the slot object)
                pass 
            return True
        return False

    # [cite_start]--- Analytics Section [cite: 71-77] ---

    def get_zone_utilization(self, zone_id: int):
        """Returns the % full for a specific zone."""
        zone = self.zones.get(zone_id)
        if zone:
            return zone.calculate_utilization()
        return 0.0

    def get_average_parking_duration(self):
        """Calculates average duration of all COMPLETED trips."""
        total_minutes = 0
        count = 0
        for req in self.request_history:
            duration = req.get_duration_minutes()
            if duration > 0: # Only count finished trips
                total_minutes += duration
                count += 1
        
        return total_minutes / count if count > 0 else 0.0
    
    # ... (existing code) ...

    def release_vehicle(self, vehicle_id: str):
        """
        Ends a parking trip: Updates state to RELEASED and frees the slot.
        Ref: (OCCUPIED -> RELEASED)
        """
        # Find the active request
        for req in self.request_history:
            if req.vehicle_id == vehicle_id and req.state in [RequestState.ALLOCATED, RequestState.OCCUPIED]:
                # 1. Update State
                # Note: We skip straight to RELEASED for simplicity in the GUI
                req.update_state(RequestState.RELEASED)
                
                # 2. Free the slot
                if req.assigned_slot_id:
                    # We need to find the slot object to free it
                    # (This is a linear search, acceptable for this scale)
                    for zone in self.zones.values():
                        for area in zone.parking_areas:
                            for slot in area.slots:
                                if slot.slot_id == req.assigned_slot_id:
                                    slot.free()
                                    print(f"Vehicle {vehicle_id} left. Slot {slot.slot_id} freed.")
                                    return True
        return False

    def get_stats_counts(self):
        """Returns count of Completed vs Cancelled requests."""
        completed = sum(1 for r in self.request_history if r.state == RequestState.RELEASED)
        cancelled = sum(1 for r in self.request_history if r.state == RequestState.CANCELLED)
        return {"completed": completed, "cancelled": cancelled}

    def get_peak_zone(self):
        """Identifies the zone with the highest current utilization."""
        highest_util = -1
        peak_zone_name = "None"
        
        for zone in self.zones.values():
            util = zone.calculate_utilization()
            if util > highest_util:
                highest_util = util
                peak_zone_name = zone.name
        
        return f"{peak_zone_name} ({highest_util:.1f}%)"