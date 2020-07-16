#!/bin/bash
gst-launch-1.0 nvarguscamerasrc ! 'video/x-raw(memory:NVMM),width=3280, height=2464, framerate=21/1, format=NV12' ! nvvidconv flip-method=0 ! 'video/x-raw,width=480, height=320' ! nvvidconv ! nvegltransform ! nveglglessink -e
