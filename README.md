# kamstrup-homeassistant
A quick and dirty script to make Kamstrup HAN data available to a file sensor in HomeAssistant

Connects to HAN meter with a MBus USB stick.
Prints a json output.
I pipe this to a file, and then set up file sensors in homeassistant to track the various parameters.

`unbuffer python /srv/hass3.6/src/KAmstrup/han_kamstrup.py 2>&1 | tee /home/hass/.homeassistant/HAN/han-data.json &`

```yaml
sensor:
  - platform: file
    name: 'AMS aktiv forbruk import'
    file_path: /home/hass/.homeassistant/HAN/han-data.json
    value_template: '{{ value_json.active_energy_p }}'
    unit_of_measurement: 'kWh'
```


