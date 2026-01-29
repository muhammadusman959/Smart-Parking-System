from django.shortcuts import render, redirect
from core_logic.parking_system import ParkingSystem

# Initialize System
SYSTEM = ParkingSystem()

# Configure Zones
if not SYSTEM.zones:
    SYSTEM.add_zone(1, "Hasan Murad Parking Lot")
    SYSTEM.add_zone(2, "Ibrahim Murad Parking Lot")

def dashboard(request):
    just_parked_id = request.session.pop('just_parked_vehicle', None)
    counts = SYSTEM.get_stats_counts()
    peak_zone = SYSTEM.get_peak_zone()
    
    context = {
        'zones': SYSTEM.zones.values(),
        'history': SYSTEM.request_history,
        'avg_duration': SYSTEM.get_average_parking_duration(),
        'completed_count': counts['completed'],
        'cancelled_count': counts['cancelled'],
        'peak_zone': peak_zone,
        'just_parked_id': just_parked_id, 
    }
    return render(request, 'dashboard.html', context)

def process_allocation(request):
    if request.method == "POST":
        vehicle_id = request.POST.get('vehicle_id')
        zone_id = int(request.POST.get('zone_id'))
        
        print(f"DEBUG: Attempting to park {vehicle_id}...") # DEBUG
        success = SYSTEM.request_parking(vehicle_id, zone_id)
        
        if success:
            print("DEBUG: Parking Successful.") # DEBUG
            request.session['just_parked_vehicle'] = vehicle_id
        else:
            print("DEBUG: Parking Failed (Full?).") # DEBUG
        
    return redirect('dashboard')

def process_undo(request):
    if request.method == "POST":
        print("DEBUG: Undo Button Clicked.") # DEBUG
        
        # Check stack size before undoing
        stack_size = len(SYSTEM.rollback_manager.history_stack)
        print(f"DEBUG: Current Stack Size: {stack_size}") 
        
        success = SYSTEM.rollback_manager.undo()
        
        if success:
            print("DEBUG: Undo SUCCESSFUL. Car should be removed.") 
        else:
            print("DEBUG: Undo FAILED. Stack was empty (or server restarted).")

    return redirect('dashboard')

def process_release(request):
    if request.method == "POST":
        vehicle_id = request.POST.get('vehicle_id')
        print(f"DEBUG: Releasing Car {vehicle_id}...")
        SYSTEM.release_parking(vehicle_id)
    return redirect('dashboard')