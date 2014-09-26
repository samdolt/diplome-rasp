#!/usr/bin/env bash
gcc robo-halt.c -I/usr/local/include -L/usr/local/lib -lwiringPi -lpthread -o robo-halt
