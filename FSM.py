import sys

class FSM:
    """Defines a Finite State Machine (FSM)"""
    states = []
    current_state = {}

    def __init__(self, state_matrix):
        # Populates the machine's states
        self.__init_states(state_matrix)

        # Sets the initial state to s0
        self.__set_state(0)

    def __init_states(self, state_matrix):
        """Initializes the FSM's states as a list of dictionaries"""
        for state in range(len(state_matrix)):
            self.states.append(
                {
                    'state':  state,
                    'next0':  state_matrix[state][0],
                    'next1':  state_matrix[state][1],
                    'output': state_matrix[state][2]
                }
            )

    def __set_state(self, next_state):
        """Sets current state to the next state"""
        self.current_state = self.states[next_state]

    def read_input(self, input_value):
        """Reads input and processes the next state"""
        if input_value == 0:
            next_state = self.current_state['next0']
            self.__set_state(next_state)
        elif input_value == 1:
            next_state = self.current_state['next1']
            self.__set_state(next_state)
        else:
            # Input is not 0 or 1
            raise ValueError(input_value)

    def write_output(self):
        """Returns the FSM's output"""
        return self.current_state['output']

"""
Test FSM
========

 Present state |  Next  state  | Output
               | Present Input |
               |   0       1   |
---------------+---------------+--------
       s0      |   s1      s0  |   0
       s1      |   s2      s1  |   1
       s2      |   s2      s0  |   1


For the state_matrix, each row corresponds to a state
For each state: [Input 0 -> Next State, Input 1 -> Next State, Output]
"""

def main():
    state_matrix = [
        # [next0, next1, output]
          [1,     0,     0], # s0
          [2,     1,     1], # s1
          [2,     0,     1], # s2
    ]

    print("*** Finite State Machine ***",
          "Press CTRL+C or CTRL+D anytime to exit",
          "",
          sep='\n')

    while True:
        try:
            # Reset to initial state after each execution
            my_fsm = FSM(state_matrix)

            input_string = input("Input:  ")

            print("Output: ", end='')
            print(my_fsm.write_output(), end='')
            for element in input_string:
                my_fsm.read_input(int(element))
                print(my_fsm.write_output(), end='')
            print("\n")

        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()