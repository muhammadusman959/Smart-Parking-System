from parking_request import RequestState

class AllocationEngine:
    def __init__(self, zone_manager):
        """
        Handles the logic for finding and assigning slots.
        Ref: [cite: 54-61]
        """
        self.zone_manager = zone_manager  # Reference to the map of all zones

    def process_allocation(self, request):
        """
        Main algorithm to allocate a slot for a request.
        Returns the assigned ParkingSlot or None if full.
        """
        
        # 1. Identify the requested zone
        primary_zone = self.zone_manager.get_zone(request.requested_zone_id)
        if not primary_zone:
            print(f"Error: Zone {request.requested_zone_id} does not exist.")
            return None

        # 2. Strategy A: Same-Zone Preference 
        # Search for first available slot in the requested zone
        slot = primary_zone.find_first_available_slot()
        
        if slot:
            print(f"Allocated in Preferred Zone {primary_zone.zone_id}")
            self._finalize_allocation(request, slot)
            return slot

        # 3. Strategy B: Cross-Zone Allocation 
        # If primary zone is full, check neighbors
        print(f"Zone {primary_zone.zone_id} is full. Attempting cross-zone allocation...")
        
        for neighbor_id in primary_zone.adjacent_zone_ids:
            neighbor_zone = self.zone_manager.get_zone(neighbor_id)
            if neighbor_zone:
                slot = neighbor_zone.find_first_available_slot()
                if slot:
                    print(f"Allocated in Neighbor Zone {neighbor_zone.zone_id} (Penalty Applied)")
                    # [cite: 61] Incurs penalty - Logic can be added here (e.g., flag on request)
                    self._finalize_allocation(request, slot)
                    return slot

        print("Allocation Failed: No slots available in Zone or Neighbors.")
        return None

    def _finalize_allocation(self, request, slot):
        """
        Helper to commit changes once a slot is found.
        Ref: 
        """
        # 1. Update Request State
        request.update_state(RequestState.ALLOCATED)
        request.assign_slot(slot.slot_id)
        
        # 2. Update Slot Status
        slot.occupy(request.vehicle_id)