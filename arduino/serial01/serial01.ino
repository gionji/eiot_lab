
void setup() {
  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop() {
  char readedByte = '0';
  
  while(Serial.available() > 0){
    readedByte = (char) Serial.read(); 
    if(readedByte == '0') 
      digitalWrite(13, LOW);
    else if(readedByte == '1')
      digitalWrite(13, HIGH);
  }

  delay(100);
}

