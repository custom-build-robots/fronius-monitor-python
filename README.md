# Fronius solar monitor - python program
This repository is about my Fronius solar monitor realized as a python program.


## Idea:
The idea was to implement an easy way to access the Fronius solar API to show the most important information available for the setup my father in law installed in his house. I started first with a small program called "fronius.py" which only access the solar API or the so called inverter. The second program loads the "fronius.py" and shows the values in the terminal window. 
With those two programs you are now able to read all the information available via your Fronius inverter.

Then I build a small terminal with a touch screen and a Raspberry Pi to show all the information and to toggle a two Tasmota AC WiFi switches to switch on / off a pump and an electric stove to store and heat the living room. The prototype setup looks like a cardboard box as shown in the picture below.

With the python program gui_fronius_touch_screen.py I implemented a solution to display the most important key figures on a 5" touch sreen powered by a Raspberry Pi 3 B+.

![Fronius Python monitor](https://www.blogyourearth.com/wp-content/uploads/2022/12/Fronius_Monitor_Python_WIFI_Touchscreen_1-1024x768.jpg)

I will update the readme very soon for some more details. In the meantime visit my blog.

## More details are available on my blog: 
https://www.blogyourearth.com/top-story/fronius-solar-api-python-beispielprogramm-monitor/12810
