void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT); //ADC 0, connect to sensor input

  Serial.begin(9600);
  
}


int senseIn = 0;
void loop() {
  // put your main code here, to run repeatedly:

  senseIn = analogRead(A0) ;

  Serial.println(senseIn);
  delay(500);
}
