#include <Arduino.h>
#include <FlexyStepper.h>


//
// stp and dir pin assignments (see electronic/hardware/schematic sheet MCU)
//
const int MOTOR_STEP_PIN = 32;
const int MOTOR_DIRECTION_PIN = 33;


//
// create the stepper motor object
//
FlexyStepper stepper;

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
  // Note 1: It is assumed that you are using a stepper motor with a 
  // 1.8 degree step angle (which is 200 steps/revolution). This is the
  // most common type of stepper.
  //
  // Note 2: It is also assumed that your stepper driver board is  
  // configured for 8x microstepping.
  //
  // Note 3: This example uses "relative" motions.  This means that each
  // command will move the number of steps given, starting from it's 
  // current position.
  //

  //
  // set the speed and acceleration rates for the stepper motor
  //
  stepper.setSpeedInStepsPerSecond(100);
  stepper.setAccelerationInStepsPerSecondPerSecond(100);

  //
  // Rotate the motor in the forward direction one revolution (200 steps). 
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
