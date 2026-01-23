from django.shortcuts import render, redirect
import sys
import os

# --- PATH FIX: Allow importing core_logic files directly ---
# This tells Django: "Look inside the core_logic folder for files too"
current_dir = os.path.dirname(os.path.abspath(__file__))
core_logic_path = os.path.join(os.path.dirname(current_dir), 'core_logic')
sys.path.append(core_logic_path)

# Now we can import your logic!
from parking_system import ParkingSystem

# --- GLOBAL SYSTEM INITIALIZATION ---
# We create ONE instance of the system that stays alive while the server runs.
SYSTEM = ParkingSystem()

# Let's pre-load some zones so the system isn't empty when you start
if not SYSTEM.zones:
    # Zone 1: Downtown (2 Slots)
    z1 = SYSTEM.add_zone(1, "Downtown")
    z1.add_parking_area(100, capacity=2)
    
    # Zone 2: Suburbs (5 Slots)
    z2 = SYSTEM.add_zone(2, "Suburbs")
    z2.add_parking_area(200, capacity=5)
    
    # Connect them
    z1.add_neighbor(2)
    z2.add_neighbor(1)

# --- VIEW FUNCTIONS ---

# ... (Imports and Setup remain the same) ...

def dashboard(request):
    """Renders the dashboard with ALL required analytics."""
    
    # Get the new stats
    counts = SYSTEM.get_stats_counts()
    peak_zone = SYSTEM.get_peak_zone()
    
    context = {
        'zones': SYSTEM.zones.values(),
        'history': SYSTEM.request_history,
        'avg_duration': SYSTEM.get_average_parking_duration(),
        'completed_count': counts['completed'],   # New Requirement
        'cancelled_count': counts['cancelled'],   # New Requirement
        'peak_zone': peak_zone                    # New Requirement
    }
    return render(request, 'dashboard.html', context)

def process_release(request):
    """Handles the 'Depart' button to finish a trip."""
    if request.method == "POST":
        vehicle_id = request.POST.get('vehicle_id')
        SYSTEM.release_vehicle(vehicle_id)
    return redirect('dashboard')

# ... (process_allocation and process_undo remain the same) ...

def process_allocation(request):
    """Handles the 'Park Vehicle' button click."""
    if request.method == "POST":
        vehicle_id = request.POST.get('vehicle_id')
        zone_id = int(request.POST.get('zone_id'))
        
        # Call your backend logic!
        success = SYSTEM.request_parking(vehicle_id, zone_id)
        
        if success:
            print(f"WEB: Allocated {vehicle_id}")
        else:
            print(f"WEB: Failed to allocate {vehicle_id}")
            
    return redirect('dashboard')

def process_undo(request):
    """Handles the 'Undo Last' button click."""
    SYSTEM.rollback_manager.rollback_last_k_operations(1)
    return redirect('dashboard')