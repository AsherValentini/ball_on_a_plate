#include <Arduino.h>
#include <driver/mcpwm.h>
#include "soc/mcpwm_periph.h"
#include <Ticker.h>
#include <Wire.h>

// ----------------------------------------------------------------------------------------------------------------------------------------------------------
// I2C Slave Information, adjust if 3PAC firmware changes:
// ----------------------------------------------------------------------------------------------------------------------------------------------------------

#define I2C_DEV_ADDR 0x42

uint32_t i = 0;


// ----------------------------------------------------------------------------------------------------------------------------------------------------------
// Function prototypes, add if needed:
// ----------------------------------------------------------------------------------------------------------------------------------------------------------

void onReceive(int len);

void setup()
{
  // ----------------------------------------------------------------------------------------------------------------------------------------------------------
  // I2C setup, adjust if needed:
  // ----------------------------------------------------------------------------------------------------------------------------------------------------------
  Serial.begin(115200);

  Wire.onReceive(onReceive);
  Wire.begin((uint8_t)I2C_DEV_ADDR);

}

void loop()
{
}


void onReceive(int len) {
    Serial.print("Length received: ");
    Serial.println(len);

    char message[64];  // Ensure buffer is appropriately sized
    int index = 0;

    while(Wire.available() && index < (sizeof(message) - 1)) {
        message[index++] = Wire.read();
    }

    message[index] = '\0';  // Null-terminate the string
    Serial.print("Received message: ");
    Serial.println(message);
}