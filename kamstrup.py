import json
import serial
from time import sleep

SERIAL_PORT = '/dev/ttyUSB1'
SERIAL_SETTINGS = serial.Serial(SERIAL_PORT, 2400, timeout=1)

json_output = {}
while True:
    data = SERIAL_SETTINGS.read(320)
    if len(data) > 0:
      if not data:
        continue
      pkt = bytearray(data)
      data = SERIAL_SETTINGS.read(pkt[0])
      pkt.extend(bytearray(data))
      if len(pkt) < 228: # Smallest packet is 228 bytes List #1
#        print('Data is less than 228 bytes', len(data))
        continue
      list_type = pkt[30]
      if list_type == 25:
        date_time_year = pkt[17] << 8 | pkt[18]
        date_time_month = pkt[19]
        date_time_date = pkt[20]
        date_time_hour = str(pkt[22]).zfill(2)
        date_time_minute = str(pkt[23]).zfill(2)
        date_time_seconds = str(pkt[24]).zfill(2)
        date_time_str = (str(date_time_year) + '-' + str(date_time_month) + '-' + str(date_time_date) + ' ' + date_time_hour + ':' + date_time_minute + ':' + date_time_seconds)
        list_type = pkt[30]
        obis_list_version = (chr(pkt[33]) + chr(pkt[34]) + chr(pkt[35]) + chr(pkt[36]) + chr(pkt[37]) + chr(pkt[38]) + chr(pkt[39]) + chr(pkt[40]) + chr(pkt[41]) + chr(pkt[42]) + chr(pkt[43]) + chr(pkt[44]) + chr(pkt[45]) + chr(pkt[46]))
        meter_serial = (chr(pkt[57]) + chr(pkt[58]) + chr(pkt[59]) + chr(pkt[60]) + chr(pkt[61]) + chr(pkt[62]) + chr(pkt[63]) + chr(pkt[64]) + chr(pkt[65]) + chr(pkt[66]) + chr(pkt[67]) + chr(pkt[68]) + chr(pkt[69]) + chr(pkt[70]) + chr(pkt[71]) + chr(pkt[72]))
        meter_type = (chr(pkt[83]) + chr(pkt[84]) + chr(pkt[85]) + chr(pkt[86]) + chr(pkt[87]) + chr(pkt[88]) + chr(pkt[89]) + chr(pkt[90]) + chr(pkt[91]) + chr(pkt[92]) + chr(pkt[93]) + chr(pkt[94]) + chr(pkt[95]) + chr(pkt[96]) + chr(pkt[97]) + chr(pkt[98]) + chr(pkt[99]) + chr(pkt[100]))
        active_power_p = (pkt[110] << 24 | pkt[111] << 16 | pkt[112] << 8 | pkt[113])
        active_power_n = (pkt[123] << 24 | pkt[124] << 16 | pkt[125] << 8 | pkt[126])
        reactive_power_p = (pkt[136] << 24 | pkt[137] << 16 | pkt[138] << 8 | pkt[139])
        reactive_power_n = (pkt[149] << 24 | pkt[150] << 16 | pkt[151] << 8 | pkt[152])
        current_l1 = (pkt[162] << 24 | pkt[163] << 16 | pkt[164] << 8 | pkt[165])
        current_l2 = (pkt[175] << 24 | pkt[176] << 16 | pkt[177] << 8 | pkt[178])
        current_l3 = (pkt[188] << 24 | pkt[189] << 16 | pkt[190] << 8 | pkt[191])
        voltage_l1 = (pkt[201] << 8 | pkt[202])
        voltage_l2 = (pkt[212] << 8 | pkt[213])
        voltage_l3 = (pkt[223] << 8 | pkt[224])

      if list_type == 35: # Hour Packet List #2
        date_time_year = pkt[17] << 8 | pkt[18]
        date_time_month = pkt[19]
        date_time_date = pkt[20]
        date_time_hour = str(pkt[22]).zfill(2)
        date_time_minute = str(pkt[23]).zfill(2)
        date_time_seconds = str(pkt[24]).zfill(2)
        date_time_str = (str(date_time_year) + '-' + str(date_time_month) + '-' + str(date_time_date) + ' ' + date_time_hour + ':' + date_time_minute + ':' + date_time_seconds)
        list_type = pkt[30]
        obis_list_version = (chr(pkt[33]) + chr(pkt[34]) + chr(pkt[35]) + chr(pkt[36]) + chr(pkt[37]) + chr(pkt[38]) + chr(pkt[39]) + chr(pkt[40]) + chr(pkt[41]) + chr(pkt[42]) + chr(pkt[43]) + chr(pkt[44]) + chr(pkt[45]) + chr(pkt[46]))
        meter_serial = (chr(pkt[57]) + chr(pkt[58]) + chr(pkt[59]) + chr(pkt[60]) + chr(pkt[61]) + chr(pkt[62]) + chr(pkt[63]) + chr(pkt[64]) + chr(pkt[65]) + chr(pkt[66]) + chr(pkt[67]) + chr(pkt[68]) + chr(pkt[69]) + chr(pkt[70]) + chr(pkt[71]) + chr(pkt[72]))
        meter_type = (chr(pkt[83]) + chr(pkt[84]) + chr(pkt[85]) + chr(pkt[86]) + chr(pkt[87]) + chr(pkt[88]) + chr(pkt[89]) + chr(pkt[90]) + chr(pkt[91]) + chr(pkt[92]) + chr(pkt[93]) + chr(pkt[94]) + chr(pkt[95]) + chr(pkt[96]) + chr(pkt[97]) + chr(pkt[98]) + chr(pkt[99]) + chr(pkt[100]))
        active_power_p = (pkt[110] << 24 | pkt[111] << 16 | pkt[112] << 8 | pkt[113])
        active_power_n = (pkt[123] << 24 | pkt[124] << 16 | pkt[125] << 8 | pkt[126])
        reactive_power_p = (pkt[136] << 24 | pkt[137] << 16 | pkt[138] << 8 | pkt[139])
        reactive_power_n = (pkt[149] << 24 | pkt[150] << 16 | pkt[151] << 8 | pkt[152])
        current_l1 = (pkt[162] << 24 | pkt[163] << 16 | pkt[164] << 8 | pkt[165])
        current_l2 = (pkt[175] << 24 | pkt[176] << 16 | pkt[177] << 8 | pkt[178])
        current_l3 = (pkt[188] << 24 | pkt[189] << 16 | pkt[190] << 8 | pkt[191])
        voltage_l1 = (pkt[201] << 8 | pkt[202])
        voltage_l2 = (pkt[212] << 8 | pkt[213])
        voltage_l3 = (pkt[223] << 8 | pkt[224])
        date_time2_year = pkt[235] << 8 | pkt[236]
        date_time2_month = pkt[237]
        date_time2_date = pkt[238]
        date_time2_hour = str(pkt[239]).zfill(2)
        date_time2_minute = str(pkt[240]).zfill(2)
        date_time2_seconds = str(pkt[241]).zfill(2)
        date_time2_str = (str(date_time2_year) + '-' + str(date_time2_month) + '-' + str(date_time2_date) + ' ' + date_time2_hour + ':' + date_time2_minute + ':' + date_time2_seconds)
        active_energy_p = (pkt[256] << 24 | pkt[257] << 16 | pkt[258] << 8 | pkt[259])
        active_energy_n = (pkt[269] << 24 | pkt[270] << 16 | pkt[271] << 8 | pkt[272])
        reactive_energy_p = (pkt[282] << 24 | pkt[283] << 16 | pkt[284] << 8 | pkt[285])
        reactive_energy_n = (pkt[295] << 24 | pkt[296] << 16 | pkt[297] << 8 | pkt[298])

      json_output["date_time"] = date_time_str
      json_output["list_type"] = list_type
      json_output["obis_list_version"] = obis_list_version
      json_output["meter_serial"] = meter_serial
      json_output["meter_type"] =  meter_type
      json_output["active_power_p"] = active_power_p
      json_output["active_power_n"] = active_power_n
      json_output["reactive_power_p"] = reactive_power_p
      json_output["reactive_power_n"] = reactive_power_n
      json_output["current_l1"] = current_l1 / 100
      json_output["current_l2"] = current_l2 / 100
      json_output["current_l3"] = current_l3 / 100
      json_output["voltage_l1"] = voltage_l1
      json_output["voltage_l2"] = voltage_l2
      json_output["voltage_l3"] = voltage_l3
      if list_type == 35:
        json_output["date_time2"] = date_time2_str
        json_output["active_energy_p"] = active_energy_p / 100
        json_output["active_energy_n"] = active_energy_n / 100
        json_output["reactive_energy_p"] = reactive_energy_p / 100
        json_output["reactive_energy_n"] = reactive_energy_n / 100
      print(json.dumps(json_output))
#      print("HAN: Recv: " +
#              " ".join("0x{0:02x}".format(x) for x in pkt))
      

ser.close()
  
  
