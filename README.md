# Arcade Legends Ultimate Control Deck Windows

This program enables use of the control deck which forms part of the Arcade Legends Ultimate (ALU) arcade cabinet to be used on Windows. It uses [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases) to present the two controllers as either Xbox 360 or DualShock 4 controllers.

This is mostly useful for anyone who has replaced the SBC in the ALU with a full PC. This is worth doing. The cabinet is crippled by the SBC and the locked down nature of the Arcade Legends software.

> If you upgrade your ALU cabinet with a full PC motherboard, Batocera is the best choice of OS for virtually all use cases. It has very good WINE support. However, there are a few edge cases where Windows is needed.

## Requirements

- Windows 10. May work on other versions but this hasn't been tested.
- [ViGEmBus](https://github.com/nefarius/ViGEmBus/releases)
- [Python 3](https://www.python.org/downloads/windows/) if not using the packaged version.

> Note the comment in the ViGEmBus releases page about needing to run the installer twice.

## Status

This is still a work in progress but so far works well.

`C` and `Z` on each of the ALU controllers are mapped to `L1` and `R1` on the virtual pads. `P1` and `P2` are mapped to the `start` button on their respective virtual controllers. 

On the first ALU controller, the central white button is mapped to the `Xbox` or `PS` button on its virtual counterpart. The `<<` button is mapped to `select`/`back`.

There's currently no way of changing these mappings without editing the code and re-building the project (the edits would be pretty simple).

When using a virtual DS4 controller, the accelerometer shows output in a single direction. This may be the default when using a real controller (due to gravity) but in any case doesn't appear to affect operation. However, please bear this in mind in case you run any applications which accept accelerometer input.

## Installation

A packaged `.exe` can be downloaded from the [releases](https://github.com/jimnarey/alu-control-deck-windows/releases) page. Just unzip the archive somewhere.

For the time being the packaged version works only on 64bit versions of Windows 10.

The packaged version requires ViGEmBus to be installed (see requirements section, above) but does not require Python 3 to be installed or any Python packages.

## How to use

To create a pair of Xbox 360 controllers, representing each of the controllers in the ALU control deck, run:

```
alu-control-win.exe
```

To represent the physical controllers as PlayStation DualShock 4 controllers instead, run:

```
alu-control-win.exe -t DS4
```

The program can read from attached HID devices and print the results to the console. This functionality was used to retrieve the values of each of the control deck inputs so they could be mapped to the virtual controller outputs in the main application. It throws read errors for some HID devices. Because the error-throwing devices did not include the control deck controllers I haven't investigated the cause. 

> The trackball and spinners, which report as single mouse device, **do** throw read errors.

To read from the attached HID devices, run:

```
alu-control-win.exe -r
```

## Running on Windows boot

- Open the location of thr `.exe` file in Windows Explorer.
- Enter `run` in the Start Menu search box and hit `Enter`.
- Enter `shell:startup` and hit `Enter`. This will open the startup directory in Windows Explorer.
- Right click on the program `.exe` file in the first Explorer window.
- Right click in empty space in the startup directory Explorer windows and select `Paste shortcut`.
- Rename the shortcut if desired.
- Right click on the shortcut and click `Properties`.
- In the options box which appears, select `Minimised` in the `Run` dropdown.
- If you prefer the ALU controllers to present as DualShock 4 controllers rather then Xbox 360 controllers, add ` -t DS4` to the command in the `Target` box. Note there should be a space between the existing command and the added text.

The virtual controllers will appear a few seconds after Windows loads.

The program will appear in the Windows Taskbar and can be closed at any time by right-clicking and selecting `Close`.

If you're not using the packaged version then instead of adding a shortcut to thr `.exe` file to the startup directory, add a shortcut to the Python 3 executable instead and add the path to the `alu-control-win.py` file as per the 'Installing/Running with Python` section below.

## Options

There are several options which can be passed on the command line:

```
Usage: main.py [options]

Represent Arcade Legends Ultimate control deck as 360/DS4 conrtollers  

Options:
  -h, --help            show this help message and exit
  -r, --read            Read from attached HID devices, print inputs to
                        console. Ignores all other options except -r   
  -s REPORT_SIZE, --reportsize=REPORT_SIZE
                        The report size specified when reading from HID
                        devices. Default 256. Should be no need to change.
  -t TYPE, --type=TYPE  Virtual device type. Defaults to Xbox 360 controller.
                        Specify '-t DS4' to use virtual DualShock 4
                        controllers instead
  -d DEVICE, --device=DEVICE
                        The vendor_id:product_id for the two ALU controllers,
                        as reported by the '-r- option. Just in case they vary
                        machine to machine. Defaults to '2104:35096'
  -p POLLRATE, --pollrate=POLLRATE
                        The poll rate of the physical controllers in HZ.
                        Defaults to 500
```

## Installing/Running with Python

Using the packaged version is the simplest option but if, for any reason, it doesn't work (e.g. you're running on a 32bit version of Windows), the program can be run by cloning the repo or downloading the source in `.zip` format (using the `Code` button above).

### Install dependencies

Install Python 3 and ViGEmBus (see requirements section).

Install the Python packages required by the project. From a terminal, within the project directory, run:

```
pip install -r hidapi vgamepad
```

### Running

Instead of running the `alu-control-win.exe` command, run the program with:

```
python "C:\path\to\alu-control-win.py"
```

...replacing the target path with the actual location of the `alu-control-win.py` file. 

Command line options (e.g. `-t DS4`) can be added to the end of the command in exactly the same way as when using the `.exe` version.

## Building

You may want to create a virtualenv for the project.

Clone the repository. Install the dependencies with:

```
pip install -r requirements.txt
```

Build the project:

```
pyinstaller --add-binary .\.venv\Lib\site-packages\vgamepad\win\vigem\client\x64\ViGEmClient.dll:. .\alu-control-win.py
```

This will create a `dist` subdirectory containing the built application directory.

## Code Style

Extremely basic, to enable easy porting of the application to C++ if required. Based on testing so far, this probably won't be necessary.
