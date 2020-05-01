#!/bin/bash

./killme.py &
PROGRAM=$!

rm -f ./killme.fifo
mkfifo ./killme.fifo

KILLSTR=$(cat ./killme.fifo)

if [ "$KILLSTR" == "killme" ]
then
	kill $PROGRAM
fi
