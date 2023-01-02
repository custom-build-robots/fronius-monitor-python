#!/usr/bin/env python
# coding:   latin-1
"""
Autor:    Ingmar Stapel
Datum:    20230102
Version:  0.2
Homepage: https://www.blogyourearth.com

This program shows some important key figures of our Fronius solar array
on a tiny touch screen together with a Raspberry Pi.
The solution is our Fronius monitor to control a pump and an electric stove.

This program should run out of the box on the latest Raspbian Bullseye OS.
"""
# python3 -m pip install PySimpleGUI

import PySimpleGUI as sg
import os
import subprocess
from datetime import datetime, timedelta
import time
import re
from fronius import *
from tasmota import *
import traceback
import logging

# Please set the IP address from the Fronius inverter you will access 
# Fronius inverter DACH
host_dach = "192.168.2.32"
# Fronius inverter ERKER
host_erker = "192.168.2.33"

# Tasmota AC WiFi switches
host_tasmota_1 = "192.168.2.46"
host_tasmota_2 = "192.168.2.XXX"

intervall = 1000

font_layout = "Helvetica 23"

# Define the window's contents

layout_text = [[sg.Text('Bezug aus dem Netz:', font=font_layout, key='-in_out-')],
            [sg.Text('Produktion Erker', font=font_layout, key='-prod_erker-')],
            [sg.Text('Produktion Dach', font=font_layout, key='-prod_dach-')],
            [sg.Text('Haus Verbrauch', font=font_layout, key='-cons-')],
            [sg.Text('Batterie Ladzustand', font=font_layout, key='-StateOfCharge-')],
            [sg.Text('Batterie Ladeleistung', font=font_layout, key='-p_akku-')],
            [sg.Button('Pumpe EIN', font=font_layout), sg.Button('Pumpe AUS', font=font_layout)],
            [sg.Text('Pumpe Status: ', font=font_layout, key='-pump_stat-'), sg.Text('-', font=font_layout, key='-pump_stat_value-'),sg.Text('', font=font_layout, size=(0,3), key='-pump_stat_dummy-')],
            [sg.Button('NEUSTART', font=font_layout)]]

layout_values = [[sg.Text('-', font=font_layout, key='-in_out_v-')],
            [sg.Text('-', font=font_layout, key='-prod_erker_v-')],
            [sg.Text('-', font=font_layout, key='-prod_dach_v-')],
            [sg.Text('-', font=font_layout, key='-cons_v-')],
            [sg.ProgressBar(1, orientation='h', size=(20,35), key='-progress_v-'), sg.Text(' -%', font=font_layout, key='-progress_v_t-')],
            [sg.Text('-', font=font_layout, key='-p_akku_v-')],
            [sg.Button('Ofen EIN',  font=font_layout), sg.Button('Ofen AUS', font=font_layout)],
            [sg.Button('Ofen Automatik', font=font_layout)],
            [sg.Text('Ofen Status: ', font=font_layout, key='-stove_stat-')],
            [sg.Button('AUSSCHALTEN', font=font_layout)]]

# ----- Full layout -----
layout = [
    [sg.Column(layout_text),
     sg.VSeperator(),
     sg.Column(layout_values)]
]

window = sg.Window('Fronius Monitor', layout, location=(0,0), size=(800,480), finalize=True)
window.Maximize()

