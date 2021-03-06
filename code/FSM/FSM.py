import sys, yaml

# Typedefs
current_state_t = dict[str, int]
states_t        = list[current_state_t]
state_matrix_t  = list[list[int]]

class FSM:
    """
    Defines a Finite State Machine (FSM)
    """
    states:        states_t        = []
    current_state: current_state_t = {}

    def __init__(self, state_matrix: state_matrix_t) -> None:
        # Populates the machine's states
        self.__init_states(state_matrix)

        # Sets the initial state to s0
        self.__set_state(0)

    def __init_states(self, state_matrix: state_matrix_t) -> None:
        """
        Initializes the FSM's states as a list of dictionaries
        """
        for state in range(len(state_matrix)):
            self.states.append(
                {
                    'state':  state,
                    'next0':  state_matrix[state][0],
                    'next1':  state_matrix[state][1],
                    'output': state_matrix[state][2]
                }
            )

    def __set_state(self, next_state: int) -> None:
        """
        Sets current state to the next state
        """
        self.current_state = self.states[next_state]

    def read_input(self, input_value: str) -> None:
        """
        Reads input and processes the next state
        """
        try:
            input_value_int = int(input_value)
            if input_value_int == 0:
                next_state = self.current_state['next0']
                self.__set_state(next_state)
            elif input_value_int == 1:
                next_state = self.current_state['next1']
                self.__set_state(next_state)
            else:
                # Input is not 0 or 1
                raise ValueError(input_value)
        except ValueError as error:
            print("\n\n[ERROR] Invalid Input:", error)
            sys.exit(1)

    def write_output(self) -> int:
        """
        Returns the FSM's output
        """
        return self.current_state['output']

def main() -> None:
    ################################ Settings #################################

    # Loads input data from YAML file
    with open('FSM_input.yaml', 'r') as stream:
        try:
            input_data: dict = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print("[ERROR] Error processing YAML file:", error)
            sys.exit(1)

    STATE_MATRIX: state_matrix_t = input_data['STATE_MATRIX']

    ###########################################################################

    print(f"{'*** Finite State Machine ***' : ^45}",
           "[NOTE] Press CTRL+C or CTRL+D anytime to exit",
           "",
          sep='\n')


    while True:
        try:
            # Reset to initial state after each execution
            my_fsm:     FSM       = FSM(STATE_MATRIX)
            states_seq: list[str] = ['s0']
            output_str: str       = ''

            input_string: str = input("Insert input string: ")

            output_str += str(my_fsm.write_output())
            for value in input_string:
                my_fsm.read_input(value)
                states_seq.append('s' + str(my_fsm.current_state['state']))
                output_str += str(my_fsm.write_output())

            print()         # 1 newline
            if len(input_string) < 15:
                # Full formatting
                print("Input string:",    ' ' *  6, (' ' * 5).join(input_string))
                print("States sequence:", ' ' *  0, states_seq)
                print("Output string:",   ' ' *  5, (' ' * 5).join(output_str))
                print('-' * 33)
                print("Final state:",     ' ' *  6, states_seq[-1])
                print("Final output:",    ' ' *  6, output_str[-1],
                      "(accepted)" if output_str[-1] == '1' else "(rejected)")
            else:
                # Short formatting
                print("Input:",           ' ' *  0, input_string)
                print("States sequence:", ' ' *  0, states_seq)
                print("Output:",          ' ' *  0, output_str)
                print('-' * 27)
                print("Final state:",     ' ' *  0, states_seq[-1])
                print("Final output:",    ' ' *  0, output_str[-1],
                      "(accepted)" if output_str[-1] == '1' else "(rejected)")
            print('\n')     # 2 newlines

        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()