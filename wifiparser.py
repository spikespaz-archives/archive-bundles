#! /usr/bin/env python3
from sys import argv


def parse_creds(filename):
    ssid_list = []
    pass_list = []

    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()

            if line.startswith("<string name=\"SSID\">"):
                ssid = line.replace("<string name=\"SSID\">", "")
                ssid = ssid.replace("</string>", "")
                ssid = ssid.replace("&quot;", "")

                ssid_list.append(ssid)

            elif line.startswith("<string name=\"PreSharedKey\">"):
                passwd = line.replace("<string name=\"PreSharedKey\">", "")
                passwd = passwd.replace("</string>", "")
                passwd = passwd.replace("&quot;", "")

                pass_list.append(passwd)

            elif line.endswith("<null name=\"PreSharedKey\" />"):
                pass_list.append(None)

    return dict(zip(ssid_list, pass_list))


if __name__ == "__main__":
    networks = parse_creds(argv[1])

    if len(argv) > 2:
        with open(argv[2], "a") as f:
            for ssid, passwd in networks.items():
                f.write("SSID: {}\nPassword: {}\n\n".format(ssid, passwd))
    else:
        for ssid, passwd in networks.items():
            print("SSID: {}\nPassword: {}\n".format(ssid, passwd))
