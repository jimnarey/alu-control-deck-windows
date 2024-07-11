# Arcade Legends Ultimate Control Deck Windows

This program enables use of the control deck which forms part of the Arcade Legends Ultimate (ALU) arcade cabinet to be used on Windows. It uses [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases) to present the two controllers as either Xbox 360 or DualShock 4 controllers.

> Note the comment in the releases page about having to run the setup program
twice.

This is mostly useful for anyone who has replaced the SBC in the ALU with a full PC. This is worth doing.

> If you upgrade your ALU cabinet with a full PC motherboard, Batocera is the best choice of OS for virtually all use cases. It has very good WINE support. However, there are a few egde cases where Windows is needed.

## Requirements

- Windows 10. May work on other versions but this hasn't been tested.
- [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases)
- [Python 3](https://www.python.org/downloads/windows/)

> Note the comment in the ViGEmBus releases page about needing to run the installer twice.

## Status

This is a work in progress.

Running `python main.py` will enable the first of the two controllers in the control deck and present it as a DualShock 4 controller. However, the menu/guide button on the control deck is unmapped. Further work is needed to enable this and the second controller.

The program can read from attached HID devices and print the results to the console. This functionality was used to map the control deck inputs to the virtual controller outputs. It throws read errors for some HID devices. Because these did not include the control deck controllers I haven't investigated the cause. 

> The trackball and spinners, which report as single mouse device, **do** throw read errors.

To read from the attached HID devices, run:

```
python main.py -r
```

## Config File

This is designed to enable the program to be used with other controller types not supported by Windows. To add a controller, run the read command. The inputs for a given controller are provided in a list. Note the index associated with each input and the value of a given action (button press, stick move etc). Then add these to the config file, following the format of the existing controller definition. 

Note that the key for each definition is the `vendor_id` and `product_id` separated by a colon. Also note that these are not the same as the `VID` or `PID`. The latter pair refer to the device as a whole (e.g. the whole ALU control deck). The former pair refer to an individual device, e.g. a single controller within the control deck.

> The ALU control deck is a composite device (has a `VID` and `PID`) comprised of three child devices, the two controller devices (one stick, six game buttons, a start button and in the case of the first controller a menu and a select button), and a device comprising the trackball and spinners which reports as a mouse. 