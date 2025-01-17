import sys
import random
import struct

# Function to convert input to a positive integer, handling invalid or negative inputs
def str_to_posint(s):
    try:
        output = int(s, 10)
        if output <= 0:
            print("Error: Input is not positive")
            sys.exit(1)
        return output
    except ValueError:
        print(f"Error: '{s}' is not a valid integer")
        sys.exit(1)

def main(args):
    # Check for correct command-line arguments
    if len(args) != 3:
        print("Usage: " + args[0] + " <size> <output filename>")
        sys.exit(1)

    size = str_to_posint(args[1])
    output_file = args[2]

    # Write random 8-byte integers to the file
    try:
        with open(output_file, "wb") as out:
            for _ in range(size):
                # Generate a random 64-bit signed integer
                rand_int = random.randint(-2**63, 2**63 - 1)
                # Pack it as an 8-byte value and write it to the file
                out.write(struct.pack('q', rand_int))
    except IOError as e:
        print(f"An error occurred while opening or writing to the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv)
