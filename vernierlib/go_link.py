#! /usr/bin/env python3
import usb.core
import usb.util
from time import sleep


def find_device(timeout=10, verbose=True):  # Find a Vernier device by scanning new connections after 10s
    all_connected = [(cfg.idVendor, cfg.idProduct) for cfg in usb.core.find(find_all=True)]
    # Create the initial list of connected devices before the Go! Link is connected

    if verbose:
        print("Please insert Go! Link device. Timeout in", timeout, "seconds.")  # Let the user know what's happening
    sleep(timeout)  # Give the user the duration of the timeout to plug in the sensor

    for device in usb.core.find(find_all=True):  # Scan all devices again
        if (device.idVendor, device.idProduct) not in all_connected:  # If the product information isn't
            # found in the previous list it must be a new device, so connect to it
            if verbose:  # Tell the user all the connection information
                print("Device found:", usb.util.get_string(device, device.iProduct),
                      "by", usb.util.get_string(device, device.iManufacturer))
            return device  # Return the device object and data

    if verbose:  # Tell the user that it has fallen back, no new connections found
        print("No Go! Link devices found.")
    return None  # Fallback, return None


def auto_detect(verbose=True):  # Attempt to automatically detect and scan all ports for a link
    for device in usb.core.find(find_all=True):  # For all scanned devices connected
        device_name = str(usb.util.get_string(device, device.iProduct))  # The name is this, accessed by the device data

        if device_name.startswith("Go! Link"):  # If the expected name is in the device string
            if verbose:  # User wants all the output, tell them it connected
                print("Device found:", device_name, "by",
                      str(usb.util.get_string(device, device.iManufacturer)))
            return device  # Return the device object and data

    if verbose:  # Tell the user that none were found
        print("No Go! Link devices found.")
    return None  # Return that None
