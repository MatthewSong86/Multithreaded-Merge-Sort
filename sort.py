import sys
import mmap
import os
import multiprocessing

def compare_i64(left, right):
    if left < right:
        return -1
    if left > right:
        return 1
    return 0

def seq_sort(arr, begin, end):
    num_elements = end - begin
    arr[begin:end] = sorted(arr[begin:end], key=lambda x: x)

def fatal(msg):
    print(f"Error: {msg}")
    sys.exit(1)

def merge(arr, begin, mid, end, temparr):
    left = begin
    right = mid
    dst = 0

    while left < mid or right < end:
        at_end_l = left >= mid
        at_end_r = right >= end

        if at_end_l and at_end_r:
            break

        if at_end_l:
            temparr[dst] = arr[right]
            right += 1
        elif at_end_r:
            temparr[dst] = arr[left]
            left += 1
        else:
            cmp = compare_i64(arr[left], arr[right])
            if cmp <= 0:
                temparr[dst] = arr[left]
                left += 1
            else:
                temparr[dst] = arr[right]
                right += 1
        dst += 1

    # Copy the merged elements back to the original array
    arr[begin:end] = temparr[:dst]

def merge_sort(arr, begin, end, threshold):
    assert end >= begin
    size = end - begin

    if size <= threshold:
        seq_sort(arr, begin, end)
        return

    mid = begin + size // 2

    pidLeft = os.fork()
    if pidLeft == 0:
        # This is now in the child process
        merge_sort(arr, begin, mid, threshold)
        os._exit(0)
    elif pidLeft < 0:
        # fork failed to start a new process
        # handle the error and exit
        fatal("Error: fork failed to start a new process")

    # Fork the right child process
    pidRight = os.fork()
    if pidRight == 0:
        # This is now in the child process
        merge_sort(arr, mid, end, threshold)
        os._exit(0)
    elif pidRight < 0:
        # fork failed to start a new process
        # handle the error and exit
        os.waitpid(pidLeft, 0)
        fatal("Error: fork failed to start a new process")

    # Wait for the left child process to finish
    os.waitpid(pidLeft, 0)

    # Wait for the right child process to finish
    os.waitpid(pidRight, 0)

    temp_arr = [0] * size
    merge(arr, begin, mid, end, temp_arr)

def main(argv):
    if len(argv) != 3:
        print("Usage: " + argv[0] + " <filename> <sequential threshold>")

    filename = argv[1]
    try:
        threshold = int(argv[2])
    except ValueError:
        print("Error: Invalid threshold value")
        return 1

    try:
        fd = os.open(filename, os.O_RDWR)
    except OSError:
        print("Error: File cannot be opened")
        return 1

    try:
        statbuf = os.fstat(fd)
    except OSError:
        print("Error: fstat error")
        os.close(fd)
        return 1

    file_size_in_bytes = statbuf.st_size

    try:
        data = mmap.mmap(fd, file_size_in_bytes, access=mmap.ACCESS_WRITE)
    except mmap.error:
        print("Error: Mapping data has failed")
        os.close(fd)
        return 1

    os.close(fd)  # Close the file descriptor immediately after mmap

    # Calculate the size of the array
    size = file_size_in_bytes // 8  # sizeof(int64_t) is 8 bytes

    merge_sort(data, 0, size, threshold)

    # Clean up
    data.close()

    
if __name__ == "__main__":
    main(sys.argv)