#!/usr/bin/env python
# coding:   latin-1
"""
Autor:    Ingmar Stapel
Datum:    20221225
Version:  0.1
Homepage: https://www.blogyourearth.com

This tiny program is used to control a tasmota wifi switch.

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



def Switch_Tasmota(host, state):
	endpoint = "/cm?cmnd=Power%20" + state

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata


def Read_Switch_Status_Tasmota(host):
	endpoint = "/cm?cmnd=Power"

	url = 'http://' + str(host) + str(endpoint)
	r = requests.get(url, timeout=60)
	r.raise_for_status()
	jsondata = r.json()

	return jsondata
