
float schwarz = 1.93;
float weiss = schwarz+0.01;
bool state = true;

int start = 0;
float mittelwert_v = 0.0;
int anzahlmessungen = 1000;

volatile unsigned long timediff = 0;
unsigned long oldtime = 0;
unsigned long addtime = 0;


void setup() {
  Serial.begin(115200);
}

void loop() {
  if(start < anzahlmessungen){
    float voltage = spannungmessen();
    mittelwert_v += voltage;
    start += 1;
  }
  else if(start == anzahlmessungen){
    schwarz = mittelwert_v/anzahlmessungen;
    start += 1;
    delay(1000);
    Serial.println(1);
  }
  else if(start > anzahlmessungen){
    unsigned long time = micros();
    float voltage = spannungmessen(); 
    if(voltage >= weiss && state == true){
      zeitmessung(false, time);
    }
    else if(voltage <= schwarz && state == false){
      zeitmessung(true, time);
    }
  }
}

float spannungmessen(){
  int sensorValue = analogRead(A0);
  return sensorValue * (5.0/1023.0); //sensorValue hat Werte von 0 bis 1023 und wird hier zu 0V bis 5V umgewandelt
}

void zeitmessung(bool status, long zeit){
  state = status;
  timediff = zeit - oldtime;
  oldtime = zeit;
  if(timediff < 400000){
    addtime += timediff;
  }
  else{
    timediff += addtime;
    addtime = 0;
    Serial.println(timediff);
  }
}
