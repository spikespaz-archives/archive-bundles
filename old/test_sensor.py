#! /usr/bin/env python3
from go_link import claim_device, find_device
from sensors import moisture_reading
from pyfiglet import figlet_format
from os import system, name as os_name, popen
from time import sleep


try:
    device, endpoint = claim_device()  # Attempt to auto-claim the device endpoint
except ConnectionError:  # claim_device raises ConnectionError when a device isn't found, so catch that
    device, endpoint = claim_device(find_device())  # Try again, maybe the device is unplugged?


def clear():  # generic clear function. "cls" for Windows and "clear" to shell for everything else
    system("cls") if os_name == "nt" else system("clear")


def fullscreen_print(text):
    size = popen("stty size", "r").read().split()
    size = int(size[1]), int(size[0])

    fig = figlet_format(text, font="doh", justify="center", width=size[0])

    fig_height = len(fig.split("\n"))
    top_pad = round((size[1] - fig_height) / 2) + 3

    clear()
    print("\n" * top_pad, fig)


while True:  # Infinite test loop
    fullscreen_print(str(moisture_reading(device, endpoint)) + "%")  # Print the percentage returned from the device
    sleep(0.01)  # Sleep the loop for 10ms
