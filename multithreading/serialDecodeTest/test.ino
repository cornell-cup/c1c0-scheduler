#include "R2Protocol.h"

uint8_t recv_buffer[27];
String msg;
int32_t x = 1000;
uint16_t checksum;
uint8_t type[5];
char data[11];
uint32_t data_len = 11;

void setup() {
  Serial.begin(115200); 
  Serial1.begin(115200);
}

void loop() {
  if (Serial1.available() > 0) {
    Serial1.readBytes(recv_buffer, 27);

  Serial.println("Received:");

  /*for(int i = 0; i < 27; i++){
    Serial.print(recv_buffer[i]);
  }*/

  //uint8_t num [5];
  x = r2p_decode(recv_buffer, 27, &checksum, type, data, &data_len);
  for(int i = 0; i < 5; i++)
    Serial.print(String(type[i]));
  //data buffer of form: {'axis: 00 +1' or 'button_a :)'}

  for(int i = 0; i < 11; i++){
    Serial.print((data[i]));
    Serial.print(" ");
    msg += data[i];
  }
  //Serial.print("message: " + msg);
   
  if(msg.equals("button_a p") || msg.equals("button_b p") || msg.equals("button_x p") || msg.equals("axis: 0 -1") || msg.equals("axis: 0 1 ") || msg.equals("axis: 1 0 ")|| msg.equals("axis: -1 0"))
      Serial.print("  correct: " + msg);

  //if(checksum)
  Serial.println();
  //else{
  Serial1.flush();
  msg = "";
  //}
  
  //     Serial.println("");
  //     for (int i=0; i<13; i++){
  //        Serial.println(data[i]);
  // }

  }
}
