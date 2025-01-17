import sys
import mmap
import numpy as np
import multiprocessing

def seq_sort(arr, begin, end):
    """Sorts the array sequentially for a small range."""
    arr[begin:end] = np.sort(arr[begin:end])

def merge(arr, begin, mid, end, temparr):
    """Merges two sorted halves into a temporary array."""
    left, right, dst = begin, mid, 0

    while left < mid or right < end:
        if left < mid and (right >= end or arr[left] <= arr[right]):
            temparr[dst] = arr[left]
            left += 1
        else:
            temparr[dst] = arr[right]
            right += 1
        dst += 1

    arr[begin:end] = temparr[:dst]

def merge_sort(arr, begin, end, threshold):
    """Recursive merge sort using multiprocessing."""
    if end - begin <= threshold:
        seq_sort(arr, begin, end)
        return

    mid = (begin + end) // 2

    #starts a process for each half of the array
    left_process = multiprocessing.Process(target=merge_sort, args=(arr, begin, mid, threshold))
    right_process = multiprocessing.Process(target=merge_sort, args=(arr, mid, end, threshold))

    left_process.start()
    right_process.start()
    left_process.join()
    right_process.join()

    temparr = np.empty(end - begin, dtype=arr.dtype)
    merge(arr, begin, mid, end, temparr)

def main(argv):
    """Main function to read a file, sort it, and save it back."""
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <filename> <sequential threshold>")
        return 1

    filename = argv[1]
    try:
        threshold = int(argv[2])
    except ValueError:
        print("Error: Invalid threshold value")
        return 1

    try:
        with open(filename, "r+b") as f:
            file_size = f.seek(0, 2)  # Get file size
            f.seek(0)
            data = mmap.mmap(f.fileno(), file_size, access=mmap.ACCESS_WRITE)

            # Create a numpy array from the memory-mapped file
            arr = np.ndarray((file_size // 8,), dtype=np.int64, buffer=data)

            # Perform merge sort
            merge_sort(arr, 0, len(arr), threshold)
            print("Sorting complete.")

            # Ensure the array is no longer used before closing mmap
            del arr

    except Exception as e:
        print(f"Error: {e}")
        return 1

    finally:
        # Cleanup
        if 'data' in locals():
            data.close()

if __name__ == "__main__":
    main(sys.argv)
