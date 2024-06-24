import sys
import struct

def main(argv):
    if len(argv) != 2:
        print("Usage: " + argv[0] + " <datafile>")
        exit()

    with open(argv[0], "rb") as f:
        data = f.read(8)
        if len(data) < 8:
            print("Could not read first data value (file is empty?)")
            return 0

        prev = struct.unpack('q', data)[0]
        num_elts = 1

        # Read remaining elements
        while True:
            data = f.read(8)
            if len(data) < 8:
                break

            curr = struct.unpack('q', data)[0]
            num_elts += 1

            if curr < prev:
                print(f"Data values are not sorted! (element {num_elts} is less than element {num_elts - 1})", file=sys.stderr)
                exit()

            prev = curr

        print("Data values are sorted!")
        exit()


if __name__ == "__main__":
    main(sys.argv)