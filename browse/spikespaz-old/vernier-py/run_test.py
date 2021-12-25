#! /usr/bin/env python3
from sys import argv
from time import sleep


def test_moisture():
    from time import sleep
    from vernierlib.sensors import moisture_reading
    import claim_device

    device, endpoint = claim_device()

    for _ in range(10):
        print(moisture_reading(device, endpoint))
        sleep(1)


def test_claim_device():
    from vernierlib.go_link import auto_detect

    print(auto_detect())


test_map = {
    "claim_device": test_claim_device,
    "moisture": test_moisture
}


if len(argv) > 1:
    exceptions = {}
    print("Starting", len(argv) - 1, "test" + ("s." if len(argv) - 1 > 1 else "."))

    for test in argv[1:]:
        if test in test_map:
            try:
                print("Starting test:", test)
                sleep(2)
                test_map[test]()
            except Exception as error:
                exceptions[test] = error
                print("Failed with exception:", error)
        else:
            print("Test not found:", test)

    print("Completed tests:", ", ".join(argv[1:]), "\n", len(exceptions), "failed.")

    if exceptions:
        print("\nExceptions:\n")
        for test, error in exceptions.items():
            print(test + ":\n", error)
