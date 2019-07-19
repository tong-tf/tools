#!/bin/bash


for fps in $(seq 50 60); do
	echo "$1 to $fps"
	lcm_fps.py $1 $fps
	./quick-make.sh k
	if [ -f kernel/resource.img ]; then
		cp kernel/resource.img rockdev/Image-rk3399_mid/resource-$fps.img
	fi
done
