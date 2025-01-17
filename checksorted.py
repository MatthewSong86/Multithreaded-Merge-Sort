import sys
import struct

def validate_sorted_file(filename):
    try:
        with open(filename, "rb") as f:
            # Read the first 8 bytes
            data = f.read(8)
            if len(data) < 8:
                print("File is empty or does not contain valid int64 data")
                return 1

            prev = struct.unpack('q', data)[0] #Unpack the data as a long long
            num_elts = 1

            # Read remaining elements
            while True:

                data = f.read(8)
                if len(data) < 8:  # End of file
                    break

                curr = struct.unpack('q', data)[0]
                num_elts += 1

                if curr < prev:
                    print(f"Data values are not sorted! (element {num_elts} is less than element {num_elts - 1})", file=sys.stderr)
                    return 1

                prev = curr

        print("Data values are sorted!")
        return 0

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        return 1
    except IOError as e:
        print(f"Error reading file '{filename}': {e}", file=sys.stderr)
        return 1
    except struct.error:
        print("Error: File does not contain valid int64 data", file=sys.stderr)
        return 1

def main(argv):
    if len(argv) != 2:
        print("Usage: " + argv[0] + " <datafile>")
        sys.exit(1)

    filename = argv[1]
    result = validate_sorted_file(filename)
    sys.exit(result)

if __name__ == "__main__":
    main(sys.argv)
