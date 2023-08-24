CC = g++
CFLAGS = #-Wall -O2 -I /path/to/armadillo-10.x.x/include
LDFLAGS = #-L /path/to/armadillo-10.x.x/lib -larmadillo
LDFLAGS = -larmadillo

TARGET_ARMA_PHASE_SHIFT_CALIB = test_arma_phase_shift_calib.a
TARGET_ARMA = test_arma.a
TARGET_RAW = test_raw.a

all: $(TARGET_ARMA) $(TARGET_RAW) $(TARGET_ARMA_PHASE_SHIFT_CALIB)

$(TARGET_ARMA_PHASE_SHIFT_CALIB): test_arma_phase_shift_calib.cpp
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS) -O3 -std=c++17 -g -Wall -march=native -m64 -DNDEBUG

$(TARGET_ARMA): test_arma.cpp
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

$(TARGET_RAW): test_raw.cpp
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET_ARMA_PHASE_SHIFT_CALIB)
	rm -f $(TARGET_ARMA)
	rm -f $(TARGET_RAW)
