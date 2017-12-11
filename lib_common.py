#! /usr/bin/env python3
from time import strftime
from pyfiglet import figlet_format
from os import system, name as os_name, popen


# Universally compatible clear function for getting a clean console to display on
def clear():
    system("cls") if os_name == "nt" else system("clear")


# Function to pretty print to the perfect center of a console window
def fullscreen_print(text, font="dotmatrix", top_pad=0):
    size = popen("stty size", "r").read().split()  # Make a tuple for the size of the console
    size = int(size[1]), int(size[0])  # Switch them, make it W, H with ints

    fig = figlet_format(str(text), font=font, justify="center", width=size[0])  # Get the fig formatted string

    fig_height = len(fig.split("\n"))  # Get the line length of the figlet formatted string
    top_pad += round((size[1] - fig_height) / 2)  # Calculate top padding (newlines) to put before the fig

    clear()  # Clear the screen
    print("\n" * top_pad, fig)  # Print the figlet and padding


# Write a line to a log file with args
def log_line(log_file, text, level=None, indent=0, date_fmt="%m-%d-%y", time_fmt="%I:%M:%S %p"):
    line_text = (" " * indent + strftime("[" + date_fmt + " | " + time_fmt + "]") +
                 ((" [" + level.upper() + "]") if level else "") + ": " + text + "\n")

    if log_file.mode in ("a", "a+"):
        log_file.write(line_text)
    elif log_file.mode == "w+":
        log_file.write(log_file.read() + line_text)
    else:
        raise FileNotFoundError("File must be write-able.")
