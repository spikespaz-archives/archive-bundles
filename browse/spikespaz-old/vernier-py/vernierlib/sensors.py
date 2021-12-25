#! /usr/bin/env python3
import usb.core
import usb.util


def _reading(device, endpoint):  # Generic sensor reading from byte array
    try:  # Surrounded with a try / catch to not throw an error on timeout
        return device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        # Read the data with the maximum packet size
    except usb.core.USBError as e:  # The device had an error, was it a timeout?
        if e.args == ("Operation timed out",):  # The device timed out so skip the reading and return None
            return None


def moisture_reading(device, endpoint):  # Provide a function wrapper for reading the moisture levels
    return 100 - round((176 - tuple(_reading(device, endpoint))[3]) * 100 / 34)  # The value ranges from
    # 134 to 176 as the 3rd item in the array returned by the human interface device
    # percent = 100 - (176 - reading) * 100 / 34
    # It is divided by 34 at the end because that is the max value, so it is "reading / 34"
    # The calculation returns percent of dryness, so subtract it from 100 to get moisture
