#!/usr/bin/env bash

ctrl_gpio=P9.12

start() {
	config-pin -a $ctrl_gpio high
	config-pin -q $ctrl_gpio 
}

stop() {
	config-pin -a $ctrl_gpio low
	config-pin -q $ctrl_gpio
}

case $1 in
	start|stop) "$1" ;;
esac

