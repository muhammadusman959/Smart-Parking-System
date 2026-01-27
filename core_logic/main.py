from parking_system import ParkingSystem
from parking_request import RequestState
import time

def run_simulation():
    print("==========================================")
    print("   SMART PARKING SYSTEM SIMULATION")
    print("==========================================")

    
    city = ParkingSystem()

    
    zone1 = city.add_zone(1, "Downtown")
    zone1.add_parking_area(10, capacity=2) 

    
    zone2 = city.add_zone(2, "Suburbs")
    zone2.add_parking_area(20, capacity=5) 

    
    zone3 = city.add_zone(3, "Industrial")
    zone3.add_parking_area(30, capacity=10)

    
    zone1.add_neighbor(2) 
    
    zone2.add_neighbor(1)
    
    print("\n[Step 1] City Built.")
    print(f"Zone 1 (Downtown): 2 slots | Neighbor: Zone 2")
    print(f"Zone 2 (Suburbs):  5 slots | Neighbor: Zone 1")
    print("------------------------------------------")

    
    print("\n[Step 2] Testing Normal Allocation (Zone 1 has space)")
    city.request_parking("CAR-A", 1)
    city.request_parking("CAR-B", 1) 
    
    
    utilization_z1 = city.get_zone_utilization(1)
    print(f"Zone 1 Utilization: {utilization_z1}% (Expected: 100.0%)")

    
    print("\n[Step 3] Testing Cross-Zone Allocation (Zone 1 Full -> Check Zone 2)")
    city.request_parking("CAR-C", 1) 
    
    
    utilization_z2 = city.get_zone_utilization(2)
    print(f"Zone 2 Utilization: {utilization_z2}% (Expected: 20.0% -> 1/5 slots)")

    
    print("\n[Step 4] Testing Rollback Manager")
    
    print("Rolling back last 1 operation...")
    city.rollback_manager.rollback_last_k_operations(1)
    
    
    utilization_z2_after = city.get_zone_utilization(2)
    print(f"Zone 2 Utilization after Rollback: {utilization_z2_after}% (Expected: 0.0%)")

    
    print("\n[Step 5] Testing Analytics (Simulating trip end)")
    
    req_a = city.request_history[0] 
    req_a.update_state(RequestState.OCCUPIED)
    time.sleep(1) 
    req_a.update_state(RequestState.RELEASED) 

    avg_time = city.get_average_parking_duration()
    print(f"Average Parking Duration: {avg_time:.4f} minutes")

    print("\n==========================================")
    print("   SIMULATION COMPLETE")
    print("==========================================")

if __name__ == "__main__":
    run_simulation()