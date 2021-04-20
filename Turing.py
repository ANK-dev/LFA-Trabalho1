import sys, time

class TuringMachine:
    states = {}
    current_state = {}

    def __init__(self, state_matrix):
        self.__init_states(state_matrix)
        self.__set_state(0)

    def __init_states(self, state_matrix):
        """
        Intializes the Turing Machine's states as a dictionary of dictionaries
        of dictionaries! (Tree-like structure).
        """

        symbols = {}
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

            last_state = row[0]

    def __set_state(self, next_state):
        """Sets current state to the next state"""
        self.current_state = self.states[next_state]

    def read_input(self, input_value):
        """Reads input and processes the next state"""
        if input_value == 0 or input_value == 1 or input_value == 'b':
            next_state = self.current_state[input_value]['next_state']
            self.__set_state(next_state)
        else:
            # Input is not 0, 1 or blank
            raise ValueError(input_value)

    def write_output(self, input_data):
        """Returns the Turing Machine's output"""

        # For debugging purposes
        print(self.current_state)
        print(self.current_state[input_data])

        return self.current_state[input_data]

class Tape:
    current_pos = 0
    length = 100
    data = ['b'] * length

    def __init__(self, input_data, starting_index):
        self.__init_data(input_data, starting_index)

    def __init_data(self, input_data, starting_index):
        self.current_pos = starting_index
        for pos, element in zip(range(self.current_pos, self.length), input_data):
            self.data[pos] = element

    def read_data(self, direction=0):
        self.current_pos += direction
        # print(self.current_pos)
        return (
            int(self.data[self.current_pos])
            if self.data[self.current_pos].isdigit()
            else self.data[self.current_pos]
        )

def main():
    state_matrix = [
        [0,  0,  1,  0, 'R'],
        [0,  1,  0,  0, 'R'],
        [0, 'b', 1,  1, 'L'],
        [1,  0,  0,  1, 'R'],
        [1,  1,  0,  1, 'R']
    ]

    my_tm = TuringMachine(state_matrix)
    my_tape = Tape('0110b', 0)
    while True:
        try:
            # Fix KeyError: 'b'
            output = my_tm.write_output(my_tape.read_data())
            time.sleep(1)
            new_dir = 1 if output['direction'] == 'R' else -1
            my_tm.read_input(my_tape.read_data(new_dir))
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)



if __name__ == "__main__":
    main()