import sys, time, yaml
from typing import Callable, Union, cast

# Typedefs
output_t        = dict[str, Union[int, str]]
current_state_t = dict[str, output_t]
states_t        = dict[int, current_state_t]
tm_matrix_t     = list[list[Union[int, str]]]

class TuringMachine:
    """
    Defines a Turing Machine (TM)
    """
    states:        states_t        = {}
    current_state: current_state_t = {}

    def __init__(self, tm_matrix: tm_matrix_t) -> None:
        self.__init_states(tm_matrix)
        self.__set_state(0)

    def __init_states(self, tm_matrix: tm_matrix_t) -> None:
        """
        Intializes the Turing Machine's states as a dictionary of dictionaries
        of dictionaries! (Tree-like structure).
        """
        symbols:    dict = {}
        last_state: int  = 0

        for row in tm_matrix:
            # Stringfies 'Present Symbol' and 'Symbol Printed' columns
            row[1] = str(row[1])
            row[2] = str(row[2])

            # Checks if we're in a new state from the input matrix, copies the
            # symbol dict to the state dict and clears the symbol dict for the
            # new state.
            if row[0] != last_state:
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
            if row == tm_matrix[-1]:
                self.states[last_state] = symbols.copy()
                symbols.clear()

            # Update last state for the next iteration
            last_state = cast(int, row[0])

    def __set_state(self, next_state: int) -> None:
        """
        Sets current state to the next state
        """
        self.current_state = self.states[next_state]


    def __write_output(
        self,
        output:      output_t,
        output_func: Callable[[str], None]
    ) -> None:
        """
        Writes the current state's output (symbol printed) to tape by calling
        the tape writing function (passed as argument)
        """
        output_func(cast(str, output['symbol_printed']))

    def execute(
        self,
        input_value: str,
        output_func: Callable[[str], None]
    ) -> output_t:
        """
        Reads input, returns output and processes the next state
        """
        # checks if input exists in current state dict
        if input_value in self.current_state:

            # Gets output before changing state and writes to tape
            output: output_t = self.current_state[input_value]
            self.__write_output(output, output_func)

            # Gets next state and sets current state to it
            next_state: int = cast(
                int, self.current_state[input_value]['next_state']
            )
            self.__set_state(next_state)

            # Returns previous state output
            return output
        else:
            # Input key doesn't exist in current state's dictionary.
            # Halt processing
            print("\nState doesn't exist! Halt!")
            sys.exit(0)

class Tape:
    current_pos: int       = 0
    length:      int       = 0
    data:        list[str] = []

    def __init__(
        self,
        input_data:     str,
        starting_index: int,
        length:         int
    ) -> None:
        self.current_pos = starting_index
        self.length      = length
        self.data        = ['b'] * self.length
        self.__init_data(input_data, starting_index)

    def __init_data(self, input_data: str, starting_index: int) -> None:
        """
        Initializes tape with input data from a starting index
        """
        for pos, element in zip(
            range(self.current_pos, self.length), input_data
        ):
            self.data[pos] = element

    def read_data(self, direction: int = 0) -> str:
        """
        Reads tape data to the left, to the right or at current tape head
        position
        """

        # Moves tape head to the left or to the right
        self.current_pos += direction

        try:
            # Avoid negative wraparound
            if self.current_pos < 0:
                raise IndexError

            return self.data[self.current_pos]
        except IndexError:
            # Stop execution if bounds of tape are reached
            lr_bound: str = (
                'Right' if self.current_pos > len(self.data) - 1 else 'Left'
            )
            print(f"\n{lr_bound} bound of tape reached! Halt!")
            sys.exit(1)

    def write_data(self, input_data: str) -> None:
        """
        Writes data to tape
        """
        self.data[self.current_pos] = input_data

    def get_data(self, direction: int = 0) -> str:
        """
        Returns formated tape data with tape head overlay
        """

        # Tape head characters
        th_left:  str = '>'
        th_right: str = '<'

        data: list[str] = self.data.copy()

        # Keep head in place if direction is past the bounds of the tape
        try:
            # Avoid negative wraparound
            if self.current_pos + direction < 0:
                raise IndexError

            # Draw tape head overlay at new index
            data[self.current_pos + direction] = (
                f"{th_left}{data[self.current_pos + direction]}{th_right}"
            )
        except IndexError:
            data[self.current_pos] = (
                f"{th_left}{data[self.current_pos]}{th_right}"
            )

        # Formatting tweaks
        data_str: str = str(data)   \
            .replace('\'' ,  '')    \
            .replace('['  ,  '[ ')  \
            .replace(']'  ,  ' ]')  \
            .replace(','  ,  ' ,')  \
            .replace(f', {th_left}'  ,  f',{th_left}')  \
            .replace(f'{th_right} ,' ,  f'{th_right},') \
            .replace(f'{th_right} ]' ,  f'{th_right}]') \
            .replace(f'[ {th_left}'  ,  f'[{th_left}')

        return data_str

def main() -> None:
    ################################ Settings #################################

    # Loads input data from YAML file
    with open('Turing_input.yaml', 'r') as stream:
        try:
            input_data: dict = yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print("[ERROR] Error processing YAML file:", error)
            sys.exit(1)

    # Tape Settings
    TAPE_DATA:   str = input_data['TAPE_DATA']
    TAPE_LENGTH: int = len(TAPE_DATA) + 6        # TODO: Change to 70 later!!!
    TAPE_STARTING_INDEX: int = (                 # Center data on tape
        TAPE_LENGTH - len(TAPE_DATA)
    ) // 2

    # Turing Machine Settings
    TM_MATRIX: tm_matrix_t = input_data['TM_MATRIX']
    MAX_ITER:  int         = input_data['MAX_ITER']

    # Debug Settings
    DEBUG: bool = input_data['DEBUG']

    ###########################################################################

    print(f"{'*** Turing Machine ***' : ^52}",
           "[NOTE] Press CTRL+C anytime during execution to halt",
           "",
          sep='\n')

    # Wait for user confirmation to proceed
    try:
        input("Press ENTER to start execution, CTRL+C to exit...")
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
        sys.exit(0)

    # Defines new instances of a TM and its tape
    my_tm:   TuringMachine = TuringMachine(TM_MATRIX)
    my_tape: Tape          = Tape(TAPE_DATA, TAPE_STARTING_INDEX, TAPE_LENGTH)

    new_dir: int = 0    # Initial tape head direction
    i:       int = 0    # Current iteration
    output:  output_t   # TM's output

    # Initial tape state
    print(f"{i} (R): {my_tape.get_data()}", end='', flush=True)

    # Main loop
    while i < MAX_ITER or MAX_ITER == -1:
        try:
            # Calculates the output of the TM
            output = my_tm.execute(
                my_tape.read_data(new_dir),
                my_tape.write_data
            )

            # Debug only
            if DEBUG: print(output, end='')

            # Sets tape head direction
            new_dir = 1 if output['direction'] == 'R' else -1

            # Write current iteration
            time.sleep(0.5)
            print(f"\r{i} (W): {my_tape.get_data()}",
                  end='', flush=True)

            # Read next iteration
            i += 1
            time.sleep(0.5)
            print(f"\r{i} (R): {my_tape.get_data(new_dir)}",
                  end='', flush=True)
        except KeyboardInterrupt:
            print("\nHalting...")
            sys.exit(0)

    print("\nMax number of iterations reached! Halt!")

if __name__ == "__main__":
    main()