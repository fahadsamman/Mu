#import argparse
#import time
import logging
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, DetrendOperations

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

# This class is a template from brainflow
# for plotting live EEG data.
class Graph:
    def __init__(self, board_shim):

        self.board_id = board_shim.get_board_id()
        self.board_shim = board_shim
        self.exg_channels = BoardShim.get_exg_channels(self.board_id)
        self.sampling_rate = BoardShim.get_sampling_rate(self.board_id)
        self.update_speed_ms = 50
        self.window_size = 4
        self.num_points = self.window_size * self.sampling_rate

        self.app = QtGui.QApplication.instance()
        if self.app == None:
            self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title='BrainFlow Plot', size=(800, 600))

        self._init_timeseries()

        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(self.update_speed_ms)
        QtGui.QApplication.instance().exec_()

    def _init_timeseries(self):
        self.plots = list()
        self.curves = list()
        for i in range(len(self.exg_channels)):
            p = self.win.addPlot(row=i, col=0)
            p.showAxis('left', False)
            p.setMenuEnabled('left', False)
            p.showAxis('bottom', False)
            p.setMenuEnabled('bottom', False)
            if i == 0:
                p.setTitle('TimeSeries Plot')
            self.plots.append(p)
            curve = p.plot()
            self.curves.append(curve)

    def update(self):
        data = self.board_shim.get_current_board_data(self.num_points)

        # 'a' to append, 'w' to just overwrite:
        # file size grows too fast. keep commented for now.
        #DataFilter.write_file(data, 'test.csv', 'a')

        for count, channel in enumerate(self.exg_channels):
            # plot timeseries
            DataFilter.detrend(data[channel], DetrendOperations.CONSTANT.value)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandpass(data[channel], self.sampling_rate, 51.0, 100.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 50.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            DataFilter.perform_bandstop(data[channel], self.sampling_rate, 60.0, 4.0, 2,
                                        FilterTypes.BUTTERWORTH.value, 0)
            self.curves[count].setData(data[channel].tolist())

        self.app.processEvents()


def main():
    BoardShim.enable_dev_board_logger()

    # params have been given default values to avoid the headache of using 'argparse':
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

    #not sure how necessary the try block is...
    try:
        board = BoardShim(0, params)
        board.prepare_session()
        # board.start_stream () # use this for default options
        board.start_stream(45000, None)
        Graph(board) # Live plot
    except BaseException:
        logging.warning('Exception', exc_info=True)
    finally:
        logging.info('End')
        if board.is_prepared():
            logging.info('Releasing session')
            board.release_session()

    # time.sleep(2)
    # data = board.get_current_board_data (256) # get latest 256 packages or less, doesnt remove them from internal buffer
    # data = board.get_board_data()  # get all data and remove it from internal buffer
    # board.stop_stream()
    # board.release_session()
    # board = BoardShim(0, params)


if __name__ == '__main__':
    main()




# Some descriptions:
#print("Board Description: ", board.get_board_descr(0))
#print("Sampling rate: ",board.get_sampling_rate(0))
#print("EEG channels: ",board.get_eeg_channels(0))
#print("Accel. channels: ",board.get_accel_channels(0))
#print("Other channels: ",board.get_other_channels(0))
#print("timestamp channel: ", board.get_timestamp_channel(0))



# Test methods:

import datetime

def float_to_datetime(fl):
    return datetime.datetime.fromtimestamp(fl)


def getTime(data, t):
    d = data[t][22]
    return datetime.datetime.fromtimestamp(d)


def getRecord(data, d):
    print("***************************")
    print("EEG channels at timestamp ")
    print(getTime(data, d))
    print()
    for i in range(1, 9):
        print(i, ": ", data[d][i])
    print("***************************")

