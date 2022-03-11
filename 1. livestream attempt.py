
import argparse
import time
import numpy as np
import pandas as pd
import sys


import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def main():
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.ip_port = 0
    params.serial_port = '/dev/cu.usbserial-DQ007SNX'
    params.mac_address = ''
    params.other_info = ''
    params.serial_number = ''
    params.ip_address = ''
    params.ip_protocol = 0
    params.timeout = 0
    params.file = ''
    

    board = BoardShim(0, params)
    #board.prepare_session()
    # board.start_stream () # use this for default options
    board.start_stream(45000, None)
    time.sleep(10)
    # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    data = board.get_board_data()  # get all data and remove it from internal buffer
    board.stop_stream()
    board.release_session()

    print(data)
    

if __name__ == "__main__":
    main()


#########################################################################
###########################################################################
###################################################################
#################################################################

print(data)

def main():
    BoardShim.enable_dev_board_logger()

    # use synthetic board for demo
    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(10)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    # demo how to convert it to pandas DF and plot data
    eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
    df = pd.DataFrame(np.transpose(data))
    print('Data From the Board')
    print(df.head(1))
    
    # demo for data serialization using brainflow API, we recommend to use it instead pandas.to_csv()
    #DataFilter.write_file(data, 'test.csv', 'w')  # use 'a' for append mode
    #restored_data = DataFilter.read_file('test.csv')
    #restored_df = pd.DataFrame(np.transpose(restored_data))
    #print('Data From the File')
    #print(restored_df.head(10))


if __name__ == "__main__":
    main()



    parser = argparse.ArgumentParser()
    # use docs to check which parameters are required for specific board, e.g. for Cyton - set serial port
    parser.add_argument('--timeout', type=int, help='timeout for device discovery or connection', required=False,
                        default=0)
    parser.add_argument('--ip-port', type=int, help='ip port', required=False, default=0)
    parser.add_argument('--ip-protocol', type=int, help='ip protocol, check IpProtocolType enum', required=False,
                        default=0)
    parser.add_argument('--ip-address', type=str, help='ip address', required=False, default='')
    parser.add_argument('--serial-port', type=str, help='serial port', required=False, default='/dev/cu.usbserial-DQ007SNX')
    parser.add_argument('--mac-address', type=str, help='mac address', required=False, default='')
    parser.add_argument('--other-info', type=str, help='other info', required=False, default='')
    parser.add_argument('--streamer-params', type=str, help='streamer params', required=False, default='')
    parser.add_argument('--serial-number', type=str, help='serial number', required=False, default='')
    parser.add_argument('--board-id', type=int, help='board id, check docs to get a list of supported boards',
                        required=True, default=0)
    parser.add_argument('--file', type=str, help='file', required=False, default='')
    
    
    args = parser.parse_args()

    params = BrainFlowInputParams()
    params.ip_port = args.ip_port
    params.serial_port = args.serial_port
    params.mac_address = args.mac_address
    params.other_info = args.other_info
    params.serial_number = args.serial_number
    params.ip_address = args.ip_address
    params.ip_protocol = args.ip_protocol
    params.timeout = args.timeout
    params.file = args.file
    
    params = BrainFlowInputParams()
    params.ip_port = 0
    params.serial_port = '/dev/cu.usbserial-DQ007SNX'
    params.mac_address = ''
    params.other_info = ''
    params.serial_number = ''
    params.ip_address = ''
    params.ip_protocol = 0
    params.timeout = ''
    params.file = ''

