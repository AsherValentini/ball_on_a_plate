//==================================================================================================================================
// SOUPs
//==================================================================================================================================
#include <Arduino.h>
#include <ESP_FlexyStepper.h> // SEPPER MOTORS
#include <bits/stdc++.h>
using namespace std;
//==================================================================================================================================
// Settings for stp and dir pin assignments (adjust if needed)
//==================================================================================================================================
const int MOTOR_1_STEP = 32;
const int MOTOR_1_DIRECTION = 33;
const int MOTOR_1_EN = 19; 

const int MOTOR_2_STEP = 15;
const int MOTOR_2_DIRECTION = 2;
const int MOTOR_2_EN = 23; 
//==================================================================================================================================
// Settings for limit switches 
//==================================================================================================================================
const int LS_1 = 35;
const int LS_2 = 34; 

// Reactivate flags in case they were cleared
bool waitingForMotor1;
bool waitingForMotor2;
//==================================================================================================================================
// Settings for creating the stepper motor objects for motors 1 and 2
//==================================================================================================================================
ESP_FlexyStepper motor_1_stepper; // create the stepper object for ethanol pump  
ESP_FlexyStepper motor_2_stepper; // create the stepper object for buffer pump 
//==================================================================================================================================
// Settings for microstepping 
//==================================================================================================================================
int micro_stepping_configuration = 64;
int revolution = 200 * micro_stepping_configuration; // nema 11 is 200 steps/rev 
//==================================================================================================================================
// Globals: 
//==================================================================================================================================
const float SPR = 200; // Steps per revolotion nema 11 (might be different for different stepper motors)
const float motor_max_pos = 800;  //[steps]
const float motor_min_pos = -800; //[steps]


// Global variables for delay management if i choose to diable the motors while not active
unsigned long disableMotor1Timer = 0;
unsigned long disableMotor2Timer = 0;
const unsigned long disableDelay = 1000; // Delay in milliseconds
//==================================================================================================================================
// Prototypes: 
//==================================================================================================================================
void serial_handler();
void handle_command(String serial_command);
void home_all_motors(); 
void handle_move_motors(String serial_command);
void handle_pid_motors(String serial_command);
void handle_stop_command(String serial_command);
void enable_stepper_motors();
void disable_all_steppers();
void enable_stepper_motors_discretely(int motorID); 
void disable_stepper_motors_discretely(int motorID);
//==================================================================================================================================
// Setup: 
//==================================================================================================================================
void setup() {
    Serial.begin(115200);
    delay(200); 
    pinMode(MOTOR_1_EN, OUTPUT);
    pinMode(MOTOR_2_EN, OUTPUT);

    pinMode(LS_1, INPUT_PULLUP);
    pinMode(LS_2, INPUT_PULLUP);

    motor_1_stepper.connectToPins(MOTOR_1_STEP, MOTOR_1_DIRECTION); //attach stepper object to stp and dir pins
    digitalWrite(MOTOR_1_EN, HIGH); //tmc2209 is disabled when EN is pulled high 

    motor_2_stepper.connectToPins(MOTOR_2_STEP, MOTOR_2_DIRECTION); // attach stepper object to stp and dir pins
    digitalWrite(MOTOR_2_EN, HIGH); //tmc2209 is disabled when EN is pulled high 

    // Reactivate flags in case they were cleared
    bool waitingForMotor1 = false;
    bool waitingForMotor2 = false;
    
    motor_1_stepper.setAccelerationInStepsPerSecondPerSecond(100); 
    motor_1_stepper.setDecelerationInStepsPerSecondPerSecond(100); 
    motor_2_stepper.setAccelerationInStepsPerSecondPerSecond(100); 
    motor_2_stepper.setDecelerationInStepsPerSecondPerSecond(100); 

    enable_stepper_motors(); 

    cout << "motors about to home" << endl; 

    home_all_motors(); 

    cout << "motors are home" << endl; 



}
//==================================================================================================================================
// Main Event Loop: 
//==================================================================================================================================
void loop() {

  serial_handler(); 

  // Motor 1 processing
  if (waitingForMotor1) {
      //digitalWrite(MOTOR_1_EN, LOW); // Enable Motor 1
      if (!motor_1_stepper.processMovement()) {
          // Movement ongoing
      } else {
          waitingForMotor1 = false; // Movement complete
          //disableMotor1Timer = millis(); // Start timer to disable
      }
  } else if (millis() - disableMotor1Timer > disableDelay) {
      //digitalWrite(MOTOR_1_EN, HIGH); // Disable Motor 1 after delay
  }

  // Motor 2 processing
  if (waitingForMotor2) {
      //digitalWrite(MOTOR_2_EN, LOW); // Enable Motor 2
      if (!motor_2_stepper.processMovement()) {
          // Movement ongoing
      } else {
          waitingForMotor2 = false; // Movement complete
          //disableMotor2Timer = millis(); // Start timer to disable
      }
  } else if (millis() - disableMotor2Timer > disableDelay) {
      //digitalWrite(MOTOR_2_EN, HIGH); // Disable Motor 2 after delay
  }
}

