# kamstrup-homeassistant
A quick and dirty script to make Kamstrup HAN data available to a file sensor in HomeAssistant

Connects to HAN meter with a MBus USB stick.
Prints a json output.
*1 phase meters are untested, just programmed based on findings.*
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

Example output of 10 second list:
```json
{"packet_size": 228, "date_time": "2019-10-14 18:26:10",
 "day_of_week": "Monday", "list_type": 25,
 "obis_list_version": "Kamstrup_V0001",
 "obis_m_s": "1.1.0.0.5.255", "meter_serial": "XXXXXXXXXXXXXXXX",
 "obis_m_t": "1.1.96.1.1.255", "meter_type": "6841121XXXXXXXXXXX",
 "meter_type_str": "Omnipower 3 Phase 3-Wire Direct meter",
 "obis_a_p_p": "1.1.1.7.0.255", "active_power_p": 4862,
 "obis_a_p_n": "1.1.2.7.0.255", "active_power_n": 0,
 "obis_r_p_p": "1.1.3.7.0.255", "reactive_power_p": 119,
 "obis_r_p_n": "1.1.4.7.0.255", "reactive_power_n": 0,
 "obis_c_l1": "1.1.31.7.0.255", "current_l1": 7.96,
 "obis_c_l2": "1.1.51.7.0.255", "current_l2": 15.99,
 "obis_c_l3": "1.1.71.7.0.255", "current_l3": 13.19,
 "obis_v_l1": "1.1.32.7.0.255", "voltage_l1": 236,
 "obis_v_l2": "1.1.52.7.0.255", "voltage_l2": 238,
 "obis_v_l3": "1.1.72.7.0.255", "voltage_l3": 235}
```


