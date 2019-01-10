# MuMuDVB Service Auto Start/Stop Solution
Script which allows to change MuMuDVB service state automatically. In other words, script able to automatically start and stop specified configuration file. User trigger on specific port initiate MuMuDVB service auto startup. If script can't find established connection from user for declared time interval, it automatically kills MuMuDVB service process and will wait new incoming trigger from user again.

## Purpose
MuMuDVB is DVB IPTV free streaming software which can run on Raspberry Pi. Problem is that MuMuDVB increases CPU load a lot, so Raspberry Pi is using CPU 100% most of the time. It is not practical to always run MuMuDVB service on this tiny computer due to limited CPU power. IPTV on demand using Raspberry Pi was the main reason why I built this script.

## Usage
If you have MuMuDVB service [configured](http://www.hospitableit.com/howto/streaming-dvb-t-over-an-ip-network-using-mumudvb-on-a-raspberry-pi-3/), to run this automation script is really easy:
```
python iptv_on_demand.py
```
<b>Note:</b> Please check and update `PORT` and `MUMUDVB_SCRIPT_LOCATION` variables according your needs.

## Shortcomings
Script is basically listening on MuMuDVB port until user opend IPTV channels playlist. Then binded socket connection will be closed and specified MuMuDVB configuration file will be started on the same port. These actions require time. This is means that user will probably gets error, that IPTV service is not running. However, this shortcoming applies only for the first channel on the list.

## Future Plans
I am planning to add the following features in the future:
* Additional parameters usage via flags;
* Output logging into the file;
* Find the way to eliminate current shortcoming.
