#!/usr/bin/env python
# coding:  latin-1
# Autor:   Ingmar Stapel
# Datum:   20160731
# Version: 2.0
# Homepage: https://www.blogyourearth.com
# This program is used to read the Fronius inverter API interface 
import sys, tty, termios, os, readchar

from fronius import *

# Please set the IP address from the Fronius inverter you will access 
host = "192.168.2.32"
# Please set the folder in which the json files should be stored.
folder = "/home/pi/"

# read the keyboard input
def getch():
   ch = readchar.readchar()
   return ch

# display the mneu
def printscreen(host):
    os.system('clear')
    print("Inverter IP: " + str(host) + "\n")
    print("Menu:")
    print("1: GetPowerFlowRealtimeData")
    print("2: GetStorageRealtimeData")
    print("3: GetActiveDeviceInfo")
    print("4: GetInverterInfo")
    print("5: GetInverterRealtimeData")
    print("6: GetLoggerInfo")
    print("7: GetLoggerLEDInfo")
    print("8: GetMeterRealtimeData")
    print("9: saveJSONdata")
    print("x: Programm beenden\n")

printscreen(host)

while True:
    # With the function getch() the keyboard input is read.
    # That input is needed to use / control the menu an execute the
    # functions to access the Fronius solar API
    char = getch()

    # Now the pressed keys are checked...
    if(char == "1"):
        printscreen(host)

        jsondata = GetPowerFlowRealtimeData(host)

        # Timestamp Daten Power Flow
        ts_flow = jsondata["Head"]["Timestamp"]
        # Energie Tag
        p_day = jsondata["Body"]["Data"]["Inverters"]["1"]["E_Day"]
        # Energie Jahr
        p_year = jsondata["Body"]["Data"]["Inverters"]["1"]["E_Year"]
        # Energie Gesamt
        p_total = jsondata["Body"]["Data"]["Inverters"]["1"]["E_Total"]
        # Einspeisung / Bezug: Negativ Einspeisung, positiv Bezug
        in_out = jsondata["Body"]["Data"]["Site"]["P_Grid"]
        # Verbrauch momentan
        cons = jsondata["Body"]["Data"]["Site"]["P_Load"]
        # Produktion momentan
        prod = jsondata["Body"]["Data"]["Site"]["P_PV"]
        # Autonomie (% Produktion an Verbrauch)
        autonomy = jsondata["Body"]["Data"]["Site"]["rel_Autonomy"]
        # Selbstverbrauch (% Eigenverbrauch an Produktion)
        selfcons = jsondata["Body"]["Data"]["Site"]["rel_SelfConsumption"]     

        print ("Timestamp Daten Power Flow: " + str(ts_flow))
        print ("Energie Tag: " + str(p_day))
        print ("Energie Jahr: " + str(p_year))
        print ("Energie Gesamt: " + str(p_total))
        print ("Einspeisung / Bezug:: " + str(in_out))
        print ("Verbrauch momentan: " + str(cons))
        print ("Produktion: " + str(prod))
        print ("Autonomie: " + str(autonomy))
        print ("Selbstverbrauch: " + str(selfcons))

    if(char == "2"):
        printscreen(host)
        jsondata = GetStorageRealtimeData(host)
        # Hersteller
        manufacturer = jsondata["Body"]["Data"]["1"]["Controller"]["Details"]["Manufacturer"]
        # Modell
        model = jsondata["Body"]["Data"]["1"]["Controller"]["Details"]["Model"]
        # Serial
        serial = jsondata["Body"]["Data"]["1"]["Controller"]["Details"]["Serial"]
        # Ladezustand in %
        StateOfCharge = jsondata["Body"]["Data"]["1"]["Controller"]["StateOfCharge_Relative"]

        print ("Hersteller: " + str(manufacturer))
        print ("Modell: " + str(model))
        print ("Serial: " + str(serial))
        print ("Batterie in %: " + str(StateOfCharge))

    if(char == "3"):
        printscreen(host)
        jsondata = GetActiveDeviceInfo(host)
        # Serial
        serial = jsondata["Body"]["Data"]["Meter"]["0"]["Serial"]

        print ("Serial: " + str(serial))

    if(char == "4"):
        printscreen(host)
        jsondata = GetInverterInfo(host)
        # PVPower
        PVPower = jsondata["Body"]["Data"]["1"]["PVPower"]

        print ("PVPower: " + str(PVPower))

    if(char == "5"):
        printscreen(host)
        jsondata = GetInverterRealtimeData(host)
        # DAY_ENERGY
        day_energy = jsondata["Body"]["Data"]["DAY_ENERGY"]["Values"]["1"]
        # TOTAL_ENERGY
        total_energy = jsondata["Body"]["Data"]["TOTAL_ENERGY"]["Values"]["1"]
        # YEAR_ENERGY
        year_energy = jsondata["Body"]["Data"]["YEAR_ENERGY"]["Values"]["1"]
        # PAC
        PAC = jsondata["Body"]["Data"]["PAC"]["Values"]["1"]

        print ("Day energy: " + str(day_energy) + " Wh")
        print ("Total energy: " + str(total_energy) + " Wh")
        print ("Year energy: " + str(year_energy) + " Wh")
        print ("PAC: " + str(PAC) + " W")

    if(char == "6"):
        printscreen(host)
        jsondata = GetLoggerInfo(host)

        # Logger Info on CO2 data
        power_led_coler = jsondata["Body"]["LoggerInfo"]["CO2Factor"]
        power_led_state = jsondata["Body"]["LoggerInfo"]["CO2Unit"]

        print ("CO2 Factor : " + str(power_led_coler))
        print ("CO2 unit: " + str(power_led_state))

    if(char == "7"):
        printscreen(host)
        jsondata = GetLoggerLEDInfo(host)

        # PowerLED
        power_led_coler = jsondata["Body"]["Data"]["PowerLED"]["Color"]
        power_led_state = jsondata["Body"]["Data"]["PowerLED"]["State"]

        print ("Power : " + str(power_led_coler))
        print ("Power LED state: " + str(power_led_state))

    if(char == "8"):
        printscreen(host)
        jsondata = GetMeterRealtimeData(host)


        Manufacturer = jsondata["Body"]["Data"]["0"]["Details"]["Manufacturer"]
        Model = jsondata["Body"]["Data"]["0"]["Details"]["Model"]
        Serial = jsondata["Body"]["Data"]["0"]["Details"]["Serial"]
        EnergyReactive_VArAC_Sum_Consumed = jsondata["Body"]["Data"]["0"]["EnergyReactive_VArAC_Sum_Consumed"]
        EnergyReactive_VArAC_Sum_Produced = jsondata["Body"]["Data"]["0"]["EnergyReactive_VArAC_Sum_Produced"]
        EnergyReal_WAC_Minus_Absolute = jsondata["Body"]["Data"]["0"]["EnergyReal_WAC_Minus_Absolute"]
        EnergyReal_WAC_Plus_Absolute = jsondata["Body"]["Data"]["0"]["EnergyReal_WAC_Plus_Absolute"]
        EnergyReal_WAC_Sum_Consumed = jsondata["Body"]["Data"]["0"]["EnergyReal_WAC_Sum_Consumed"]
        EnergyReal_WAC_Sum_Produced = jsondata["Body"]["Data"]["0"]["EnergyReal_WAC_Sum_Produced"]
        Frequency_Phase_Average = jsondata["Body"]["Data"]["0"]["Frequency_Phase_Average"]
        Meter_Location_Current = jsondata["Body"]["Data"]["0"]["Meter_Location_Current"]
        PowerApparent_S_Phase_1 = jsondata["Body"]["Data"]["0"]["PowerApparent_S_Phase_1"]
        PowerApparent_S_Phase_2 = jsondata["Body"]["Data"]["0"]["PowerApparent_S_Phase_2"]
        PowerApparent_S_Phase_3 = jsondata["Body"]["Data"]["0"]["PowerApparent_S_Phase_3"]
        PowerApparent_S_Sum = jsondata["Body"]["Data"]["0"]["PowerApparent_S_Sum"]
        PowerFactor_Phase_1 = jsondata["Body"]["Data"]["0"]["PowerFactor_Phase_1"]
        PowerFactor_Phase_2 = jsondata["Body"]["Data"]["0"]["PowerFactor_Phase_2"]
        PowerFactor_Phase_3 = jsondata["Body"]["Data"]["0"]["PowerFactor_Phase_3"]
        PowerFactor_Sum = jsondata["Body"]["Data"]["0"]["PowerFactor_Sum"]
        PowerReactive_Q_Phase_1 = jsondata["Body"]["Data"]["0"]["PowerReactive_Q_Phase_1"]
        PowerReactive_Q_Phase_2 = jsondata["Body"]["Data"]["0"]["PowerReactive_Q_Phase_2"]
        PowerReactive_Q_Phase_3 = jsondata["Body"]["Data"]["0"]["PowerReactive_Q_Phase_3"]
        PowerReactive_Q_Sum = jsondata["Body"]["Data"]["0"]["PowerReactive_Q_Sum"]
        PowerReal_P_Phase_1 = jsondata["Body"]["Data"]["0"]["PowerReal_P_Phase_1"]
        PowerReal_P_Phase_2 = jsondata["Body"]["Data"]["0"]["PowerReal_P_Phase_2"]
        PowerReal_P_Phase_3 = jsondata["Body"]["Data"]["0"]["PowerReal_P_Phase_3"]
        PowerReal_P_Sum = jsondata["Body"]["Data"]["0"]["PowerReal_P_Sum"]
        TimeStamp = jsondata["Body"]["Data"]["0"]["TimeStamp"]
        Visible = jsondata["Body"]["Data"]["0"]["Visible"]
        Voltage_AC_PhaseToPhase_12 = jsondata["Body"]["Data"]["0"]["Voltage_AC_PhaseToPhase_12"]
        Voltage_AC_PhaseToPhase_23 = jsondata["Body"]["Data"]["0"]["Voltage_AC_PhaseToPhase_23"]
        Voltage_AC_PhaseToPhase_31 = jsondata["Body"]["Data"]["0"]["Voltage_AC_PhaseToPhase_31"]
        Voltage_AC_Phase_1 = jsondata["Body"]["Data"]["0"]["Voltage_AC_Phase_1"]
        Voltage_AC_Phase_2 = jsondata["Body"]["Data"]["0"]["Voltage_AC_Phase_2"]
        Voltage_AC_Phase_3 = jsondata["Body"]["Data"]["0"]["Voltage_AC_Phase_3"]


        print ("Manufacturer:" + str(Manufacturer))
        print ("Model:" + str(Model))
        print ("Serial:" + str(Serial))
        print ("EnergyReactive_VArAC_Sum_Consumed: " + str(EnergyReactive_VArAC_Sum_Consumed))
        print ("EnergyReactive_VArAC_Sum_Produced: " + str(EnergyReactive_VArAC_Sum_Produced))
        print ("EnergyReal_WAC_Minus_Absolute: " + str(EnergyReal_WAC_Minus_Absolute))
        print ("EnergyReal_WAC_Plus_Absolute: " + str(EnergyReal_WAC_Plus_Absolute))
        print ("EnergyReal_WAC_Sum_Consumed: " + str(EnergyReal_WAC_Sum_Consumed))
        print ("EnergyReal_WAC_Sum_Produced: " + str(EnergyReal_WAC_Sum_Produced))
        print ("Frequency_Phase_Average: " + str(Frequency_Phase_Average))
        print ("Meter_Location_Current: " + str(Meter_Location_Current))
        print ("PowerApparent_S_Phase_1: " + str(PowerApparent_S_Phase_1))
        print ("PowerApparent_S_Phase_2: " + str(PowerApparent_S_Phase_2))
        print ("PowerApparent_S_Phase_3: " + str(PowerApparent_S_Phase_3))
        print ("PowerApparent_S_Sum: " + str(PowerApparent_S_Sum))
        print ("PowerFactor_Phase_1: " + str(PowerFactor_Phase_1))
        print ("PowerFactor_Phase_2: " + str(PowerFactor_Phase_2))
        print ("PowerFactor_Phase_3: " + str(PowerFactor_Phase_3))
        print ("PowerFactor_Sum: " + str(PowerFactor_Sum))
        print ("PowerReactive_Q_Phase_1: " + str(PowerReactive_Q_Phase_1))
        print ("PowerReactive_Q_Phase_2: " + str(PowerReactive_Q_Phase_2))
        print ("PowerReactive_Q_Phase_3: " + str(PowerReactive_Q_Phase_3))
        print ("PowerReactive_Q_Sum: " + str(PowerReactive_Q_Sum))
        print ("PowerReal_P_Phase_1: " + str(PowerReal_P_Phase_1))
        print ("PowerReal_P_Phase_2: " + str(PowerReal_P_Phase_2))
        print ("PowerReal_P_Phase_3: " + str(PowerReal_P_Phase_3))
        print ("PowerReal_P_Sum: " + str(PowerReal_P_Sum))
        print ("TimeStamp: " + str(TimeStamp))
        print ("Visible: " + str(Visible))
        print ("Voltage_AC_PhaseToPhase_12: " + str(Voltage_AC_PhaseToPhase_12))	
        print ("Voltage_AC_PhaseToPhase_23: " + str(Voltage_AC_PhaseToPhase_23))
        print ("Voltage_AC_PhaseToPhase_31: " + str(Voltage_AC_PhaseToPhase_31))
        print ("Voltage_AC_Phase_1: " + str(Voltage_AC_Phase_1))
        print ("Voltage_AC_Phase_2: " + str(Voltage_AC_Phase_2))
        print ("Voltage_AC_Phase_3: " + str(Voltage_AC_Phase_3))

    if(char == "9"):    
        printscreen(host)
        print("All files will be saved in the folder " + folder)
        jsondata = GetPowerFlowRealtimeData(host)
        saveJSONdata(jsondata, "GetPowerFlowRealtimeData", folder)

        jsondata = GetStorageRealtimeData(host)
        saveJSONdata(jsondata, "GetStorageRealtimeData", folder)

        jsondata = GetActiveDeviceInfo(host)
        saveJSONdata(jsondata, "GetActiveDeviceInfo", folder)

        jsondata = GetInverterInfo(host)
        saveJSONdata(jsondata, "GetInverterInfo", folder)

        jsondata = GetInverterRealtimeData(host)
        saveJSONdata(jsondata, "GetInverterRealtimeData", folder)

        jsondata = GetLoggerLEDInfo(host)
        saveJSONdata(jsondata, "GetLoggerLEDInfo", folder)

        jsondata = GetMeterRealtimeData(host)
        saveJSONdata(jsondata, "GetMeterRealtimeData", folder)

        print("All files have been saved... in the folder " + folder)

    if(char == "x"):
        printscreen(host)       
        print("Quit program")
        break

    # now the variable char will be reset to catch the next input...
    char = ""

# end  