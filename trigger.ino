// Sets an IO pin high or low based on the 'coolant' output from klipper
// Define the input and output pins
const int inputPin = A0;
const int outputPin = 12;

// Define the threshold value for high and low
const int threshold = 512;

void setup() {
  // Initialize the output pin as an output
  pinMode(outputPin, OUTPUT);
}

void loop() {
  // Read the analog value from the PWM input pin
  int inputValue = analogRead(inputPin);

  // Set the output pin based on the threshold
  if (inputValue >= threshold) {
    digitalWrite(outputPin, HIGH);
  } else {
    digitalWrite(outputPin, LOW);
  }

  // Small delay for stability
  delay(10);
}
