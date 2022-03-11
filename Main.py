
import argparse
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


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


board.prepare_session()
# board.start_stream () # use this for default options
board.start_stream(45000, None)
time.sleep(2)
# data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
data = board.get_board_data()  # get all data and remove it from internal buffer
board.stop_stream()
board.release_session()

print(data)



# set default display to show all rows and columns:
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
#pd.set_option('display.width', 250)

data = pd.DataFrame(data)


display(data)

#print("Board Description: ", board.get_board_descr(0))
print("Sampling rate: ",board.get_sampling_rate(0))
print("EEG channels: ",board.get_eeg_channels(0))
print("Accel. channels: ",board.get_accel_channels(0))
print("Other channels: ",board.get_other_channels(0))
print("timestamp channel: ", board.get_timestamp_channel(0))


import datetime

def float_to_datetime(fl):
    return datetime.datetime.fromtimestamp(fl)
    

def getTime(data,t):
    d = data[t][22]
    return datetime.datetime.fromtimestamp(d)
    
def getRecord(data,d):
    print("***************************")
    print("EEG channels at timestamp ")
    print(getTime(data,d))
    print()
    for i in range(1,9):
        print(i, ": ", data[d][i])
    print("***************************")
    
def getChannels(data):
    data = data
    return (data[1:][1:8]).T
        
#getRecord(data,3)


data2 = getChannels(data)
#display(data2)
data2.plot()
plt.show()

