# R2 Protocol Spec

## General

* R2 packets in an ordered connection (UART, TCP) may be split up across packets.
* R2 packets in UDP must fit within a single packet.
* USB serial baud rate must be 115200.

## Protocol

| Section | Bytes | Description | Example |
|:---|:---:|:---|:---|
| Start | 3 | Start of packet bytes | 0xa2b2c2 |
| Checksum | 2 | CRC-16 Checksum (CCITT) of data, or 0x0000 if no checksum | 0x1234 or 0x0000 |
| Type | 4 | Type of data, exactly 4 bytes | "PING" |
| Length | 4 | Length of data (big endian) | 0x0004 |
| Data | ? | Payload data | ? |
| End | 3 | End of packet bytes | 0xd2e2f2 |

## Default packet types

| User | Type | Description |
| :--- | :--- | :--- |
| Master | WHO  | Respond with the device. |
| Master | PING | Check if the device is alive. Must respond with "PONG". |
| Slave | PONG | Response to "PING". |
