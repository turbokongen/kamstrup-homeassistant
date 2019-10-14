"""
Module that reads data from an Mbus serial adapter.

It decodes the incoming data and output json formatted dict.
"""

import datetime
import logging
from time import sleep
import han_decode
import serial
from crccheck.crc import CrcX25

BAUDRATE = 2400
DATA_FLAG = [230, 231, 0, 15]
FRAME_FLAG = b'\x7e'
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
        self.han_data = {}

    def test_valid_data(self, data):
        """Test the incoming data for validity."""
        # pylint: disable=too-many-return-statements
        if len(data) > 302 or len(data) < 180:
            _LOGGER.warning('Invalid packet size %s', len(data))
            return False

        if not data[0] and data[-1] == FRAME_FLAG:
            _LOGGER.warning("%s Recieved %s bytes of %s data",
                            datetime.datetime.now().isoformat(),
                            len(data), False)
            return False

        header_checksum = CrcX25.calc(bytes(data[1:6]))
        read_header_checksum = (data[7] << 8 | data[6])

        if header_checksum != read_header_checksum:
            _LOGGER.warning('Invalid header CRC check')
            return False

        frame_checksum = CrcX25.calc(bytes(data[1:-3]))
        read_frame_checksum = (data[-2] << 8 | data[-3])

        if frame_checksum != read_frame_checksum:
            _LOGGER.warning('Invalid frame CRC check')
            return False

        if data[8:12] != DATA_FLAG:
            _LOGGER.warning('Data does not start with %s: %s',
                            DATA_FLAG, data[8:12])
            return False

        packet_size = len(data)
        read_packet_size = ((data[1] & 0x0F) << 8 | data[2]) + 2

        if packet_size != read_packet_size:
            _LOGGER.warning(
                'Packet size does not match read packet size: %s : %s',
                packet_size, read_packet_size)
            return False
        return True

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


if __name__ == '__main__':
    APP = HanPowermeter()
    han_data = {}

    while True:
        try:
            RAW_BYTES = APP.read_bytes()
            if APP.test_valid_data(RAW_BYTES):
                PROCESSED_DATA = han_decode.parse_data(han_data, RAW_BYTES)
                print(PROCESSED_DATA)
        except KeyboardInterrupt:
            _LOGGER.error("Killed process on user signal")
            APP.ser.close()
            break
