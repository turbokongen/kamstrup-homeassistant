"""
Module that reads data from an Mbus serial adapter.

It decodes the incoming data and output json formatted dict.
"""

import datetime
import json
import logging
from time import sleep
import serial
from crccheck.crc import CrcX25

BAUDRATE = 2400
DATA_FLAG = [230, 231, 0, 15]
FRAME_FLAG = b'\x7e'
LIST_TYPE_SHORT_1PH = 17
LIST_TYPE_LONG_1PH = 27
LIST_TYPE_SHORT_3PH = 25
LIST_TYPE_LONG_3PH = 35
WEEKDAY_MAPPING = {
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday',
    7: 'Sunday'
}

SERIAL_PORT = '/dev/ttyUSB1'
TIMEOUT = 0
_LOGGER = logging.getLogger(__name__)


class HanPowermeter():
    """The HAN serial reader class."""

    def __init__(self):
        """Initialize variables."""
        self.ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUDRATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=TIMEOUT)
        self._pkt = None
        self._valid_data = None

    def test_valid_data(self, data):
        """Test the incoming data for validity."""
        self._valid_data = True
        if len(data) > 302 or len(data) < 180:
            self._valid_data = False
            _LOGGER.warning('Invalid packet size')
        if not data[0] and data[-1] == FRAME_FLAG:
            self._valid_data = False
            _LOGGER.warning("%s Recieved %s bytes of %s data",
                            datetime.datetime.now().isoformat(),
                            len(data), self._valid_data)
        header_checksum = CrcX25.calc(bytes(data[1:6]))
        read_header_checksum = (data[7] << 8 | data[6])
        if header_checksum != read_header_checksum:
            self._valid_data = False
            _LOGGER.warning('Invalid header CRC check')
        frame_checksum = CrcX25.calc(bytes(data[1:-3]))
        read_frame_checksum = (data[-2] << 8 | data[-3])
        if frame_checksum != read_frame_checksum:
            self._valid_data = False
            _LOGGER.warning('Invalid frame CRC check')
        return self._valid_data

    def read_bytes(self):
        """Read the raw data from serial port."""
        byte_counter = 0
        bytelist = []
        while True:
            data = self.ser.read()
            if data:
                bytelist.extend(data)
                if data == FRAME_FLAG and byte_counter > 1:
                    return bytelist
                byte_counter = byte_counter + 1
            else:
                sleep(2.5)

    def parse_data(self, data):
        """Parse the incoming data to dict."""
        # pylint: disable=too-many-locals, too-many-statements
        self._pkt = data
        if self._pkt[8:12] != DATA_FLAG:
            _LOGGER.warning('Data does not start with %s: %s',
                            DATA_FLAG, self._pkt[8:12])
            return False
        packet_size = len(self._pkt)
        han_data = {}
        read_packet_size = ((self._pkt[1] & 0x0F) << 8 | self._pkt[2]) + 2
        han_data["packet_size"] = read_packet_size

        if packet_size != read_packet_size:
            _LOGGER.warning(
                'Packet size does not match read packet size: %s : %s',
                packet_size, read_packet_size)
            return False

        date_time_year = self._pkt[17] << 8 | self._pkt[18]
        date_time_month = self._pkt[19]
        date_time_date = self._pkt[20]
        date_time_hour = str(self._pkt[22]).zfill(2)
        date_time_minute = str(self._pkt[23]).zfill(2)
        date_time_seconds = str(self._pkt[24]).zfill(2)
        date_time_str = (str(date_time_year) +
                         '-' + str(date_time_month) +
                         '-' + str(date_time_date) +
                         ' ' + date_time_hour +
                         ':' + date_time_minute +
                         ':' + date_time_seconds)
        han_data["date_time"] = date_time_str
        han_data["day_of_week"] = WEEKDAY_MAPPING.get(self._pkt[21])
        list_type = self._pkt[30]
        han_data["list_type"] = list_type
        han_data["obis_list_version"] = (chr(self._pkt[33]) +
                                         chr(self._pkt[34]) +
                                         chr(self._pkt[35]) +
                                         chr(self._pkt[36]) +
                                         chr(self._pkt[37]) +
                                         chr(self._pkt[38]) +
                                         chr(self._pkt[39]) +
                                         chr(self._pkt[40]) +
                                         chr(self._pkt[41]) +
                                         chr(self._pkt[42]) +
                                         chr(self._pkt[43]) +
                                         chr(self._pkt[44]) +
                                         chr(self._pkt[45]) +
                                         chr(self._pkt[46]))
        han_data["obis_m_s"] = (str(self._pkt[49]) +
                                '.' + str(self._pkt[50]) +
                                '.' + str(self._pkt[51]) +
                                '.' + str(self._pkt[52]) +
                                '.' + str(self._pkt[53]) +
                                '.' + str(self._pkt[54]))
        han_data["meter_serial"] = (chr(self._pkt[57]) +
                                    chr(self._pkt[58]) +
                                    chr(self._pkt[59]) +
                                    chr(self._pkt[60]) +
                                    chr(self._pkt[61]) +
                                    chr(self._pkt[62]) +
                                    chr(self._pkt[63]) +
                                    chr(self._pkt[64]) +
                                    chr(self._pkt[65]) +
                                    chr(self._pkt[66]) +
                                    chr(self._pkt[67]) +
                                    chr(self._pkt[68]) +
                                    chr(self._pkt[69]) +
                                    chr(self._pkt[70]) +
                                    chr(self._pkt[71]) +
                                    chr(self._pkt[72]))
        han_data["obis_m_t"] = (str(self._pkt[75]) +
                                '.' + str(self._pkt[76]) +
                                '.' + str(self._pkt[77]) +
                                '.' + str(self._pkt[78]) +
                                '.' + str(self._pkt[79]) +
                                '.' + str(self._pkt[80]))
        han_data["meter_type"] = (chr(self._pkt[83]) +
                                  chr(self._pkt[84]) +
                                  chr(self._pkt[85]) +
                                  chr(self._pkt[86]) +
                                  chr(self._pkt[87]) +
                                  chr(self._pkt[88]) +
                                  chr(self._pkt[89]) +
                                  chr(self._pkt[90]) +
                                  chr(self._pkt[91]) +
                                  chr(self._pkt[92]) +
                                  chr(self._pkt[93]) +
                                  chr(self._pkt[94]) +
                                  chr(self._pkt[95]) +
                                  chr(self._pkt[96]) +
                                  chr(self._pkt[97]) +
                                  chr(self._pkt[98]) +
                                  chr(self._pkt[99]) +
                                  chr(self._pkt[100]))
        han_data["obis_a_p_p"] = (str(self._pkt[103]) +
                                  '.' + str(self._pkt[104]) +
                                  '.' + str(self._pkt[105]) +
                                  '.' + str(self._pkt[106]) +
                                  '.' + str(self._pkt[107]) +
                                  '.' + str(self._pkt[108]))
        han_data["active_power_p"] = (self._pkt[110] << 24 |
                                      self._pkt[111] << 16 |
                                      self._pkt[112] << 8 |
                                      self._pkt[113])
        han_data["obis_a_p_n"] = (str(self._pkt[116]) +
                                  '.' + str(self._pkt[117]) +
                                  '.' + str(self._pkt[118]) +
                                  '.' + str(self._pkt[119]) +
                                  '.' + str(self._pkt[120]) +
                                  '.' + str(self._pkt[121]))
        han_data["active_power_n"] = (self._pkt[123] << 24 |
                                      self._pkt[124] << 16 |
                                      self._pkt[125] << 8 |
                                      self._pkt[126])
        han_data["obis_r_p_p"] = (str(self._pkt[129]) +
                                  '.' + str(self._pkt[130]) +
                                  '.' + str(self._pkt[131]) +
                                  '.' + str(self._pkt[132]) +
                                  '.' + str(self._pkt[133]) +
                                  '.' + str(self._pkt[134]))
        han_data["reactive_power_p"] = (self._pkt[136] << 24 |
                                        self._pkt[137] << 16 |
                                        self._pkt[138] << 8 |
                                        self._pkt[139])
        han_data["obis_r_p_n"] = (str(self._pkt[142]) +
                                  '.' + str(self._pkt[143]) +
                                  '.' + str(self._pkt[144]) +
                                  '.' + str(self._pkt[145]) +
                                  '.' + str(self._pkt[146]) +
                                  '.' + str(self._pkt[147]))
        han_data["reactive_power_n"] = (self._pkt[149] << 24 |
                                        self._pkt[150] << 16 |
                                        self._pkt[151] << 8 |
                                        self._pkt[152])
        han_data["obis_c_l1"] = (str(self._pkt[155]) +
                                 '.' + str(self._pkt[156]) +
                                 '.' + str(self._pkt[157]) +
                                 '.' + str(self._pkt[158]) +
                                 '.' + str(self._pkt[159]) +
                                 '.' + str(self._pkt[160]))
        han_data["current_l1"] = (self._pkt[162] << 24 |
                                  self._pkt[163] << 16 |
                                  self._pkt[164] << 8 |
                                  self._pkt[165])

        if list_type == LIST_TYPE_SHORT_3PH or LIST_TYPE_LONG_3PH:
            han_data["obis_c_l2"] = (str(self._pkt[168]) +
                                     '.' + str(self._pkt[169]) +
                                     '.' + str(self._pkt[170]) +
                                     '.' + str(self._pkt[171]) +
                                     '.' + str(self._pkt[172]) +
                                     '.' + str(self._pkt[173]))
            han_data["current_l2"] = (self._pkt[175] << 24 |
                                      self._pkt[176] << 16 |
                                      self._pkt[177] << 8 |
                                      self._pkt[178])
            han_data["obis_c_l3"] = (str(self._pkt[181]) +
                                     '.' + str(self._pkt[182]) +
                                     '.' + str(self._pkt[183]) +
                                     '.' + str(self._pkt[184]) +
                                     '.' + str(self._pkt[185]) +
                                     '.' + str(self._pkt[186]))
            han_data["current_l3"] = (self._pkt[188] << 24 |
                                      self._pkt[189] << 16 |
                                      self._pkt[190] << 8 |
                                      self._pkt[191])
            han_data["obis_v_l1"] = (str(self._pkt[194]) +
                                     '.' + str(self._pkt[195]) +
                                     '.' + str(self._pkt[196]) +
                                     '.' + str(self._pkt[197]) +
                                     '.' + str(self._pkt[198]) +
                                     '.' + str(self._pkt[199]))
            han_data["voltage_l1"] = (self._pkt[201] << 8 |
                                      self._pkt[202])
            han_data["obis_v_l2"] = (str(self._pkt[205]) +
                                     '.' + str(self._pkt[206]) +
                                     '.' + str(self._pkt[207]) +
                                     '.' + str(self._pkt[208]) +
                                     '.' + str(self._pkt[209]) +
                                     '.' + str(self._pkt[210]))
            han_data["voltage_l2"] = (self._pkt[212] << 8 |
                                      self._pkt[213])
            han_data["obis_v_l3"] = (str(self._pkt[216]) +
                                     '.' + str(self._pkt[217]) +
                                     '.' + str(self._pkt[218]) +
                                     '.' + str(self._pkt[219]) +
                                     '.' + str(self._pkt[220]) +
                                     '.' + str(self._pkt[221]))
            han_data["voltage_l3"] = (self._pkt[223] << 8 |
                                      self._pkt[224])

        if list_type == LIST_TYPE_SHORT_1PH or LIST_TYPE_LONG_1PH:
            han_data["obis_v_l1"] = (str(self._pkt[168]) +
                                     '.' + str(self._pkt[169]) +
                                     '.' + str(self._pkt[170]) +
                                     '.' + str(self._pkt[171]) +
                                     '.' + str(self._pkt[172]) +
                                     '.' + str(self._pkt[173]))
            han_data["voltage_l1"] = (self._pkt[175] << 8 |
                                      self._pkt[176])

        if list_type == LIST_TYPE_LONG_1PH:
            han_data["obis_date_time2"] = (str(self._pkt[179]) +
                                           '.' + str(self._pkt[180]) +
                                           '.' + str(self._pkt[181]) +
                                           '.' + str(self._pkt[182]) +
                                           '.' + str(self._pkt[183]) +
                                           '.' + str(self._pkt[184]))
            date_time2_year = self._pkt[187] << 8 | self._pkt[188]
            date_time2_month = self._pkt[189]
            date_time2_date = self._pkt[190]
            han_data["meter_day_of_week"] = WEEKDAY_MAPPING.get(self._pkt[191])
            date_time2_hour = str(self._pkt[192]).zfill(2)
            date_time2_minute = str(self._pkt[193]).zfill(2)
            date_time2_seconds = str(self._pkt[194]).zfill(2)
            han_data["meter_date_time"] = (str(date_time2_year) +
                                           '-' + str(date_time2_month) +
                                           '-' + str(date_time2_date) +
                                           ' ' + date_time2_hour +
                                           ':' + date_time2_minute +
                                           ':' + date_time2_seconds)
            han_data["obis_a_e_p"] = (str(self._pkt[201]) +
                                      '.' + str(self._pkt[202]) +
                                      '.' + str(self._pkt[203]) +
                                      '.' + str(self._pkt[204]) +
                                      '.' + str(self._pkt[205]) +
                                      '.' + str(self._pkt[206]))
            han_data["active_energy_p"] = (self._pkt[208] << 24 |
                                           self._pkt[209] << 16 |
                                           self._pkt[210] << 8 |
                                           self._pkt[211])
            han_data["obis_a_e_n"] = (str(self._pkt[214]) +
                                      '.' + str(self._pkt[215]) +
                                      '.' + str(self._pkt[216]) +
                                      '.' + str(self._pkt[217]) +
                                      '.' + str(self._pkt[218]) +
                                      '.' + str(self._pkt[219]))
            han_data["active_energy_n"] = (self._pkt[221] << 24 |
                                           self._pkt[222] << 16 |
                                           self._pkt[223] << 8 |
                                           self._pkt[224])
            han_data["obis_r_e_p"] = (str(self._pkt[227]) +
                                      '.' + str(self._pkt[228]) +
                                      '.' + str(self._pkt[229]) +
                                      '.' + str(self._pkt[230]) +
                                      '.' + str(self._pkt[231]) +
                                      '.' + str(self._pkt[232]))
            han_data["reactive_energy_p"] = (self._pkt[234] << 24 |
                                             self._pkt[235] << 16 |
                                             self._pkt[236] << 8 |
                                             self._pkt[237])
            han_data["obis_r_e_n"] = (str(self._pkt[240]) +
                                      '.' + str(self._pkt[241]) +
                                      '.' + str(self._pkt[242]) +
                                      '.' + str(self._pkt[243]) +
                                      '.' + str(self._pkt[244]) +
                                      '.' + str(self._pkt[245]))
            han_data["reactive_energy_n"] = (self._pkt[247] << 24 |
                                             self._pkt[248] << 16 |
                                             self._pkt[249] << 8 |
                                             self._pkt[250])

        if list_type == LIST_TYPE_LONG_3PH:
            han_data["obis_date_time2"] = (str(self._pkt[227]) +
                                           '.' + str(self._pkt[228]) +
                                           '.' + str(self._pkt[229]) +
                                           '.' + str(self._pkt[230]) +
                                           '.' + str(self._pkt[231]) +
                                           '.' + str(self._pkt[232]))
            date_time2_year = self._pkt[235] << 8 | self._pkt[236]
            date_time2_month = self._pkt[237]
            date_time2_date = self._pkt[238]
            han_data["day_of_week"] = WEEKDAY_MAPPING.get(self._pkt[239])
            date_time2_hour = str(self._pkt[240]).zfill(2)
            date_time2_minute = str(self._pkt[241]).zfill(2)
            date_time2_seconds = str(self._pkt[242]).zfill(2)
            han_data["date_time2"] = (str(date_time2_year) +
                                      '-' + str(date_time2_month) +
                                      '-' + str(date_time2_date) +
                                      ' ' + date_time2_hour +
                                      ':' + date_time2_minute +
                                      ':' + date_time2_seconds)
            han_data["obis_a_e_p"] = (str(self._pkt[249]) +
                                      '.' + str(self._pkt[250]) +
                                      '.' + str(self._pkt[251]) +
                                      '.' + str(self._pkt[252]) +
                                      '.' + str(self._pkt[253]) +
                                      '.' + str(self._pkt[254]))
            han_data["active_energy_p"] = (self._pkt[256] << 24 |
                                           self._pkt[257] << 16 |
                                           self._pkt[258] << 8 |
                                           self._pkt[259])
            han_data["obis_a_e_n"] = (str(self._pkt[262]) +
                                      '.' + str(self._pkt[263]) +
                                      '.' + str(self._pkt[264]) +
                                      '.' + str(self._pkt[265]) +
                                      '.' + str(self._pkt[266]) +
                                      '.' + str(self._pkt[267]))
            han_data["active_energy_n"] = (self._pkt[269] << 24 |
                                           self._pkt[270] << 16 |
                                           self._pkt[271] << 8 |
                                           self._pkt[272])
            han_data["obis_r_e_p"] = (str(self._pkt[275]) +
                                      '.' + str(self._pkt[276]) +
                                      '.' + str(self._pkt[277]) +
                                      '.' + str(self._pkt[278]) +
                                      '.' + str(self._pkt[279]) +
                                      '.' + str(self._pkt[280]))
            han_data["reactive_energy_p"] = (self._pkt[282] << 24 |
                                             self._pkt[283] << 16 |
                                             self._pkt[284] << 8 |
                                             self._pkt[285])
            han_data["obis_r_e_n"] = (str(self._pkt[288]) +
                                      '.' + str(self._pkt[289]) +
                                      '.' + str(self._pkt[290]) +
                                      '.' + str(self._pkt[291]) +
                                      '.' + str(self._pkt[292]) +
                                      '.' + str(self._pkt[293]))
            han_data["reactive_energy_n"] = (self._pkt[295] << 24 |
                                             self._pkt[296] << 16 |
                                             self._pkt[297] << 8 |
                                             self._pkt[298])
        return json.dumps(han_data)


if __name__ == '__main__':
    APP = HanPowermeter()

    while True:
        try:
            RAW_BYTES = APP.read_bytes()
            if APP.test_valid_data(RAW_BYTES):
                PROCESSED_DATA = APP.parse_data(RAW_BYTES)
                print(PROCESSED_DATA)
        except KeyboardInterrupt:
            _LOGGER.error("Killed process on user signal")
            APP.ser.close()
            break
