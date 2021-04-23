// RP LIDAR V0.6 - Michael Fuell - Senior Design Spring 2021
//Team: Electric Boogaloo
//---------------------------------------------------------------------
// - Libraries - 
#include <Arduino.h>
#include <SD.h>
#include <Wire.h>
#include <Adafruit_BNO055.h>
#include <RPLidar.h>
#include <EEPROM.h>
//---------------------------------------------------------------------
// - Definitions - 
#define RPLIDAR_MOTOR 22 // The PWM pin for control the speed of RPLIDAR's motor. //MotoCtrl
#define RGB_RED 2
#define RGB_GRN 3
#define RGB_BLU 4
#define PSH_BTN 6
#define EPR_ADR 10
#define CS_PIN  10
#define BTN_PIN 5
#define DET_PIN 9
#define EPR_RD EEPROM.read(EPR_ADR)
//---------------------------------------------------------------------
// - Global Variables and Objects -
RPLidar lidar;
Adafruit_BNO055 bno1 = Adafruit_BNO055(55, 0x28);
File dataFile;
String fileName = ("data_"+String(EPR_RD)+".txt");
const int strLen = (fileName.length()+1);
char charFileName[12];
int Clicks = 0;
boolean readyToMoveOn = false;
bool beenPressed = false;

//---------------------------------------------------------------------
//---------------------------------------------------------------------
boolean isAllNumeric(String str){
  int strLen = str.length();
  if(strLen <= 0){
    return false;
  }
  for(int i=0;i<strLen;i++){
    if(isDigit(str.charAt(i))){
      continue;
    }
    else if((str.charAt(0) == '-') && (i==0)){
      continue;
    }
    else{
      return false;
    }
  }
  return true;
}
//---------------------------------------------------------------------
//---------------------------------------------------------------------
void serialEvent(){
  if(!Serial.available()){
    return;
  }
  String tempSerial = "";
  char incommingByte = '\0';
  while(Serial.available()){
    incommingByte = char(Serial.read());
    if(incommingByte == '\n'){
      break;
    }
    else{
      tempSerial = tempSerial + incommingByte;
    }
  }
  if(tempSerial == "Module?"){
      Serial.print("LMM\n");
      readyToMoveOn = true;
  }
  else if(isAllNumeric(tempSerial)){
    Clicks = tempSerial.toInt();
  }
  else{
  }
  
}
void buttonPress(){
  static unsigned long prev_time = 0;
  static unsigned long this_time = 0;
  this_time = millis();
  if(this_time-prev_time > 200){
    if(!beenPressed){
      beenPressed = true;
    }
  }
  prev_time = this_time;
}
//---------------------------------------------------------------------
//---------------------------------------------------------------------
void setup() {
  pinMode(RPLIDAR_MOTOR, OUTPUT);
  pinMode(RGB_RED, OUTPUT);
  pinMode(RGB_GRN, OUTPUT);
  pinMode(RGB_BLU, OUTPUT);
  pinMode(PSH_BTN, INPUT);
  pinMode(DET_PIN, INPUT);
  pinMode(BTN_PIN, INPUT_PULLUP);
  pinMode(10, OUTPUT);
  digitalWrite(10, HIGH);
  
  attachInterrupt(digitalPinToInterrupt(BTN_PIN), buttonPress, RISING);
  fileName.toCharArray(charFileName, strLen);
  digitalWrite(RGB_BLU, HIGH); //Blue
  Serial.begin(115200);  
  while(!Serial){
    delay(10);
    if(beenPressed){
      break;
    }
  }
  digitalWrite(RGB_RED, HIGH); //Purple
  while(!readyToMoveOn){
    serialEvent();
    delay(10);
    if(beenPressed){
      break;
    }
  }
  digitalWrite(RGB_BLU, LOW); //Red
  while(!lidar.begin(Serial4));
  digitalWrite(RGB_GRN, HIGH); //Yellow
  while(!bno1.begin());
  digitalWrite(RGB_RED, LOW);  //
  digitalWrite(RGB_BLU, HIGH); //Cyan
  bool sdc = false;
  while(!sdc){
    while(!digitalRead(DET_PIN)){
      digitalWrite(RGB_GRN, LOW); //Blue
      delay(500);
      digitalWrite(RGB_GRN, HIGH); //Cyan
      delay(500);
    }
    sdc = SD.begin(CS_PIN);
  }
  digitalWrite(RGB_RED,HIGH); //
  digitalWrite(RGB_BLU, LOW); //Yellow
  uint8_t system, gyro, accel, mag = 0;
  while(gyro != 3){
    bno1.getCalibration(&system, &gyro, &accel, &mag);
    digitalWrite(RGB_GRN, LOW); //Red
    delay(500);
    digitalWrite(RGB_GRN, HIGH);//Yellow
    delay(500);
  }
  digitalWrite(RGB_RED, LOW);
  EEPROM.write(EPR_ADR, EPR_RD+1);
  dataFile = SD.open(charFileName, FILE_WRITE);
  dataFile.println("Time,Heading,Clicks,Azimuth,Distance,Quality");
}
//---------------------------------------------------------------------
//---------------------------------------------------------------------
void loop() {
  //Version 0.6.1
  static float lidarData[3][360] = {0};
  static float TimeData[2][360] = {0};
  static long sysTime = 0;
  static long delayTime = 0;
  static int r = 0;
  static int c = 0;
  static float angle = 0;
  static int quality = 0;
  static int i = 0;
  static int writes = 0;
  static sensors_event_t orientationData1;
  static RPLidarMeasurement CurrPoint;
  if(!digitalRead(DET_PIN)){
    analogWrite(RPLIDAR_MOTOR, 0);
    lidar.stop();
    while(!digitalRead(DET_PIN)){
      digitalWrite(RGB_BLU, HIGH);
      delay(500);
      digitalWrite(RGB_BLU, LOW);
      delay(500);
    }
    dataFile = SD.open(charFileName, FILE_WRITE);
  }
  else if(!dataFile){
    dataFile = SD.open(charFileName, FILE_WRITE);
  }
  if(Serial.available()){
    serialEvent();
  }
  sysTime = micros();                                             //get system time in microseconds
  if( (IS_OK(lidar.waitPoint())) && (sysTime>=delayTime) ){ //check for lidar, and get point
    CurrPoint = lidar.getCurrentPoint();
    angle = CurrPoint.angle;                        //angle value in degrees
    quality = CurrPoint.quality;
    if(angle<360 && 14<quality && writes<360){
      lidarData[0][writes] = CurrPoint.angle;       // float
      lidarData[1][writes] = CurrPoint.distance;    // float
      lidarData[2][writes] = CurrPoint.quality;     // Byte
      TimeData[0][writes] = sysTime;
      if(writes%5 == 0){
        bno1.getEvent(&orientationData1);
      }
      TimeData[1][writes] = (orientationData1.orientation.x);
      writes++;     //incriment writes to array
    }
  } 
  else if(sysTime>=delayTime){                        // try to detect RPLIDAR... 
    rplidar_response_device_info_t info;
    
    if (IS_OK(lidar.getDeviceInfo(info, 100))) {
       lidar.startScan();                       // detected...
       analogWrite(RPLIDAR_MOTOR, 255);         // start motor rotating at max allowed speed
       delayTime = micros()+1500000;            //set time for lidar start, so that there can be a delay before read in
    }
  }// end of if - else for reading and starting LIDAR
  if(writes>359){                              //Write Data
    if(dataFile){
      for(i=0;i<360;i++){
        dataFile.println(String(TimeData[0][i])+","+String(TimeData[1][i])+","+String(Clicks)+","+String(lidarData[0][i])+","+String(lidarData[1][i])+","+String(lidarData[2][i]));
      }
      dataFile.close();
    }
    
    for(r=0;r<3;r++){ //Zero out lidar arrays
      for(c=0;c<360;c++){
        lidarData[r][c] = 0;
      }
    }
    for(r=0;r<2;r++){ //Zero out lidar arrays
      for(c=0;c<360;c++){
        TimeData[r][c] = 0;
      }
    }
    writes = 0;
  }   //End Serial Data If - Statment*/

  //Everyting past here is a diferent version
  
  /*//Version 0.5
  static float lidarData[3][360] = {0};
  static float TimeData[2][360] = {0};
  static long sysTime = 0;
  static long delayTime = 0;
  static int r = 0;
  static int c = 0;
  static float angle = 0;
  static int angleRound = 0;
  static int i = 0;
  static int writes = 0;
  static sensors_event_t orientationData1;
  static RPLidarMeasurement CurrPoint;
  if(!digitalRead(DET_PIN)){
    analogWrite(RPLIDAR_MOTOR, 0);
    lidar.stop();
    while(!digitalRead(DET_PIN)){
      digitalWrite(RGB_BLU, HIGH);
      delay(500);
      digitalWrite(RGB_BLU, LOW);
      delay(500);
    }
    dataFile = SD.open(charFileName, FILE_WRITE);
  }
  else if(!dataFile){
    dataFile = SD.open(charFileName, FILE_WRITE);
  }
  if(Serial.available()){
    serialEvent();
  }
  sysTime = micros();                                             //get system time in microseconds
  if( (IS_OK(lidar.waitPoint())) && (sysTime>=delayTime) ){ //check for lidar, and get point
    CurrPoint = lidar.getCurrentPoint();
    angle = CurrPoint.angle;                        //angle value in degrees
    if(angle<360){
      angleRound = round(angle)%360;                                //make sure the index dosent exceed 359
      lidarData[0][angleRound] = CurrPoint.angle;       // float
      lidarData[1][angleRound] = CurrPoint.distance;    // float
      lidarData[2][angleRound] = CurrPoint.quality;     // Byte
      TimeData[0][angleRound] = sysTime;
      if(writes%4 == 0){ //%8&4 is clean with one BNO055
        bno1.getEvent(&orientationData1);
      }
      TimeData[1][angleRound] = (orientationData1.orientation.x);
      writes++;     //incriment writes to array
    }
  } 
  else if(sysTime>=delayTime){                        // try to detect RPLIDAR... 
    rplidar_response_device_info_t info;
    rplidar_response_device_health_t health;
    
    if (IS_OK(lidar.getDeviceInfo(info, 100))) {
       lidar.startScan();                       // detected...
       analogWrite(RPLIDAR_MOTOR, 255);         // start motor rotating at max allowed speed
       delayTime = micros()+1500000;            //set time for lidar start, so that there can be a delay before read in
    }
  }// end of if - else for reading and starting LIDAR
  if(writes>360){                              //Write Data
    if(dataFile){
      for(i=0;i<360;i++){
        dataFile.println(String(TimeData[0][i])+","+String(TimeData[1][i])+","+String(Clicks)+","+String(lidarData[0][i])+","+String(lidarData[1][i])+","+String(lidarData[2][i]));
      }
      dataFile.close();
    }
    
    for(r=0;r<3;r++){ //Zero out lidar arrays
      for(c=0;c<360;c++){
        lidarData[r][c] = 0;
      }
    }
    for(r=0;r<2;r++){ //Zero out lidar arrays
      for(c=0;c<360;c++){
        TimeData[r][c] = 0;
      }
    }
    writes = 0;
  }   //End Serial Data If - Statment*/
} //end of for loop
