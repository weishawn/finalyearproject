const int emergencystopbuttonPin = 2;
const int lampPin =  8;
const int panelPin = 12;

int emergencystopbuttonState = 0;
int lastemergencystopbuttonState = 0;
int on = 0;
int lamp = 1;
int panel = 0;

int stop = 0;

#define d_limitto1 200 //steps between limit switch and 1st cell
#define d_1to2 1000     //steps between the cells
#define Dir 3
#define Step 4
#define Enable 5
#define Limit_1 6
#define Limit_2 7
int pos = 0;
bool initial = true;
bool initialISR = true;
int x = 0;



void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  pinMode(lampPin, OUTPUT);
  pinMode(panelPin, OUTPUT);
  pinMode(emergencystopbuttonPin, INPUT);

  pinMode(Dir,OUTPUT);
  pinMode(Step,OUTPUT);
  pinMode(Enable,OUTPUT);
  digitalWrite(Enable,HIGH);
  pinMode(Limit_1,INPUT);
  pinMode(Limit_2,INPUT); 
  
  Serial.flush();

  attachInterrupt(digitalPinToInterrupt(emergencystopbuttonPin), emergencystop, RISING);
  //attachInterrupt(digitalPinToInterrupt(Limit_1), emergencystop, RISING);
  //attachInterrupt(digitalPinToInterrupt(Limit_2), emergencystop, RISING);
}

//ISR
void emergencystop(){
  static unsigned long last_interrupt_time = 0;
  unsigned long interrupt_time = millis();
  if (interrupt_time - last_interrupt_time > 2000) 
  {
    stop = 1;
    digitalWrite(lampPin, LOW);
    digitalWrite(panelPin, LOW);
    if (initialISR){
      initialISR = 0;
      Serial.println(8);
      Serial.println(8);
    }
    else{
      //Serial.write(7);
      Serial.println(7);
      Serial.flush();
    }
  }
  last_interrupt_time = interrupt_time;
}

void runMotor(int wait, int steps, boolean dir){
  
  digitalWrite(Enable,LOW);
  digitalWrite(Dir,dir);
  
  pos = pos + steps;
  for(int i=0;i<(steps);i++){
    if(stop){
    digitalWrite(Enable,HIGH);
    stop = 0;
    return;
    }
    digitalWrite(Step,HIGH);
    delayMicroseconds(wait);
    digitalWrite(Step,LOW);
    delayMicroseconds(wait);
  }

  if(pos>800){
    digitalWrite(Enable,HIGH);
  }
}
  
void homing(boolean enable){
  runMotor(1000,pos,false);
  pos = 0;
  digitalWrite(Enable,HIGH);
}

void calibration(){
  digitalWrite(Enable,LOW);
  digitalWrite(Dir,false);
  for(int i=0;i<(100000);i++){
    if(stop){
      delay(200);
      digitalWrite(Enable,HIGH);
      stop = 0;
      runMotor(1000,d_limitto1,true);
      digitalWrite(Enable,HIGH);
      pos = 0;
      return;
    }
    digitalWrite(Step,HIGH);
    delayMicroseconds(1000);
    digitalWrite(Step,LOW);
    delayMicroseconds(1000);
  }
}

void loop(){
  
  if(Serial.available()>0){
    x = Serial.readString().toInt();}


  
  /*emergencystopbuttonState = digitalRead(emergencystopbuttonPin);
  if(emergencystopbuttonState==1 && lastemergencystopbuttonState == 0){
    digitalWrite(lampPin, LOW);
    digitalWrite(panelPin, LOW);
    //add here part to send python a signal to stop the program
    Serial.write(7);
   //
  }
  lastemergencystopbuttonState = emergencystopbuttonState;*/

  //HOMING
  if (x==1){
    x=0;
    if(initial){
      calibration();
      initial = 0;
    }
    else{
      homing(true);}
      
    delay(1000);
    //Serial.write(1);
    Serial.println(1);
    Serial.flush();
  }
  
 
  //MOVE
  if (x==2){
    x=0;
    runMotor(1000,d_1to2,true);
    delay(1000);
    //Serial.write(1);
    Serial.println(1);
    Serial.flush();
  }
  
//   if (x==3){
//    x = 0;
//    delay(5000);
//    Serial.write(1);
//  }
  
  //PL
  if (x==4){
    x= 0;
    //Serial.println("PL mode from arduino");
    digitalWrite(lampPin, HIGH);
    digitalWrite(panelPin, LOW);
    delay(500);
    //Serial.write(2);
    Serial.println(2);
    Serial.flush();
  }
 
  //EL
  if (x==5){
    x= 0;
    //Serial.println("EL mode from arduino");
    digitalWrite(lampPin, LOW);
    digitalWrite(panelPin, HIGH);
    delay(500);
    //Serial.write(2);
    Serial.println(2);
    Serial.flush();
  }
  
  //OFF
  if (x==6){
    x= 0;
    digitalWrite(lampPin, LOW);
    digitalWrite(panelPin, LOW);
    delay(500);
    //Serial.write(3);
    Serial.println(3);
    Serial.flush();
    
  }
  
  if (x==7){
    stop = 0;
    initial = true;
    initialISR = true;
  }
}





  
