# kamstrup-homeassistant
A quick and dirty script to make Kamstrup HAN data available to a file sensor in HomeAssistant

Connects to HAN meter with a MBus USB stick.
Prints a json output.
I pipe this to a file, and then set up file sensors in homeassistant to track the various parameters.