#!/bin/bash
socat -d -d pty,raw,echo=0 pty,raw,echo=0 > /dev/null 2>&1 &
socat PTY,link=./ptyp1,b9600 PTY,link=./ptyp2,b9600 > /dev/null 2>&1 &
