#include <Arduino.h>
#include <FlexyStepper.h>

// The following programme assumes: 
// You are using a TMC2209 V1.3 stepper motor driver breakout board
// You are wiring the driver to the MCU according to the MCU pinout found in electronic/hardware/schematic sheet MCU
// You have wired the EN pin on the stepper motor driver to the common GND node. This enables the driver in hardware. Active low IC. 
// You have wired the MS1 and MS2 pins on the stepper motor board to common GND. Hardware set for 8x microstepping. 

//==================================================================================================================================
// Settings for stp and dir pin assignments (adjust if needed)
//==================================================================================================================================
const int MOTOR_STEP_PIN = 32;
const int MOTOR_DIRECTION_PIN = 33;
//==================================================================================================================================
// Settings for creating the stepper motor object
//==================================================================================================================================
FlexyStepper stepper;
//==================================================================================================================================
// Settings for microstepping 
//==================================================================================================================================
int micro_stepping_configuration = 8;
int revolution = 200 * micro_stepping_configuration; // nema 11 is 200 steps/rev 


void setup() 
{
  
  Serial.begin(115200);

  // connect and configure the stepper motor to its IO pins
  stepper.connectToPins(MOTOR_STEP_PIN, MOTOR_DIRECTION_PIN);
}



void loop() 
{

  //
  // set the speed and acceleration rates for the stepper motor
  //
  stepper.setSpeedInStepsPerSecond(100);
  stepper.setAccelerationInStepsPerSecondPerSecond(100);

  //
  // Rotate the motor in the forward direction one revolution (1600 steps). 
  // This function call will not return until the motion is complete.
  //
  stepper.moveRelativeInSteps(revolution);

  //
  // now that the rotation has finished, delay 1 second before starting 
  // the next move
  //
  delay(1000);

  //
  // rotate backward 1 rotation, then wait 1 second
  //
  stepper.moveRelativeInSteps(-revolution);
  delay(1000);

  //
  // This time speedup the motor, turning 10 revolutions.  Note if you
  // tell a stepper motor to go faster than it can, it just stops.
  //
  stepper.setSpeedInStepsPerSecond(800);
  stepper.setAccelerationInStepsPerSecondPerSecond(800);
  stepper.moveRelativeInSteps(revolution * 10);
  delay(2000);
}
