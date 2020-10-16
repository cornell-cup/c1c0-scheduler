CC=g++
CFLAGS=-std=c++11 -Wall
LDFLAGS=
SOURCES=$(wildcard test/*.cpp)
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=$(SOURCES:.cpp=.x)

all: test
	$(foreach x,$(EXECUTABLE),./$(x);)

test: $(EXECUTABLE)

test/%.x: test/%.cpp
	$(CC) $(CFLAGS) $(LDFLAGS) $< -o $@

clean:
	-rm test/*.o test/*.x
