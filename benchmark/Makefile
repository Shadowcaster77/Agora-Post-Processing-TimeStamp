CC = g++
CFLAGS = #-Wall -O2 -I /path/to/armadillo-10.x.x/include
LDFLAGS = #-L /path/to/armadillo-10.x.x/lib -larmadillo
LDFLAGS = -larmadillo

TARGET_ARMA = test_arma.a
TARGET_RAW = test_raw.a

all: $(TARGET_ARMA) $(TARGET_RAW)

$(TARGET_ARMA): test_arma.cpp
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

$(TARGET_RAW): test_raw.cpp
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET_ARMA)
	rf -f $(TARGET_RAW)
