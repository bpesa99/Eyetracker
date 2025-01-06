double spannungmessen();

void setup() {
  Serial.begin(115200);
}

void loop() {
  long spannung = spannungmessen();
  Serial.println(spannung);
}

double spannungmessen(){
  double sensorValue = 0;
  const int n = 10;
  for ( int i = 0; i < n; i++){
    sensorValue += analogRead(A0);
  }
  return (sensorValue/n) * (5000.0/1023.0);
}