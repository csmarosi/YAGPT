.PHONY: all run clean

ARCHFLAG = -m32
CFLAGS = -fstack-protector-all -g --std=c++11 -Wall -fPIC $(ARCHFLAG)

all: clean $(patsubst %.cpp, %.o, $(wildcard *.cpp))
	g++ $(ARCHFLAG) -shared -o mainLoop.so mainLoop.o
	g++ $(ARCHFLAG) -o main.out main.o -ldl

%.o: %.cpp
	g++ $(CFLAGS) -c $< -o $@

clean:
	rm -vf *.out *.o *.so

run: all
	./main.out
