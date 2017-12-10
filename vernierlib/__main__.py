#! /usr/bin/env python3
from vernierlib.go_link import *
from sensors import *


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
