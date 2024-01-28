#include <Arduino.h>
#include <FlexyStepper.h>


const int MOTOR_STEP_PIN = 32;
const int MOTOR_DIRECTION_PIN = 33;
const int LIMIT_SWITCH_PIN = 34;


//
// create the stepper motor object
//
FlexyStepper stepper;

//==================================================================================================================================
// Settings for microstepping 
//==================================================================================================================================
int micro_stepping_configuration = 8;
int revolution = 200 * micro_stepping_configuration; // nema 11 is 200 steps/rev 

void setup() 
{

  pinMode(LIMIT_SWITCH_PIN, INPUT_PULLUP);
  Serial.begin(115200);


  //
  // connect and configure the stepper motor to its IO pins
  //
  stepper.connectToPins(MOTOR_STEP_PIN, MOTOR_DIRECTION_PIN);
}



void loop() 
{



  //
  // set the speed and acceleration rates for the stepper motor
  //
  stepper.setSpeedInStepsPerSecond(100);
  stepper.setAccelerationInStepsPerSecondPerSecond(100);




  const int directionTowardHome = -1;        // direction to move toward limit switch: 1 goes positive direction, -1 backward
  
  if(stepper.moveToHomeInSteps(directionTowardHome, 200, 2*revolution, LIMIT_SWITCH_PIN) != true)
  {
    Serial.printf("failed to home");
  }


  //
  // homing is now complete, the motor is stopped at position 0mm
  //
  delay(500);


  //
  // if you want your 0 origin someplace else, you can change it 
  //
  //stepper.setCurrentPositionInMillimeters(325);


  //
  // indicate the program has finished by blinking slowly forever
  //
  while(true)
  {
    Serial.printf("home");
  }
}
