from collections import deque
from parking_request import RequestState

class RollbackManager:
    def __init__(self):
        """
        Manages the history of operations to support rollback.
        Ref: [cite: 62-70]
        """
        # Using deque as a Stack (LIFO)
        self.operation_stack = deque() 

    def log_allocation(self, request, slot):
        """
        Records a successful allocation so it can be rolled back later.
        Ref: 
        """
        # Store a tuple or small object containing the references needed to undo
        operation_record = {
            'type': 'ALLOCATION',
            'request': request,
            'slot': slot
        }
        self.operation_stack.append(operation_record)
        print(f"[RollbackLog] Recorded allocation for Vehicle {request.vehicle_id}")

    def rollback_last_k_operations(self, k: int):
        """
        Undoes the last k allocation operations.
        Ref: [cite: 67-70]
        """
        count = 0
        while count < k and self.operation_stack:
            last_op = self.operation_stack.pop() # Pop from stack
            
            if last_op['type'] == 'ALLOCATION':
                request = last_op['request']
                slot = last_op['slot']

                # 1. Restore Slot Availability [cite: 65, 69]
                print(f"[Rollback] Undoing allocation for Vehicle {request.vehicle_id} in Slot {slot.slot_id}")
                slot.free()

                # 2. Restore Request State [cite: 66, 70]
                # We revert it back to 'REQUESTED' or 'CANCELLED' depending on interpretation.
                # Usually, 'Rollback' implies undoing the success, so we set it back to CANCELLED 
                # or just reset it. For this project, let's treat it as cancelling the allocation.
                request.state = RequestState.CANCELLED 
                request.assigned_slot_id = None
            
            count += 1
        
        return count  # Returns how many operations were actually rolled back