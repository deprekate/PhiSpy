CC = g++
FLAGS = -O3
all:
	$(CC) $(FLAGS) PhiSpy_tools/repeatFinder.cpp -o PhiSpy_tools/repeatFinder
