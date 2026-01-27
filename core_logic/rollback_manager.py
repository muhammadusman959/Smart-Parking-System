# CORRECTED IMPORT: Added 'core_logic.' prefix
from core_logic.parking_request import RequestState

class RollbackManager:
    def __init__(self):
        self.history_stack = []

    def log_allocation(self, request, slot):
        # Push the operation to the stack
        # Store tuple: (type, request_obj, slot_obj)
        self.history_stack.append(('ALLOCATE', request, slot))

    def undo(self):
        if not self.history_stack:
            return False

        action_type, request, slot = self.history_stack.pop()

        if action_type == 'ALLOCATE':
            # Reverse the allocation
            slot.free_slot()
            request.update_state(RequestState.CANCELLED)
            return True
        
        return False 