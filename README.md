# Jstris-MaxAPM-Checker
An eligibility checker designed for TAWS' Jstris tournaments coded in Python.

## What it does
This software was designed for TAWS' Jstris tournaments in order to apply a maximum all-time APM limit to registered players to prevent sandbagging. However, this software can be used for any tournament that requires an all-time APM cap.

This software is very barebones, with its only features being to determine if a player is below the all-time APM limit or not, with a warning being issued for being within 90% of the limit.

## Usage
Ensure that the requests library is installed by running `pip install requests` from the command line, then run the program from the commandline, with the following command:
``` 
python JAWSEligibilityChecker.py <name> <apmCap>
```
where `<name>` is the Jstris name of the user that you wish to check, and `<apmCap>` being the APM Cap for the tournament. Linux and macOS users may have to run the command with `python3` instead of `python`.
