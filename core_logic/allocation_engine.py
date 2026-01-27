
from core_logic.parking_request import RequestState

class AllocationEngine:
    def __init__(self, zones_map):
        self.zones = zones_map

    def allocate_slot(self, request):
        preferred_zone = self.zones.get(request.preferred_zone_id)
        
        if not preferred_zone:
            request.update_state(RequestState.CANCELLED)
            return False, None

        
        slot = self.find_slot_in_zone(preferred_zone)
        
        
        if not slot:
            for zid, zone in self.zones.items():
                if zid != request.preferred_zone_id:
                    slot = self.find_slot_in_zone(zone)
                    if slot: break
        
        if slot:
            slot.occupy_slot(request.vehicle_id)
            request.allocate(slot.slot_id)
            request.complete() 
            return True, slot
        else:
            request.update_state(RequestState.CANCELLED)
            return False, None

    def find_slot_in_zone(self, zone):
        for area in zone.parking_areas:
            for slot in area.slots:
                if not slot.is_occupied:
                    return slot
        return None