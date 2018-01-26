# Team Target-Tek (BYU Capstone Team 19)
# State Machine framework. Governs communications between
# U-blox and Raspberry Pi. Use by initializing the state machine
# and then calling execute_next_state() in a loop.
# Contributors: Lukas Nordlin
# 1/25/2018

class StateMachine:
    
    def __init__(self):
        # Constructor. Initializes to default state.
        self.nextState = StateMachine.waiting_st

    def execute_next_state(self):
        # Call this to move the SM forward one step.
        self.nextState(self)    # Does whatever we set as the next state.

    def initial_st(self):
        # The initial state for the state machine.
        # This will probably be expanded to call initialization code,
        # such as calibrating the accelerometer.
        print('Initial state')
        self.nextState = StateMachine.waiting_st

    def waiting_st(self):
        # Idle state for the state machine. Wait for input.
        print('Waiting state')
        
        # REPLACE THIS BLOCK WITH YOUR OWN LOGIC
        userInputsAvailable = False #TODO: change this to your own logic 
        messagesAvailable = False   #TODO: change this to your own logic 
        # END REPLACE BLOCK

        # State transitions. Feel free to change as needed.
        if messagesAvailable:
            self.nextState = StateMachine.read_ublox_msg_st
        elif userInputsAvailable:
            self.nextState = StateMachine.read_user_input_st
        else:
            self.nextState = StateMachine.write_ublox_msg_st

    def write_ublox_msg_st(self):
        # Write a message to the U-blox.
        print('Write U-blox message state')
        # State transitions.
        self.nextState = StateMachine.waiting_st

    def read_user_input_st(self):
        # Read user input and process it.
        print('Read user input state')
        self.nextState = StateMachine.waiting_st

    def read_ublox_msg_st(self):
        # Read message from the U-blox.
        print('Read U-blox message state')
        self.nextState = StateMachine.waiting_st
