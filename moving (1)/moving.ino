#define Dir 3
#define Step 4
#define Enable 5
#define Limit_1 6
#define Limit_2 7
int pos = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(Dir,OUTPUT);
  pinMode(Step,OUTPUT);
  pinMode(Enable,OUTPUT);
  pinMode(Limit_1,INPUT);
  pinMode(Limit_2,INPUT);  
}

void loop() {
  // put your main code here, to run repeatedly:
  moving(false); //false for CCW
}

void moving(boolean dir){ 
  runMotorSingleStep(1000,dir);
  pos = pos + 2;
  //if(digitalRead(Limit_1) == false){ // stops when it is in contact with the limit switch
   //   digitalWrite(Enable,HIGH);
  //}
  
  //if(digitalRead(Limit_2) == false){ //  stops when it is in contact with the limit switch
     /// digitalWrite(Enable,HIGH);
  //}
  
  if (pos > 2000){ //if the camera reaches certain point, it stops (to capture images)
    digitalWrite(Enable,HIGH);
  }

}

void runMotorSingleStep(int wait, boolean dir){
  digitalWrite(Dir,dir);
  digitalWrite(Step,HIGH);
  delayMicroseconds(wait);
  digitalWrite(Step,LOW);
  delayMicroseconds(wait);
}
