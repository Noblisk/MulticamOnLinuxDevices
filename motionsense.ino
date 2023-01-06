void setup() {
  // Set the four digital ports as inputs
  pinMode(1, INPUT);
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
}

int counter = 0; // Declare and initialize the counter variable
String out = ""; // Placeholder for cameras 

void loop() {

  // Read the values of the four digital ports
  int port1 = digitalRead(0);
  int port2 = digitalRead(1);
  int port3 = digitalRead(2);
  int port4 = digitalRead(3);

  
  // If there is a signal on port 1, print "cam1"
  if (port1 == HIGH) {
    out += "cam1";
    // delay(300); // Add a delay of 300 milliseconds
  }

  // If there is a signal on port 2, print "cam2"
  if (port2 == HIGH) {
    out += "cam2";
    // delay(300); // Add a delay of 300 milliseconds
  }

  // If there is a signal on port 3, print "cam3"
  if (port3 == HIGH) {
    out += "cam3";
    // delay(300); // Add a delay of 300 milliseconds
  }

  // If there is a signal on port 4, print "cam4"
  if (port4 == HIGH) {
    out += "cam4";
    // delay(300); // Add a delay of 300 milliseconds
  }

  Serial.println(out)
  out = ""

  // If there is no signal on any of the ports, stop printing output
  if (port1 == LOW && port2 == LOW && port3 == LOW && port4 == LOW) {
    counter++; // Increment the counter
    Serial.println("No signal on any port. Counter: " + String(counter));
    // delay(300);
    return;
  }
}
