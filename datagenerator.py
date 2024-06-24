import sys
import random 

#function to convert input to integer and handles negative int or invalid int
def str_to_posint(s):
    try:
        output = int(s, 10)
        if output <= 0:
            print("Error: Input is not positive")
            exit()
        return output
    except ValueError:
        print(f"Error: '{s}' is not a valid integer")
        exit()
    
def main(args):
    #checks for correct command line arguments
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " <size> <output filename> \n")
        exit()
    size = str_to_posint(sys.argv[1])

    output_file = sys.argv[2]

    #writes random integers to file
    try:
        with open(output_file, "wb") as out:
            for i in range(size):
                b = random.randint(0, 255)
                if out.write(bytes([b])) != 1:
                    print("Error: write failed", file=sys.stderr)
                    exit()
    except IOError as e:
        print(f"An error occurred while opening or writing to the file: {e}")      
        exit()
           

if __name__ == "__main__":
    main(sys.argv)