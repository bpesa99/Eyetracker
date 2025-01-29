double spannungmessen();
void maximum(double a);

double schwarz = 0.0; //max in mV
bool state = true; //ist das Bild schwarz (false), oder weiß (true)
int start = 0;
int anzahlmessungen = 500;

void setup() {
  Serial.begin(115200);
}

void loop() {
  if(start == 0){
    for(int i = 0; i < anzahlmessungen; i++){  
      maximum(spannungmessen()); //Bestimmen des maximalen Spannungswerts für Schwarz
    }
    delay(10000);
    Serial.println(1);
    start = 1;
  }
  else if(start == 1){
    double voltage = spannungmessen(); 
    if(voltage > schwarz+2 && state == true){
      state = false;
      Serial.println(1);
    }
    else if(voltage < schwarz && state == false){
      state = true;
      Serial.println(1);
    }
  }
}

double spannungmessen(){
  long sensorValue = 0;
  const int n = 10; 
  for ( int i = 0; i < n; i++){
    sensorValue += analogRead(A0); //Spannungswerte werden gemittelt, da es sonst zu false positives kommt
  }
  return (sensorValue/n) * (5000.0/1023.0); //sensorValue hat Werte von 0 bis 1023 und wird hier zu 0V bis 5000mV umgewandelt
}

void maximum(double a){
  if(a > schwarz){
    schwarz = a;
  }  
}