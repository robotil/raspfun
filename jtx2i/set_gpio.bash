#!/bin/bash

echo 298 > /sys/class/gpio/export
echo 388 > /sys/class/gpio/export
echo 480 > /sys/class/gpio/export
echo 486 > /sys/class/gpio/export
sleep 2
echo out > /sys/class/gpio/gpio388/direction
echo in > /sys/class/gpio/gpio298/direction
echo in > /sys/class/gpio/gpio480/direction
echo in > /sys/class/gpio/gpio486/direction

