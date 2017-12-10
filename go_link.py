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


def claim_device(device=None, interface=0, verbose=True):  # If the device has been
    # claimed by the OS or Kernel, release it and give it to the process
    if device is None:  # Nothing can be done with an empty object
        device = auto_detect(verbose)  # Attempt to auto connect

    if not device:  # device still wasn't found, even after auto connect
        raise ConnectionError("No connected Go! Link device.")  # Raise a ConnectionError to abort the process
    try:
        endpoint = device[0][(0, 0)][0]  # Get the device endpoint
    except TypeError:  # Couldn't create an endpoint with the device
        raise ValueError("Could not create endpoint.")  # Say so and abort

    if device.is_kernel_driver_active(interface):  # Is the kernel active on the device?
        device.detach_kernel_driver(interface)  # Tell the kernel to fuck off
        usb.util.claim_interface(device, interface)  # Claim the device for the process

    return device, endpoint  # Return a tuple with the endpoint and device object
