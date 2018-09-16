# state.py

class State(object):

    def __init__(self):
        print ('Current state:', str(self))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

    def return_to_idle(self):
        """
        Handle return to Idle after operation
        """
        pass