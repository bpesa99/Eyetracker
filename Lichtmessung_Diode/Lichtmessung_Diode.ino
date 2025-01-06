double spannungmessen();
void zeitmessung(bool status, long zeit);
void maximum(double a);

double schwarz = 0.0; //max in mV
bool state = true;
int start = 0;
int anzahlmessungen = 500;
long timediff = 0;
long oldtime = 0;
long addtime = 0;
int wait = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  if(start == 0){
    for(int i = 0; i < anzahlmessungen; i++){
      maximum(spannungmessen());
    }
    delay(1000);
    Serial.println(1);
    start = 1;
  }
  else if(start == 1){
    long time = micros();
    double voltage = spannungmessen(); 
    if(voltage > schwarz+2 && state == true){
      zeitmessung(false, time);
    }
    else if(voltage < schwarz && state == false){
      zeitmessung(true, time);
    }
  }
}

double spannungmessen(){
  long sensorValue = 0;
  const int n = 10;
  for ( int i = 0; i < n; i++){
    sensorValue += analogRead(A0);
  }
  return (sensorValue/n) * (5000.0/1023.0); //sensorValue hat Werte von 0 bis 1023 und wird hier zu 0V bis 5000000uV umgewandelt
}

void zeitmessung(bool status, long zeit){
  state = status;
  timediff = zeit - oldtime;
  oldtime = zeit;
  if(timediff/1000 < 100){
    addtime += timediff;
  }
  else{
    timediff += addtime;
    addtime = 0;
    delay(1000);
    Serial.println(timediff/1000); 
  }
}

void maximum(double a){
  if(a > schwarz){
    schwarz = a;
  }  
}