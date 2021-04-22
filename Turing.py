import sys, time

class TuringMachine:
    states        = {}
    current_state = {}

    def __init__(self, state_matrix):
        self.__init_states(state_matrix)
        self.__set_state(0)

    def __init_states(self, state_matrix):
        """
        Intializes the Turing Machine's states as a dictionary of dictionaries
        of dictionaries! (Tree-like structure).
        """
        symbols    = {}
        last_state = 0

        for row in state_matrix:

            # Checks if we're in a new state from the input matrix, copies the
            # symbol dict to the state dict and clears the symbol dict for the
            # new state.
            if row[0] > last_state:
                self.states[last_state] = symbols.copy()
                symbols.clear()

            symbols[row[1]] = {
                'present_state':  row[0],
                'present_symbol': row[1],
                'symbol_printed': row[2],
                'next_state':     row[3],
                'direction':      row[4]
            }

            # Special case: we're on the last row of the matrix. Copy symbol
            # dict to state dict before the end of the loop.
            if row == state_matrix[-1]:
                self.states[last_state] = symbols.copy()
                symbols.clear()

            # Update last state for the next iteration
            last_state = row[0]

    def __set_state(self, next_state):
        """
        Sets current state to the next state
        """
        self.current_state = self.states[next_state]


    def __write_output(self, output, output_func):
        """
        Writes the current state's output (symbol printed) to tape by calling
        the tape writing function (passed as argument)
        """
        output_func(output['symbol_printed'])

    def execute(self, input_value, output_func):
        """
        Reads input, returns output and processes the next state
        """
        if input_value == 0 or input_value == 1 or input_value == 'b':
            if input_value in self.current_state:
                # Gets output before changing state and writes to tape
                output = self.current_state[input_value]
                self.__write_output(output, output_func)

                # Gets next state and sets current state to it
                next_state = self.current_state[input_value]['next_state']
                self.__set_state(next_state)

                # Returns previous state output
                return output
            else:
                # Input key doesn't exist in current state's dictionary.
                # Halt processing
                print("State doesn't exist. Halt!")
                sys.exit(0)
        else:
            # Input is not 0, 1 or blank
            raise ValueError(input_value)

class Tape:
    current_pos = 0
    length      = 0
    data        = []

    def __init__(self, input_data, starting_index, length):
        self.length = length
        self.current_pos = starting_index
        self.data = ['b'] * self.length
        self.__init_data(input_data, starting_index)

    def __init_data(self, input_data, starting_index):
        """
        Initializes tape with input data from a starting index
        """
        for pos, element in zip(
            range(self.current_pos, self.length), input_data
        ):

            # Hack for dealing with digit and strings, might fix later
            self.data[pos] = (
                int(element) if str(element).isdigit() else element
            )

    def read_data(self, direction=0):
        """
        Reads tape data to the left, to the right or at current tape head
        position
        """

        # Moves tape head to the left or to the right
        self.current_pos += direction

        # Hack for dealing with digit and strings, might fix later
        # if str(self.data[self.current_pos]).isdigit():
        #     return int(self.data[self.current_pos])
        # else:
        return self.data[self.current_pos]

    def write_data(self, input_data):
        """
        Writes data to tape
        """
        self.data[self.current_pos] = input_data

def main():

    ################################ Settings #################################

    # Tape Settings
    TAPE_DATA = '0110b'
    TAPE_LENGTH = 21    # Change to 70 later
    TAPE_STARTING_INDEX = (TAPE_LENGTH - len(TAPE_DATA)) // 2

    # Turing Machine Settings
    STATE_MATRIX = [
        [0,  0,  1,  0, 'R'],
        [0,  1,  0,  0, 'R'],
        [0, 'b', 1,  1, 'L'],
        [1,  0,  0,  1, 'R'],
        [1,  1,  0,  1, 'R']
    ]

    ###########################################################################

    # Defines new instances of a Turing Machine and its tape
    my_tm   = TuringMachine(STATE_MATRIX)
    my_tape = Tape(TAPE_DATA, TAPE_STARTING_INDEX, TAPE_LENGTH)

    new_dir = 0   # Initial tape head direction
    i       = 0   # Current iteration

    print("*** Turing Machine ***",
          "Press CTRL+C or CTRL+D anytime to exit",
          "",
          sep='\n')

    print(f"{i}: {my_tape.data}")  # Initial tape state

    while True:
        try:
            i += 1
            output = my_tm.execute(
                my_tape.read_data(new_dir),
                my_tape.write_data
            )
            print(f"{i}: {my_tape.data}")
            new_dir = 1 if output['direction'] == 'R' else -1
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)

if __name__ == "__main__":
    main()