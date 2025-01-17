This is some code I adapted from my homework for EN.601.229 CSF. Essentially, it sorts the input file using a merge sort, 
but at each divide, it creates two child processes to sort the smaller portions. This allows for faster computation speed
compared to a traditional merge sort.

Requirements:
python3, numpy: pip install numpy

Usage:
python3 datagenerator.py <size> <filename>

size - denotes the number of integers to sort
filename - denotes  file name

python3 checksorted.py <filename>
filename - denotes file name

python3 sort.py <filename> <threshold>
filename - denotes file name
threshold - denotes the smallest number of integers before sequential sort is run