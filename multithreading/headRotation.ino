#include <Servo.h>
#include "/Users/cecerae/Desktop/servo/headRotation/modified_protocol.h" //Change to whatever path containts the modified R2 protocol, very specific


Servo headServo;  // create servo object to control a servo, currently set up for the HS-755HB servo (non-continuous rotation between 0 and 202 degrees

int ang;        // variable to represent the current angle of the servo
int startPos;   // variable to represent the starting position when chaning the angle of the servo
int endPos;     // variable to represent the ending position (goal) when changing the angle of the servo
bool absolute;  // variable to represent when the angle taken from the serial port is an absolute angle or a change in angle (1 if absolute)
bool negative;  // variable to represent when a change in angle is negative (1 is negative)

const uint8_t dataLength = 4; // since data_len may be changed by decode, this ensures all assumed data lengths are specified manually
uint16_t checksum; //integer for checksum to be inserted into
uint8_t address = 3; // ID address for this microcontroller. If the message does not contain this address of 3, the message will not be processed
uint8_t recv_buffer[R2P_HEADER_SIZE + dataLength]; // this is the receiving buffer which the data will be put into, the data is 2 bytes long, so the buffer is 2 + the header size
uint32_t buffer_len = R2P_HEADER_SIZE + dataLength; 
char type[5]; //character array which the type literal will be inserted into
uint8_t data[4]; //the array which data will be inserted into
uint32_t data_len; // integer for length of data to be inserted into
uint8_t datalast;
uint16_t t;

void setup() {
  headServo.attach(2,556,2410);                  // attaches the servo on pin 9 to the servo object, PWM range between 556-2410 for the HS-755HB (change for different servos)
  Serial.begin(9600);                          // Communication to servo
  Serial2.begin(9600);                         // Communication to jetson
  while (Serial2.available()) Serial2.read(); // clear the serial port from jetson
  while (Serial.available()) Serial.read();   // clear serial port to servo
  t = 0;
  
  headServo.write(90);                          // sets a current angle 
}

void loop() {
  if(Serial2.available() > 0) //checks if there is data in the serial buffer to be read
  {   
      Serial2.readBytes(recv_buffer,R2P_HEADER_SIZE + dataLength); // reads the buffer data storing a buffer_len length of data in in recv_buffer
      r2p_decode(recv_buffer,address,buffer_len,&checksum,type,data, &data_len,&t); // decoding received data

      Serial.println(data[0]);  // angle
      Serial.println(data[1]);  // absolute
      Serial.println(data[2]);  // negative
      
      startPos = headServo.read();
      absolute = data[1];
      negative = data[2];
      
      if (absolute){
        endPos = int(data[0]);
      }
      else{
        if(negative){
          endPos = int(startPos - data[0]);
        }
        else{
          endPos = int(startPos + data[0]);
        }
      }
      
      if (startPos <= endPos && endPos < 202){    // change 202 to max angle as this runs when the ending position is some angle larger than the current one
        for(int pos = startPos; pos <= endPos; pos++){
          ang = headServo.read();                  // sets the servo position according to the scaled value
          //Serial.println(ang);
          headServo.write(pos);
          delay(60);                           // waits for the servo to get there
        }
      }
     else if (startPos >= endPos && endPos > 0){   // change 0 to mmin angle (probably 0) as this runs when the ending position is some angle smaller than the current one
       for(int pos = startPos; pos >= endPos; pos--){
          ang = headServo.read();                  // sets the servo position according to the scaled value
          //Serial.println(ang);
          headServo.write(pos);
          delay(60);                           // waits for the servo to get there
       }
    }
  
  }
}
