const int emergencystopbuttonPin = 2;
const int lampPin =  8;
const int panelPin = 12;

int emergencystopbuttonState = 0;
int lastemergencystopbuttonState = 0;
int on = 0;
int lamp = 1;
int panel = 0;


#define Dir 3
#define Step 4
#define Enable 5
#define Limit_1 6
#define Limit_2 7
int pos = 0;
bool initial = true;
int x = 0;

//ISR
void calibration(){
    //varies deending on the distance between limit switch and first cell
    runMotor(1000,200,true);
    initial=false;
}


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  pinMode(lampPin, OUTPUT);
  pinMode(panelPin, OUTPUT);
  pinMode(emergencystopbuttonPin, INPUT);

  pinMode(Dir,OUTPUT);
  pinMode(Step,OUTPUT);
  pinMode(Enable,OUTPUT);
  pinMode(Limit_1,INPUT);
  pinMode(Limit_2,INPUT); 

  attachInterrupt(digitalPinToInterrupt(emergencystopbuttonPin), calibration, CHANGE);
  
}

void runMotor(int wait, int steps, boolean dir){
  digitalWrite(Enable,LOW);
  digitalWrite(Dir,dir);
  
  pos = pos + steps;
  for(int i=0;i<(steps);i++){
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

void loop(){
  
  if(Serial.available()>0){
    x = Serial.readString().toInt();}


  
  emergencystopbuttonState = digitalRead(emergencystopbuttonPin);
  if(emergencystopbuttonState==1 && lastemergencystopbuttonState == 0){
    digitalWrite(lampPin, LOW);
    digitalWrite(panelPin, LOW);
    //add here part to send python a signal to stop the program
    Serial.write(7);
   //
  }
  lastemergencystopbuttonState = emergencystopbuttonState;

  if (x==1){
    x=0;
    if(initial){
      
      runMotor(1000,10000,false);
    }
    else{
      homing(true);}
      
    delay(1000);
    Serial.write(1);
  }
  
 
  
  if (x==2){
    x=0;
    runMotor(1000,1000,true);
    delay(1000);
    Serial.write(1);
  }
  
//   if (x==3){
//    x = 0;
//    delay(5000);
//    Serial.write(1);
//  }
  
  if (x==4){
    x= 0;
    //Serial.println("PL mode from arduino");
    digitalWrite(lampPin, HIGH);
    digitalWrite(panelPin, LOW);
    delay(500);
    Serial.write(2);
    //delay(500);
  }
 
  if (x==5){
    x= 0;
    //Serial.println("EL mode from arduino");
    digitalWrite(lampPin, LOW);
    digitalWrite(panelPin, HIGH);
    Serial.write(2);
  }

    if (x==6){
    x= 0;
    digitalWrite(lampPin, LOW);
    digitalWrite(panelPin, LOW);
    delay(1000);
    Serial.write(3);
    
  }
}


  
