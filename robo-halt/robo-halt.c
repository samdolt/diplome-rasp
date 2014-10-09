/*
 * isr.c:
 *	Wait for Interrupt test program - ISR method
 *
 *	How to test:
 *	  Use the SoC's pull-up and pull down resistors that are avalable
 *	on input pins. So compile & run this program (via sudo), then
 *	in another terminal:
 *		gpio mode 0 up
 *		gpio mode 0 down
 *	at which point it should trigger an interrupt. Toggle the pin
 *	up/down to generate more interrupts to test.
 *
 * Copyright (c) 2013 Gordon Henderson.
 ***********************************************************************
 * This file is part of wiringPi:
 *	https://projects.drogon.net/raspberry-pi/wiringpi/
 *
 *    wiringPi is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    wiringPi is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
 ***********************************************************************
 */

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>


// What GPIO input are we using?
//	This is a wiringPi pin number

#define	BUTTON_PIN	0

// globalCounter:
//	Global variable to count interrupts
//	Should be declared volatile to make sure the compiler doesn't cache it.

const int off_request_pin = 5;
const int rasp_off_pin = 4;



/*
 * myInterrupt:
 *********************************************************************************
 */

void off_request (void) {
    static int halt_process = 0;
    
    if(!halt_process) {
        halt_process = 1;
        printf("Procédure d'exctinction enclenchée \n");
        system("sudo halt");
    }
        
}


/*
 *********************************************************************************
 * main
 *********************************************************************************
 */
 

int main (void)
{

  wiringPiSetupGpio();

  wiringPiISR (off_request_pin, INT_EDGE_RISING, &off_request) ;
  
  // Settup is done -> tell PIC32 with rasp_off_pin
  digitalWrite(rasp_off_pin, LOW);
  pinMode(rasp_off_pin, OUTPUT);


  for (;;)
  {

  }

  return 0 ;
}

