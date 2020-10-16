#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "../reference/R2Protocol.h"

void test_simple() {
  uint8_t encoded[] = {
    0xa2, 0xb2, 0xc2,
    189, 34,
    'T', 'E', 'S', 'T',
    0, 0, 0, 12,
    'H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!',
    0xd2, 0xe2, 0xf2
  };
  uint32_t encoded_len = 12 + 16;

  uint8_t buffer[256];
  r2pf_t fsm = r2pf_init(buffer, 256);
  for (uint32_t i = 0; i < encoded_len; i++) {
    r2pf_read(&fsm, encoded[i]);
  }
  assert(fsm.done == 1);
  assert(strncmp("TEST", fsm.type, 4) == 0);
  assert(fsm.checksum == ((189 << 8) | 34));
  assert(fsm.crc == fsm.checksum);
  assert(fsm.data_len == 12);
  assert(strncmp(reinterpret_cast<char*>(fsm.data), "Hello world!", 12) == 0);
}

int main(int argc, char** argv) {
  test_simple();
  printf("%s: All tests pass!\n", argv[0]);
  return 0;
}
