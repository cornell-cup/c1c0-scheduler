#include <assert.h>
#include <stdint.h>
#include <stdio.h>

#include "../reference/R2Protocol.h"
#include "../reference/R2Protocol.hpp"

void test_encode_simple() {
  char text[] = "Hello world!";
  uint8_t* data = reinterpret_cast<uint8_t*>(text);
  uint8_t buffer[12 + 16];

  R2Protocol::encode("TEST", data, 12, buffer, 12 + 16, true);
  uint8_t golden[] = {
    0xa2, 0xb2, 0xc2,
    189, 34,
    'T', 'E', 'S', 'T',
    0, 0, 0, 12,
    'H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!',
    0xd2, 0xe2, 0xf2
  };
  for (uint32_t i = 0; i < 12 + 16; i++) {
    assert(buffer[i] == golden[i]);
  }
}

void test_decode_simple() {
  uint8_t buffer[] = {
    0xa2, 0xb2, 0xc2,
    189, 34,
    'T', 'E', 'S', 'T',
    0, 0, 0, 12,
    'H', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd', '!',
    0xd2, 0xe2, 0xf2
  };

  uint8_t data[12];
  uint32_t data_len;
  uint16_t checksum;
  char type[5];

  R2Protocol::decode(buffer, 12 + 16, type, data, &data_len, &checksum);

  assert(strncmp(type, "TEST", 4) == 0);
  assert(checksum == ((189 << 8) | 34));
  assert(data_len == 12);
  assert(strncmp(reinterpret_cast<char*>(data), "Hello world!", 12) == 0);
}

void test_random() {
  char text[] = "Hello world!";
  uint32_t len = strlen(text);
  uint8_t* data = reinterpret_cast<uint8_t*>(text);
  uint8_t* c_buffer = new uint8_t[len + 16];
  uint8_t* cpp_buffer = new uint8_t[len + 16];

  assert(r2p_encode("TEST", data, len, c_buffer, len + 16) == (int32_t) len + 16);
  assert(R2Protocol::encode("TEST", data, len, cpp_buffer, len + 16, true) == (int32_t) len + 16);
  for (uint32_t i = 0; i < len + 16; i++) {
    assert(c_buffer[i] == cpp_buffer[i]);
  }

  delete c_buffer;
  delete cpp_buffer;
}

int main(int argc, char** argv) {
  test_encode_simple();
  test_decode_simple();
  printf("%s: All tests pass!\n", argv[0]);
  return 0;
}
