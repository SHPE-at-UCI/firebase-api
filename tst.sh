#!/bin/bash

for i in {1..9} 
do
    curl --data "emailInput=$i" http://localhost:5000/ &> /dev/null
done