//==================================================================================================================================
// Serial Handler: 
//==================================================================================================================================
void serial_handler() {
  String inString;  // Declare the String to hold the incoming data

  // Read all available serial data, keeping only the last complete command
  while (Serial.available() > 0) {
      inString = Serial.readStringUntil('\n');  // Read the latest complete command
  }

  // Check if a command was received and handle it
  if (inString.length() > 0) {
      handle_command(inString);  // Handle only the last command read
  }
}

//==================================================================================================================================
// Start Stop Handler: 
//==================================================================================================================================
void handle_command(String serial_command){

  char move = serial_command[0]; 
  if(move == 'm'){
    handle_move_motors(serial_command); 
  }
  else if(move == 'o'){
    handle_stop_command(serial_command);
  }
  else if (move == 'j'){
    handle_pid_motors(serial_command); 
  }
}
//==================================================================================================================================
// Home Motors Handler: 
//==================================================================================================================================
void home_all_motors() {
    // Set a slow, safe speed for homing
    motor_1_stepper.setSpeedInStepsPerSecond(900);
    motor_2_stepper.setSpeedInStepsPerSecond(900);

    bool motor1Homed = false;
    bool motor2Homed = false;

    // Continue moving both motors towards home until both are homed
    while (!motor1Homed || !motor2Homed) {
        if (!motor1Homed) {
            if (digitalRead(LS_1) == HIGH) {
                motor_1_stepper.setTargetPositionRelativeInSteps(-100); // Small steps towards home
                motor_1_stepper.processMovement();
            } else {
                motor_1_stepper.setCurrentPositionInSteps(0); // Reset the position to zero at home
                motor1Homed = true;
            }
        }

        if (!motor2Homed) {
            if (digitalRead(LS_2) == HIGH) {
                motor_2_stepper.setTargetPositionRelativeInSteps(-100); // Small steps towards home
                motor_2_stepper.processMovement();
            } else {
                motor_2_stepper.setCurrentPositionInSteps(0); // Reset the position to zero at home
                motor2Homed = true;
            }
        }

        delay(10); // Small delay to reduce speed and give time for mechanical movement
    }

    // Post-homing movement
    if (motor1Homed && motor2Homed) {
        motor_1_stepper.setTargetPositionRelativeInSteps(960);
        motor_2_stepper.setTargetPositionRelativeInSteps(960);

        while (!motor_1_stepper.motionComplete() || !motor_2_stepper.motionComplete()) {
            motor_1_stepper.processMovement();
            motor_2_stepper.processMovement();
        }

        Serial.println("Both motors homed successfully.");
        motor_2_stepper.setCurrentPositionInSteps(0); // Reset the position to zero at home
        motor_1_stepper.setCurrentPositionInSteps(0); // Reset the position to zero at home
    }
}
//==================================================================================================================================
// Move Motors Handler: 
//==================================================================================================================================
void handle_move_motors(String serial_command){
  

  int firstTagIndex = serial_command.indexOf('<');
  int secondTagIndex = serial_command.indexOf('>', firstTagIndex+1);
  int thirdTagIndex = serial_command.indexOf('<', secondTagIndex+1); 
  int fourthTagIndex = serial_command.indexOf('>', thirdTagIndex+1);

  float motor_1_pos_percent = serial_command.substring(firstTagIndex + 1, secondTagIndex).toFloat(); // motor 1 pos
  float motor_2_pos_percent = serial_command.substring(thirdTagIndex + 1, fourthTagIndex).toFloat(); // motor 2 pos 

  float motor_1_pos = motor_max_pos * motor_1_pos_percent;
  float motor_2_pos = motor_max_pos * motor_2_pos_percent; 

  // Clamp values within the allowed range
  motor_1_pos = constrain(motor_1_pos, motor_min_pos, motor_max_pos);
  motor_2_pos = constrain(motor_2_pos, motor_min_pos, motor_max_pos);

  motor_1_stepper.setTargetPositionInSteps(motor_1_pos);
  motor_2_stepper.setTargetPositionInSteps(motor_2_pos);

  // Reactivate flags in case they were cleared
  waitingForMotor1 = true;
  waitingForMotor2 = true;

  cout << motor_1_pos << " " << motor_2_pos << endl; 
}

