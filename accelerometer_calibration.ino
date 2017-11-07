/**
 * Target-Tek (BYU Capstone Team 19) Accelerometer Calibration Prototype Code
 * Our accelerometer needs to be calibrated! We're going to do that by sticking it on
 * a rotating platform, and taking a number of readings equally spaced around a circle.
 * Averaging those readings together will allow us to establish a good normal vector.
 */

#include <Stepper.h> // Stepper motor library.

#define ERROR_TOLERANCE 20 // Leeway in the accelerometer reading. Accelerometer outputs are from 0 to 1023.
#define ACCELEROMOTER_ZERO 512 // 0g is in the middle of the accelerometer's +-3g range.
#define NUMBER_OF_READINGS 8 // Take 8 readings at 45 degree increments.
#define SETTLING_TIME_DELAY 1000 // Wait 200 ms after arriving at a position before taking a reading.
#define STEPS_PER_FULL_ROTATION 200 // This stepper motor has 200 steps per full rotation- one step is 1.8 degrees.
#define STEPS_PER_READING (STEPS_PER_FULL_ROTATION / NUMBER_OF_READINGS) // 200 steps per full revolution, divided into equal parts.
#define RPM 60 // Stepper motor revolutions per minute.

uint16_t x, y, z, x_golden, y_golden, z_golden; // Declare x, y, and z variables, and calibrated averages x,y,z_golden.
uint16_t count; // Number of readings we've taken so far.
uint16_t x_readings[NUMBER_OF_READINGS], y_readings[NUMBER_OF_READINGS], z_readings[NUMBER_OF_READINGS]; // Declare arrays to hold readings to be averaged.

Stepper stepper_motor(STEPS_PER_FULL_ROTATION, 8, 9, 10, 11); // Initialize stepper motor on PWM pins 6, 9, 10, and 11.

enum state_t {init_st, read_st, rotate_st, math_st, final_st} state;

uint16_t average(uint16_t *val){ // Use like: average(x_readings)
  // Averages our NUMBER_OF_READINGS readings into one.
  uint16_t avg = 0; // Initialize average variable.
  for(uint16_t i=0; i<NUMBER_OF_READINGS; ++i)
    avg += val[i]; // Add together all the readings.
  avg /= NUMBER_OF_READINGS; // Divide by the number of readings.
  return avg;
}

void setup() {
  stepper_motor.setSpeed(RPM); // Initialize motor at 60 RPM.
  analogReference(EXTERNAL); // Uses the accelerometer's reference output.
  pinMode(A0, INPUT); // Initialize X pin.
  pinMode(A1, INPUT); // Initialize Y pin.
  pinMode(A2, INPUT); // Initialize Z pin.
  pinMode(LED_BUILTIN, OUTPUT); // Initialize LED.
}

void loop() {
  // Moore actions.
  switch(state){
    case init_st:
      count = 0; // Set count to zero; we've taken zero readings so far.
      break;
    case read_st:
      delay(SETTLING_TIME_DELAY); // Delay so things mechanically settle before taking a reading.
      // Take reading.
      x_readings[count] = analogRead(A0);
      y_readings[count] = analogRead(A1);
      z_readings[count] = analogRead(A2);
      ++count; // Increment count; we've taken another reading.
      delay(SETTLING_TIME_DELAY); // Delay again. Just in case.
      break;
    case rotate_st:
      // Stepper datasheet: http://www.ni.com/datasheet/pdf/en/ds-311
      stepper_motor.step(STEPS_PER_READING); // Rotate 360 / NUMBER_OF_READINGS degrees.
      delay(SETTLING_TIME_DELAY); // Delay so it actually rotates ????????????????????????????????????????????????
      break;
    case math_st:
      // Compute averages of our readings to calibrate the accelerometer.
      x_golden = average(x_readings);
      y_golden = average(y_readings);
      z_golden = average(z_readings);
      break;
    case final_st:
      // Read accelerometer data.
      x = analogRead(A0);
      y = analogRead(A1);
      z = analogRead(A2);  
      if(abs(x-x_golden)<ERROR_TOLERANCE && abs(y-y_golden)<ERROR_TOLERANCE) // If you're close to level...
        digitalWrite(LED_BUILTIN, HIGH); // ...turn on LED.      
      else
        digitalWrite(LED_BUILTIN, LOW); // If not level, turn off LED.      
      break;
  }
  // Mealy actions and transitions.
  switch(state){
    case init_st:
      state = read_st; // Go take a reading.
      break;
    case read_st:
      if(count < NUMBER_OF_READINGS) // If we're not done taking readings...
        state = rotate_st; // ...rotate and go take another one.
      else // If we are done taking readings...
        state = math_st; // ...go to our demonstration mode.
      break;
    case rotate_st:
      state = read_st; // Take another reading.
      break;
    case math_st:
      state = final_st; // Transition to final demonstration state.
      break;
    case final_st:
      // Do nothing.
      break;
  }

}
