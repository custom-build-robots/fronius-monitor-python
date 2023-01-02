#!/usr/bin/env python
# coding:   latin-1
"""
Autor:    Ingmar Stapel
Datum:    20230101
Version:  0.2
Homepage: http://custom-build-robots.com

This tiny program which fetches the results of the fronius API endpoints.

This program should run out of the box on the latest Raspbian Bullseye OS.

In case of the following error:
-----> requests.exceptions.InvalidURL: Failed to parse: <-----

This error could be fixed by upgrading the urllib3 with the following command:
-----> pip install --upgrade urllib3 <-----

"""

import requests
import sys
import os
import json
import re
import socket

def GetPowerFlowRealtimeData(host):
	endpoint = "/solar_api/v1/GetPowerFlowRealtimeData.fcgi"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata

def GetStorageRealtimeData(host):
	endpoint = "/solar_api/v1/GetStorageRealtimeData.cgi?Scope=System"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata

def GetActiveDeviceInfo(host):
	endpoint = "/solar_api/v1/GetActiveDeviceInfo.cgi?DeviceClass=System"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata

def GetInverterInfo(host):
	endpoint = "/solar_api/v1/GetInverterInfo.cgi"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata

def GetInverterRealtimeData(host):
	endpoint = "/solar_api/v1/GetInverterRealtimeData.cgi?Scope=System"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata

def GetLoggerInfo(host):
	endpoint = "/solar_api/v1/GetLoggerInfo.cgi"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata

def GetLoggerLEDInfo(host):
	endpoint = "/solar_api/v1/GetLoggerLEDInfo.cgi"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata


def GetMeterRealtimeData(host):
	endpoint = "/solar_api/v1/GetMeterRealtimeData.cgi?Scope=System"
	#print("Fetching: " + endpoint)

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata

def saveJSONdata(jsondata, filename, directory):

	if not os.path.exists(directory):
		os.makedirs(directory)

	with open(os.path.join(directory, filename + ".json"), 'w') as f:
		json.dump(jsondata, f, indent=4, sort_keys=True)


def inverterLifeCheck(host, port):
	# Check if the inverters are online or not
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((host, port))
	if result == 0:
		#print("inverter is online")
		return "online"
	else:
		#print("inverter is offline")
		return "offline"