void handle_pid_motors(String serial_command){


  motor_1_stepper.setAccelerationInStepsPerSecondPerSecond(10000); 
  motor_1_stepper.setDecelerationInStepsPerSecondPerSecond(10000); 
  motor_2_stepper.setAccelerationInStepsPerSecondPerSecond(10000); 
  motor_2_stepper.setDecelerationInStepsPerSecondPerSecond(10000); 

  motor_1_stepper.setSpeedInStepsPerSecond(3000);
  motor_2_stepper.setSpeedInStepsPerSecond(3000);

  int firstTagIndex = serial_command.indexOf('<');
  int secondTagIndex = serial_command.indexOf('>', firstTagIndex+1);
  int thirdTagIndex = serial_command.indexOf('<', secondTagIndex+1); 
  int fourthTagIndex = serial_command.indexOf('>', thirdTagIndex+1);

  float motor_1_pos = serial_command.substring(firstTagIndex + 1, secondTagIndex).toFloat(); // motor 1 pos
  float motor_2_pos = serial_command.substring(thirdTagIndex + 1, fourthTagIndex).toFloat(); // motor 2 pos 


  // Clamp values within the allowed range
  motor_1_pos = constrain(motor_1_pos, motor_min_pos, motor_max_pos);
  motor_2_pos = constrain(motor_2_pos, motor_min_pos, motor_max_pos);

  motor_1_stepper.setTargetPositionInSteps(motor_1_pos);
  motor_2_stepper.setTargetPositionInSteps(motor_2_pos);

  // Reactivate flags in case they were cleared
  waitingForMotor1 = true;
  waitingForMotor2 = true;

}


//==================================================================================================================================
// Stop Motors Handler: 
//==================================================================================================================================
void handle_stop_command(String serial_command){
  disable_all_steppers(); 
}
//==================================================================================================================================
// Enable steppers: 
//==================================================================================================================================
void enable_stepper_motors()
{
  digitalWrite(MOTOR_1_EN, LOW);
  digitalWrite(MOTOR_2_EN, LOW);
}
//==================================================================================================================================
// Disable steppers nonselectly: 
//==================================================================================================================================
void disable_all_steppers()
{
  digitalWrite(MOTOR_1_EN, HIGH);
  digitalWrite(MOTOR_2_EN, HIGH);
}

void enable_stepper_motors_discretely(int motorID) {
  if (motorID == 1) {
    digitalWrite(MOTOR_1_EN, LOW); // Enable only the first motor
  } else if (motorID == 2) {
    digitalWrite(MOTOR_2_EN, LOW); // Enable only the second motor
  }
}

void disable_stepper_motors_discretely(int motorID) {
  if (motorID == 1) {
    digitalWrite(MOTOR_1_EN, HIGH); // Disable only the first motor
  } else if (motorID == 2) {
    digitalWrite(MOTOR_2_EN, HIGH); // Disable only the second motor
  }
}

