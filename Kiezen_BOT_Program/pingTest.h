/*
 * Program : pingTest.h
 * This program will deal with the ping sensor.
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

#include "Arduino.h"

#ifndef pingTest_h
#define pingTest_h

int pingSensorPin;
long duration, inches, cm;

long microsecondsToCentimeters(long microseconds)
{
	return microseconds / 29 / 2;
}

long getDistanceFromPing(int pin1, int pin2)
{
    int pingPin = pin1;
    int pingEchoPin = pin2;
    pinMode(pingPin, OUTPUT);
    digitalWrite(pingPin, LOW);
    delayMicroseconds(2);
    digitalWrite(pingPin, HIGH);
    delayMicroseconds(5);
    digitalWrite(pingPin, LOW);

    // The same pin is used to read the signal from the PING))): a HIGH
    // pulse whose duration is the time (in microseconds) from the sending
    // of the ping to the reception of its echo off of an object.
    pinMode(pingEchoPin, INPUT);
    duration = pulseIn(pingEchoPin, HIGH);

    // convert the time into a distance
    cm = microsecondsToCentimeters(duration);

    Serial.print(cm);
    Serial.print("cm");
    Serial.println();

    delay(10);
    return cm;
}

long microsecondsToInches(long microseconds)
{
	return microseconds / 74 / 2;
}

#endif pingTest_h
