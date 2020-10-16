#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "../reference/R2Protocol.h"
#include "../reference/R2Protocol.hpp"

// Test the golden string "Hello world!"
void test_golden() {
  char text[] = "Hello world!";
  uint32_t len = strlen(text);
  uint8_t* data = reinterpret_cast<uint8_t*>(text);

  uint16_t crc = r2p_crc16(data, len);
  assert(crc == 48418);
}

// Test all possible 16 bit numbers
void test_full() {
  uint8_t* distribution = new uint8_t[1 << 16];
  uint32_t count = 0;
  for (uint32_t data = 0; data < (1 << 16); data++) {
    uint16_t crc = r2p_crc16(reinterpret_cast<uint8_t*>(&data), 2);
    if (distribution[crc] == 0) {
      count++;
      distribution[crc] = 1;
    }
  }

  // Distribution should be extremely high
  assert(count > (0xf << 12));

  // No crcs should be 0
  assert(distribution[0] == 0);

  delete distribution;
}

// Match c implementation with cpp implementation
void test_full_match() {
  for (uint32_t data = 0; data < (1 << 16); data++) {
    uint16_t c_crc = r2p_crc16(reinterpret_cast<uint8_t*>(&data), 2);
    uint16_t cpp_crc = R2Protocol::crc16(reinterpret_cast<uint8_t*>(&data), 2);
    if (c_crc != cpp_crc) {
      printf("%d %d\n", c_crc, cpp_crc);
    }
    assert(c_crc == cpp_crc);
  }
}

int main(int argc, char** argv) {
  test_golden();
  test_full();
  test_full_match();
  printf("%s: All tests pass!\n", argv[0]);
  return 0;
}