# Display and interact with the Window using an Event Loop
while True:             # Event Loop
    try:
        timestamp_now = time.time()
        dach = inverterLifeCheck(host_dach, 80)
        erker = inverterLifeCheck(host_erker, 80)

        # was implemented to show a clock in the display in the upper right corner
        # Actual no longer implemented...
        # now = datetime.now()
        # current_time = now.strftime("%H:%M")
        # current_date = now.strftime("%d.%m.%Y")

        # Read the Tasmota switch state. The tasmota switch 1 
        # follows a timetable for an on/off activity of the switch
        tasmota_state = Read_Switch_Status_Tasmota(host_tasmota_1)
        tasmota_state_value = tasmota_state["POWER"]

        event, values = window.read(timeout=intervall)
        if event == sg.WIN_CLOSED or event == 'NEUSTART':
            os.system("sudo reboot")
            break
            
        if event == sg.WIN_CLOSED or event == 'AUSSCHALTEN':
            os.system("sudo shutdown -h now")
            break

        if event == 'Pumpe EIN':
            print("Pumpe ein")
            tasmota_state = Switch_Tasmota(host_tasmota_1, "on")
            tasmota_state_value = tasmota_state["POWER"]
            print(tasmota_state_value)

        if event == 'Pumpe AUS':
            print("Pumpe aus")
            tasmota_state = Switch_Tasmota(host_tasmota_1, "off")
            tasmota_state_value = tasmota_state["POWER"]
            print(tasmota_state_value)

        if event == 'Ofen EIN':
            print("Ofen EIN")

        if event == 'Ofen AUS':
            print("Ofen AUS")

        if event == 'Ofen Automatik':
            print("Ofen Automatik")

        if dach == "online":
            jsondata_power_flow = GetPowerFlowRealtimeData(host_dach)
            jsondata_storage = GetStorageRealtimeData(host_dach)
            # Timestamp Daten Power Flow
            ts_flow = jsondata_power_flow["Head"]["Timestamp"]
            # Energie Tag
            #p_day = jsondata_power_flow["Body"]["Data"]["Inverters"]["1"]["E_Day"]
            # Energie Jahr
            #p_year = jsondata_power_flow["Body"]["Data"]["Inverters"]["1"]["E_Year"]
            # Energie Gesamt
            #p_total = jsondata_power_flow["Body"]["Data"]["Inverters"]["1"]["E_Total"]
            # Einspeisung / Bezug: Negativ Einspeisung, positiv Bezug
            in_out = jsondata_power_flow["Body"]["Data"]["Site"]["P_Grid"]
            # Verbrauch momentan
            cons = jsondata_power_flow["Body"]["Data"]["Site"]["P_Load"]
            # Produktion Dach momentan
            prod_dach = jsondata_power_flow["Body"]["Data"]["Site"]["P_PV"]
            # Batterie ladenn
            p_akku = jsondata_power_flow["Body"]["Data"]["Site"]["P_Akku"]
            # Autonomie (% Produktion an Verbrauch)
            #autonomy = jsondata_power_flow["Body"]["Data"]["Site"]["rel_Autonomy"]
            # Selbstverbrauch (Eigenverbrauch an Produktion)
            #selfcons = jsondata_power_flow["Body"]["Data"]["Site"]["rel_SelfConsumption"]   
            # Ladezustand in %
            StateOfCharge = jsondata_storage["Body"]["Data"]["1"]["Controller"]["StateOfCharge_Relative"]

        if erker == "online":
            jsondata_power_flow = GetPowerFlowRealtimeData(host_erker)
            # Produktion Erker momentan
            prod_erker = jsondata_power_flow["Body"]["Data"]["Site"]["P_PV"]
        else:
            prod_erker = "0"

        #p_day = str(p_day).split('.', 1)[0]
        #p_year = str(p_year).split('.', 1)[0]
        #p_total = str(p_total).split('.', 1)[0]
        in_out = str(in_out).split('.', 1)[0]
        cons = str(cons).split('.', 1)[0]
        prod_dach = str(prod_dach).split('.', 1)[0]
        #autonomy = str(autonomy).split('.', 1)[0]
        #selfcons = str(selfcons).split('.', 1)[0]
        StateOfCharge = str(StateOfCharge).split('.', 1)[0]
        prod_erker = str(prod_erker).split('.', 1)[0]
        p_akku = str(p_akku).split('.', 1)[0]
        
        # If no sun shines prod_dach, prod_erker, selfcons and p_akku is null and 
        # my logic above return as value None. 
        # To get no error I have to deal with that and replase None with 0
        if prod_dach == "None":
            prod_dach = 0

        if prod_erker == "None":
            prod_erker = 0

        if p_akku == "None":
            p_akku = -1           

       # if selfcons == "None":
       #     selfcons = 0  

        if int(in_out) >= 0:
            window['-in_out-'].update('Bezug aus dem Netz:')
        else:
            window['-in_out-'].update('Einspeisung:')
        window['-prod_erker-'].update('Produktion Erker:')
        window['-cons-'].update('Haus Verbrauch:')
        window['-prod_dach-'].update('Produktion Dach:')
        window['-StateOfCharge-'].update('Batterie Ladzustand:')
        window['-progress_v-'].UpdateBar(int(StateOfCharge), 100)
        

        if int(p_akku) <= 0:
            window['-p_akku-'].update('Batterie laden:')
        else:
            window['-p_akku-'].update('Batterie entladen:')    


        window['-pump_stat_value-'].update(str(tasmota_state_value))

        # In case the battery is full 100% the solar panel called erker 
        # will directly load the energy back in the public net.
        if int(StateOfCharge) >= 100:
            window['-in_out_v-'].update(str(abs(int(in_out)) ) + ' W')
            # now at 100% battery charge the energy goes ino the grid...
            window['-in_out-'].update('Einspeisung Dach:')
            window['-prod_erker-'].update('Einspeisung Erker:')
        else:    
            window['-in_out_v-'].update(str(abs(int(in_out))) + ' W')
        window['-prod_dach_v-'].update(str(prod_dach) + ' W')
        window['-prod_erker_v-'].update(str(prod_erker) + ' W')
        window['-cons_v-'].update(str(abs(int(cons))) + ' W')
        window['-progress_v-'].UpdateBar(int(StateOfCharge), 100)
        window['-progress_v_t-'].update(str(StateOfCharge) + ' %')

        if int(p_akku) < 0:
            #window['-p_akku_v-'].update(str(abs(int(p_akku)) + abs(int(prod_erker))) + ' W')
            window['-p_akku_v-'].update(str(abs(int(p_akku))) + ' W')
            #window['-StateOfCharge-'].update(text_color='green')
        else:
            window['-p_akku_v-'].update(str(abs(int(p_akku))) + ' W')
            #window['-StateOfCharge-'].update(text_color='red')

        window['-stove_stat-'].update('Ofen Status: Kein Schalter')

        window.refresh()
    except Exception as e:
        logging.error(traceback.format_exc())
        print("Ooooops... ERROR")