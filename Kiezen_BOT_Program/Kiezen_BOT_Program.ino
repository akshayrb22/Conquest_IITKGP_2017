/*
 * Program : Motor Test
 * This program will test the motor which is connected
 * to the arduino.
 *
 * created by : DREAMERS
 * build      : 07/14/2015
 *
 * If you are having any issue related to this program
 * please contact your mentor.
 * If your mentor is missing or mentor is unreachable
 * then please poke the person giving presentation.
 *
 * WARNING:
 * PLEASE DO NOT BURN THE ARDUINO PROVIDED TO YOU.
 * PLEASE DO NOT SPOIL THE ARDUINO PROVIDED TO YOU.
 * PLEASE DO NOT DAMAGE THE ARDUINO PROVIDED TO YOU.
 * PLEASE LISTEN TO THE INSTRUCTIONS VERY CAREFULLY.
 * YOU MIGHT HAVE 6 PACK WITH MUSCULAR BODY, BUT PLEASE HANDLE
 * THE ARDUINO CABLE CORDS WITH CARE.
 *
 * PLEASE FOLLOW AND OBEY THE TRAFFIC RULES.
 * PLEASE DO NOT DRINK AND DRIVE YOUR ROBOT :P
 */

/*
 * include the header files needed for the program.
 */
#include <Arduino.h>
#include <Wire.h>      // these are actually not needed.
#include <Servo.h>     // these are actually not needed.
#include <SoftwareSerial.h>
#define RxD 2 // Pin that the Bluetooth (BT_TX) will transmit to the Arduino (RxD)
#define TxD 3 //
//#include "pingTest.h"
SoftwareSerial blueToothSerial(RxD,TxD);
double angle_rad = PI/180.0;  // 1 degree in radians.
double angle_deg = 180.0/PI;  // 1 radian in degree.
 int AUTO_FLAG = 0;
/*
 * These values are used to set the speed of the bot.
 */
int speed_slow = 50;
int speed_medium = 150;
int speed_fast = 255;

int var = 50;
/*
 * These are the functions which are required to
 * control the bot.
 *
 * PLEASE MAKE SURE YOU HAVE A "DRIVING LICENCE" before driving.
 */
void moveForward();
void Stop();
void moveBackward();
void arcRight();
void arcLeft();
void spotRight();
void spotLeft();

void checkAUTO_FLAG();

double Distance;    // Distance of the obstacle, this will be given by ping.
//Mdouble AUTO_FLAG;   // To check whether the bot is controlled by you or autonomous.
int leftA = 9;
int leftB = 10;
int rightA = 7;
int rightB = 8;

void moveForward()
{
    digitalWrite(leftA,1);

    digitalWrite(leftB,0);

    digitalWrite(rightA,1);

    digitalWrite(rightB,0);
    Serial.println("Forward");
}
void setupBlueToothConnection()
{
 blueToothSerial.begin(9600); //Set BluetoothBee BaudRate to default baud rate 38400
 blueToothSerial.print("\r\n+STWMOD=0\r\n"); //set the bluetooth work in slave mode
 blueToothSerial.print("\r\n+STNA=SeeedBTSlave\r\n"); //set bluetooth name as "SeeedBTSlave"
 blueToothSerial.print("\r\n+STOAUT=1\r\n"); // Permit Paired device to connect me
 blueToothSerial.print("\r\n+STAUTO=0\r\n"); // Auto-connection should be forbidden here
 delay(2000); // This delay is required.
 blueToothSerial.print("\r\n+INQ=1\r\n"); //make the slave bluetooth inquirable 
 Serial.println("The slave bluetooth is inquirable!");
 delay(2000); // This delay is required.
 blueToothSerial.flush();
}
void Stop()
{
    digitalWrite(leftA,0);

    digitalWrite(leftB,0);

    digitalWrite(rightA,0);

    digitalWrite(rightB,0);
    Serial.println("Stop");
}

void moveBackward()
{
    digitalWrite(leftA,0);

    digitalWrite(leftB,1);

    digitalWrite(rightA,0);

    digitalWrite(rightB,1);
    Serial.println("Backward");
}

void arcRight()
{
    digitalWrite(leftA,1);

    digitalWrite(leftB,0);

    digitalWrite(rightA,1);

    digitalWrite(rightB,1);
    Serial.println(" Arc Right");
}

void arcLeft()
{
    digitalWrite(leftA,1);

    digitalWrite(leftB,1);

    digitalWrite(rightA,1);

    digitalWrite(rightB,0);
    Serial.println("Arc Left");
}

void spotRight()
{
    digitalWrite(leftA,1);

    digitalWrite(leftB,0);

    digitalWrite(rightA,0);

    digitalWrite(rightB,1);
    Serial.println("Spot Right");
}

void spotLeft()
{
    digitalWrite(leftA,0);

    digitalWrite(leftB,1);

    digitalWrite(rightA,1);

    digitalWrite(rightB,0);
    Serial.println("Spot Left");
}


 
void setup()
{
    pinMode(leftA,OUTPUT);
    pinMode(leftB,OUTPUT);
    pinMode(rightA,OUTPUT);
    pinMode(rightB,OUTPUT);
    pinMode(5,OUTPUT);
    pinMode(6,OUTPUT);
    pinMode(13,OUTPUT);
    pinMode(RxD, INPUT); // Set pin to receive INPUT from bluetooth shield on Digital Pin 6
    pinMode(TxD, OUTPUT);
    Serial.begin(9600);
    //AUTO_FLAG = 0;
    Distance = 0;
    setupBlueToothConnection();

    analogWrite(5,255);
    analogWrite(6,255);
    AUTO_FLAG = 0;
    Distance = 0;
    
    Serial.println("@@@@@@@@@");
}

/*
 * This is the part which will be running repeatedly,
 * much like the forever block of 'SCRATCH'.
 */

void loop()
{
    //checkAUTO_FLAG();
    if(blueToothSerial.available())
    {//check for data sent from the remote bluetooth shield
      char recvChar = blueToothSerial.read();
      Serial.println(recvChar);
      
      switch (recvChar)
      {  
       case 'f' :moveForward();
                 delay(var);
                 break;
       case 'b' :moveBackward();
                delay(var);
                break;
       case 'a' :spotLeft();
                delay(var);
                break;
       case 'c' :spotRight();
                delay(var);
                break;
       case 's' : Stop();
                delay(var);
                break;
       case 'r' : arcRight();
                delay(var);
                break;
       case 'l': arcLeft();
                delay(var);
                break;
       
       case 'X' : {String str = blueToothSerial.readStringUntil('$');
                  int Speed = str.toInt();
                  Serial.println(Speed);
                  analogWrite(5,Speed);
                  analogWrite(6,Speed);
                  break;
       }
       case 'k' : digitalWrite(13,HIGH);
                  delay(250);
                  digitalWrite(13,LOW);
                  delay(250);
                  digitalWrite(13,HIGH);
                  delay(250);
                  digitalWrite(13,LOW);
                  delay(250);
       default : 
                 Stop();
  
      }
       
    

    }
    else
    {
      Stop();

    }

}
