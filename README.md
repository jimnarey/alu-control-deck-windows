# Arcade Legends Ultimate Control Deck Windows

This program enables use of the control deck which forms part of the Arcade Legends Ultimate (ALU) arcade cabinet to be used on Windows. It uses [vJoy](https://sourceforge.net/projects/vjoystick/) to present the two controllers as either Xbox 360 or DualShock 4 controllers.

This is mostly useful for anyone who has replaced the SBC in the ALU with a full PC. This is worth doing.

> I replaced the SBC in my ALU with the guts of a refurbished Lenovo office PC which cost around £120 and it makes everything easier to work with and expands the capability of the cabinet enormously. Far and away the best OS is Batocera, which works with the ALU's control deck out of the box. However, despite Batocera's excellent WINE support, there are some edge cases where running Windows is necessary. 

## Status

This is a work in progress. Right now, it only reads from the HID devices connected to the machine and prints the status of their inputs. This is necessary to properly map the controls to vJoy. 

To read from the attached HID devices, run:

```
python main.py -r
```

## Config File

This is designed to enable the program to be used with other controller types not supported by Windows. To add a controller, run the read command. The inputs for a given controller are provided in a list. Note the index associated with each input and the value of a given action (button press, stick move etc). Then add these to the config file, following the format of the existing controller definition. 

Note that the key for each definition is the `vendor_id` and `product_id` separated by a colon. Also note that these are not the same as the `VID` or `PID`. The latter pair refer to the device as a whole (e.g. the whole ALU control deck). The former pair refer to an individual device, e.g. a single controller within the control deck.

> The ALU control deck is a composite device (has a `VID` and `PID`) comprised of three child devices, the two controller devices (one stick, six game buttons, a start button and in the case of the first controller a menu and a select button), and a device comprising the trackball and spinners which reports as a mouse. 