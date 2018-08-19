#! /usr/bin/env python3
from sys import stdout
from argparse import ArgumentParser


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
    args = ArgumentParser()

    args.epilog = "Created by spikespaz (Jacob Birkett). Repository: https://github.com/spikespaz/tool-scripts"
    args.add_argument(
        "-i",
        "--in",
        help="Path to input file to read. Usually found at `/data/misc/wifi/WifiConfigStore.xml`.",
        dest="file_in",
        required=True)
    args.add_argument(
        "-o",
        "--out",
        help="Path to the output file to write retrieved data to. If unspecified, will be printed to `STDOUT`.",
        dest="file_out")
    args.add_argument(
        "-a",
        "--all",
        help="Include open networks or ones without a password in the output.",
        dest="log_all",
        action="store_true")

    options = args.parse_args()

    networks = parse_creds(options.file_in)

    out = open(options.file_out, "a") if options.file_out else stdout

    for ssid, passwd in networks.items():
        if options.log_all or passwd:
            out.write("SSID: {}\nPassword: {}\n\n".format(ssid, passwd or ""))
