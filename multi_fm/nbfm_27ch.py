#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: 27 Channel FM Receiver
# Author: John Ackermann   N8UR   jra@febo.com
# Description: Derived from work by Chris Kuethe <chris.kuethe+github@gmail.com>
# Generated: Sat Jun  3 16:30:56 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from nbfm_block_9ch import nbfm_block_9ch  # grc-generated hier_block
from optparse import OptionParser
import osmosdr
import sip
import time
from gnuradio import qtgui


class nbfm_27ch(gr.top_block, Qt.QWidget):

    def __init__(self, ch0_init=146.61e6, ch_spacing_init=30):
        gr.top_block.__init__(self, "27 Channel FM Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("27 Channel FM Receiver")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "nbfm_27ch")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.ch0_init = ch0_init
        self.ch_spacing_init = ch_spacing_init

        ##################################################
        # Variables
        ##################################################
        self.num_chans = num_chans = 27
        self.ch_spacing = ch_spacing = ch_spacing_init * 1000
        self.ch0_freq = ch0_freq = ch0_init
        self.sample_width = sample_width = ch_spacing * (num_chans + 1)
        self.band_start = band_start = ch0_freq - ch_spacing
        self.hardware_rate = hardware_rate = sample_width * 2
        self.band_end = band_end = band_start + ((num_chans +1) * ch_spacing)
        self.tuner_freq = tuner_freq = band_start - (0.1* hardware_rate)
        self.fm_dev = fm_dev = int(5e3)
        self.channel_map = channel_map = range(0, num_chans)
        self.band_center = band_center = band_start + ((band_end - band_start)/2)
        self.volume = volume = 0.4
        self.tuner_offset = tuner_offset = band_center - tuner_freq
        self.squelch = squelch = -40
        self.sq_ramp = sq_ramp = 1
        self.sq_alpha = sq_alpha = 0.0005
        self.rf_gain = rf_gain = 25
        self.ppm_corr = ppm_corr = 0
        self.pfb_taps = pfb_taps = firdes.low_pass(2.0, sample_width, ((fm_dev*2)+3e3),2500, firdes.WIN_HAMMING, 6.76)
        self.lpf_taps = lpf_taps = firdes.low_pass(1.0, hardware_rate, sample_width/2,ch_spacing, firdes.WIN_HAMMING, 6.76)
        self.decimation = decimation = 2
        self.channelizer_map = channelizer_map = 14,15,16,17,18,19,20,21,22,23,24,25,26,0,1,2,3,4,5,6,7,8,9,10,11,12,13
        self.channel_names = channel_names = map( lambda x: "%.3fMHz" % ( (ch0_freq+ (x*ch_spacing))/1e6) , channel_map)
        self.ch9_mute = ch9_mute = 1
        self.ch8_mute = ch8_mute = 1
        self.ch7_mute = ch7_mute = 1
        self.ch6_mute = ch6_mute = 1
        self.ch5_mute = ch5_mute = 1
        self.ch4_mute = ch4_mute = 1
        self.ch3_mute = ch3_mute = 1
        self.ch2_mute = ch2_mute = 1
        self.ch26_mute = ch26_mute = 1
        self.ch25_mute = ch25_mute = 1
        self.ch24_mute = ch24_mute = 1
        self.ch23_mute = ch23_mute = 1
        self.ch22_mute = ch22_mute = 1
        self.ch21_mute = ch21_mute = 1
        self.ch20_mute = ch20_mute = 1
        self.ch1_mute = ch1_mute = 1
        self.ch19_mute = ch19_mute = 1
        self.ch18_mute = ch18_mute = 1
        self.ch17_mute = ch17_mute = 1
        self.ch16_mute = ch16_mute = 1
        self.ch15_mute = ch15_mute = 1
        self.ch14_mute = ch14_mute = 1
        self.ch13_mute = ch13_mute = 1
        self.ch12_mute = ch12_mute = 1
        self.ch11_mute = ch11_mute = 1
        self.ch10_mute = ch10_mute = 1
        self.ch0_mute = ch0_mute = 1
        self.audio_hw_rate = audio_hw_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 1, 0.01, 0.4, 50)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, 'Volume', "slider", float)
        self.top_grid_layout.addWidget(self._volume_win, 0,5,1,2)
        self._squelch_range = Range(-60, -20, 2, -40, 50)
        self._squelch_win = RangeWidget(self._squelch_range, self.set_squelch, 'Squelch', "slider", float)
        self.top_grid_layout.addWidget(self._squelch_win, 0,7,1,2)
        self._rf_gain_range = Range(0, 50, 1, 25, 50)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, 'RF Gain', "slider", int)
        self.top_grid_layout.addWidget(self._rf_gain_win, 0,3,1,2)
        self._ppm_corr_range = Range(-60, 60, 1, 0, 50)
        self._ppm_corr_win = RangeWidget(self._ppm_corr_range, self.set_ppm_corr, 'PPM Corr.', "slider", float)
        self.top_grid_layout.addWidget(self._ppm_corr_win, 0,9,1,2)
        self._ch_spacing_options = (15000, 20000, 25000, 30000, 50000, )
        self._ch_spacing_labels = ('15 kHz', '20 kHz', '25 kHz', '30 kHz', '50 kHz', )
        self._ch_spacing_tool_bar = Qt.QToolBar(self)
        self._ch_spacing_tool_bar.addWidget(Qt.QLabel('Spacing'+": "))
        self._ch_spacing_combo_box = Qt.QComboBox()
        self._ch_spacing_tool_bar.addWidget(self._ch_spacing_combo_box)
        for label in self._ch_spacing_labels: self._ch_spacing_combo_box.addItem(label)
        self._ch_spacing_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch_spacing_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ch_spacing_options.index(i)))
        self._ch_spacing_callback(self.ch_spacing)
        self._ch_spacing_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_ch_spacing(self._ch_spacing_options[i]))
        self.top_grid_layout.addWidget(self._ch_spacing_tool_bar, 0,2,1,1)
        self._ch9_mute_options = (0, 1, )
        self._ch9_mute_labels = ('Mute', 'Unmute', )
        self._ch9_mute_group_box = Qt.QGroupBox(channel_names[9])
        self._ch9_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch9_mute_button_group = variable_chooser_button_group()
        self._ch9_mute_group_box.setLayout(self._ch9_mute_box)
        for i, label in enumerate(self._ch9_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch9_mute_box.addWidget(radio_button)
        	self._ch9_mute_button_group.addButton(radio_button, i)
        self._ch9_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch9_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch9_mute_options.index(i)))
        self._ch9_mute_callback(self.ch9_mute)
        self._ch9_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch9_mute(self._ch9_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch9_mute_group_box, 1,9,1,1)
        self._ch8_mute_options = (0, 1, )
        self._ch8_mute_labels = ('Mute', 'Unmute', )
        self._ch8_mute_group_box = Qt.QGroupBox(channel_names[8])
        self._ch8_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch8_mute_button_group = variable_chooser_button_group()
        self._ch8_mute_group_box.setLayout(self._ch8_mute_box)
        for i, label in enumerate(self._ch8_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch8_mute_box.addWidget(radio_button)
        	self._ch8_mute_button_group.addButton(radio_button, i)
        self._ch8_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch8_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch8_mute_options.index(i)))
        self._ch8_mute_callback(self.ch8_mute)
        self._ch8_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch8_mute(self._ch8_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch8_mute_group_box, 1,8,1,1)
        self._ch7_mute_options = (0, 1, )
        self._ch7_mute_labels = ('Mute', 'Unmute', )
        self._ch7_mute_group_box = Qt.QGroupBox(channel_names[7])
        self._ch7_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch7_mute_button_group = variable_chooser_button_group()
        self._ch7_mute_group_box.setLayout(self._ch7_mute_box)
        for i, label in enumerate(self._ch7_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch7_mute_box.addWidget(radio_button)
        	self._ch7_mute_button_group.addButton(radio_button, i)
        self._ch7_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch7_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch7_mute_options.index(i)))
        self._ch7_mute_callback(self.ch7_mute)
        self._ch7_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch7_mute(self._ch7_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch7_mute_group_box, 1,7,1,1)
        self._ch6_mute_options = (0, 1, )
        self._ch6_mute_labels = ('Mute', 'Unmute', )
        self._ch6_mute_group_box = Qt.QGroupBox(channel_names[6])
        self._ch6_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch6_mute_button_group = variable_chooser_button_group()
        self._ch6_mute_group_box.setLayout(self._ch6_mute_box)
        for i, label in enumerate(self._ch6_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch6_mute_box.addWidget(radio_button)
        	self._ch6_mute_button_group.addButton(radio_button, i)
        self._ch6_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch6_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch6_mute_options.index(i)))
        self._ch6_mute_callback(self.ch6_mute)
        self._ch6_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch6_mute(self._ch6_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch6_mute_group_box, 1,6,1,1)
        self._ch5_mute_options = (0, 1, )
        self._ch5_mute_labels = ('Mute', 'Unmute', )
        self._ch5_mute_group_box = Qt.QGroupBox(channel_names[5])
        self._ch5_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch5_mute_button_group = variable_chooser_button_group()
        self._ch5_mute_group_box.setLayout(self._ch5_mute_box)
        for i, label in enumerate(self._ch5_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch5_mute_box.addWidget(radio_button)
        	self._ch5_mute_button_group.addButton(radio_button, i)
        self._ch5_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch5_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch5_mute_options.index(i)))
        self._ch5_mute_callback(self.ch5_mute)
        self._ch5_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch5_mute(self._ch5_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch5_mute_group_box, 1,5,1,1)
        self._ch4_mute_options = (0, 1, )
        self._ch4_mute_labels = ('Mute', 'Unmute', )
        self._ch4_mute_group_box = Qt.QGroupBox(channel_names[4])
        self._ch4_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch4_mute_button_group = variable_chooser_button_group()
        self._ch4_mute_group_box.setLayout(self._ch4_mute_box)
        for i, label in enumerate(self._ch4_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch4_mute_box.addWidget(radio_button)
        	self._ch4_mute_button_group.addButton(radio_button, i)
        self._ch4_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch4_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch4_mute_options.index(i)))
        self._ch4_mute_callback(self.ch4_mute)
        self._ch4_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch4_mute(self._ch4_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch4_mute_group_box, 1,4,1,1)
        self._ch3_mute_options = (0, 1, )
        self._ch3_mute_labels = ('Mute', 'Unmute', )
        self._ch3_mute_group_box = Qt.QGroupBox(channel_names[3])
        self._ch3_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch3_mute_button_group = variable_chooser_button_group()
        self._ch3_mute_group_box.setLayout(self._ch3_mute_box)
        for i, label in enumerate(self._ch3_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch3_mute_box.addWidget(radio_button)
        	self._ch3_mute_button_group.addButton(radio_button, i)
        self._ch3_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch3_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch3_mute_options.index(i)))
        self._ch3_mute_callback(self.ch3_mute)
        self._ch3_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch3_mute(self._ch3_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch3_mute_group_box, 1,3,1,1)
        self._ch2_mute_options = (0, 1, )
        self._ch2_mute_labels = ('Mute', 'Unmute', )
        self._ch2_mute_group_box = Qt.QGroupBox(channel_names[2])
        self._ch2_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch2_mute_button_group = variable_chooser_button_group()
        self._ch2_mute_group_box.setLayout(self._ch2_mute_box)
        for i, label in enumerate(self._ch2_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch2_mute_box.addWidget(radio_button)
        	self._ch2_mute_button_group.addButton(radio_button, i)
        self._ch2_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch2_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch2_mute_options.index(i)))
        self._ch2_mute_callback(self.ch2_mute)
        self._ch2_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch2_mute(self._ch2_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch2_mute_group_box, 1,2,1,1)
        self._ch26_mute_options = (0, 1, )
        self._ch26_mute_labels = ('Mute', 'Unmute', )
        self._ch26_mute_group_box = Qt.QGroupBox(channel_names[26])
        self._ch26_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch26_mute_button_group = variable_chooser_button_group()
        self._ch26_mute_group_box.setLayout(self._ch26_mute_box)
        for i, label in enumerate(self._ch26_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch26_mute_box.addWidget(radio_button)
        	self._ch26_mute_button_group.addButton(radio_button, i)
        self._ch26_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch26_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch26_mute_options.index(i)))
        self._ch26_mute_callback(self.ch26_mute)
        self._ch26_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch26_mute(self._ch26_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch26_mute_group_box, 3,4,1,1)
        self._ch25_mute_options = (0, 1, )
        self._ch25_mute_labels = ('Mute', 'Unmute', )
        self._ch25_mute_group_box = Qt.QGroupBox(channel_names[25])
        self._ch25_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch25_mute_button_group = variable_chooser_button_group()
        self._ch25_mute_group_box.setLayout(self._ch25_mute_box)
        for i, label in enumerate(self._ch25_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch25_mute_box.addWidget(radio_button)
        	self._ch25_mute_button_group.addButton(radio_button, i)
        self._ch25_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch25_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch25_mute_options.index(i)))
        self._ch25_mute_callback(self.ch25_mute)
        self._ch25_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch25_mute(self._ch25_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch25_mute_group_box, 3,3,1,1)
        self._ch24_mute_options = (0, 1, )
        self._ch24_mute_labels = ('Mute', 'Unmute', )
        self._ch24_mute_group_box = Qt.QGroupBox(channel_names[24])
        self._ch24_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch24_mute_button_group = variable_chooser_button_group()
        self._ch24_mute_group_box.setLayout(self._ch24_mute_box)
        for i, label in enumerate(self._ch24_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch24_mute_box.addWidget(radio_button)
        	self._ch24_mute_button_group.addButton(radio_button, i)
        self._ch24_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch24_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch24_mute_options.index(i)))
        self._ch24_mute_callback(self.ch24_mute)
        self._ch24_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch24_mute(self._ch24_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch24_mute_group_box, 3,2,1,1)
        self._ch23_mute_options = (0, 1, )
        self._ch23_mute_labels = ('Mute', 'Unmute', )
        self._ch23_mute_group_box = Qt.QGroupBox(channel_names[23])
        self._ch23_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch23_mute_button_group = variable_chooser_button_group()
        self._ch23_mute_group_box.setLayout(self._ch23_mute_box)
        for i, label in enumerate(self._ch23_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch23_mute_box.addWidget(radio_button)
        	self._ch23_mute_button_group.addButton(radio_button, i)
        self._ch23_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch23_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch23_mute_options.index(i)))
        self._ch23_mute_callback(self.ch23_mute)
        self._ch23_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch23_mute(self._ch23_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch23_mute_group_box, 3,1,1,1)
        self._ch22_mute_options = (0, 1, )
        self._ch22_mute_labels = ('Mute', 'Unmute', )
        self._ch22_mute_group_box = Qt.QGroupBox(channel_names[22])
        self._ch22_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch22_mute_button_group = variable_chooser_button_group()
        self._ch22_mute_group_box.setLayout(self._ch22_mute_box)
        for i, label in enumerate(self._ch22_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch22_mute_box.addWidget(radio_button)
        	self._ch22_mute_button_group.addButton(radio_button, i)
        self._ch22_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch22_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch22_mute_options.index(i)))
        self._ch22_mute_callback(self.ch22_mute)
        self._ch22_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch22_mute(self._ch22_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch22_mute_group_box, 3,0,1,1)
        self._ch21_mute_options = (0, 1, )
        self._ch21_mute_labels = ('Mute', 'Unmute', )
        self._ch21_mute_group_box = Qt.QGroupBox(channel_names[21])
        self._ch21_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch21_mute_button_group = variable_chooser_button_group()
        self._ch21_mute_group_box.setLayout(self._ch21_mute_box)
        for i, label in enumerate(self._ch21_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch21_mute_box.addWidget(radio_button)
        	self._ch21_mute_button_group.addButton(radio_button, i)
        self._ch21_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch21_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch21_mute_options.index(i)))
        self._ch21_mute_callback(self.ch21_mute)
        self._ch21_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch21_mute(self._ch21_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch21_mute_group_box, 2,10,1,1)
        self._ch20_mute_options = (0, 1, )
        self._ch20_mute_labels = ('Mute', 'Unmute', )
        self._ch20_mute_group_box = Qt.QGroupBox(channel_names[20])
        self._ch20_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch20_mute_button_group = variable_chooser_button_group()
        self._ch20_mute_group_box.setLayout(self._ch20_mute_box)
        for i, label in enumerate(self._ch20_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch20_mute_box.addWidget(radio_button)
        	self._ch20_mute_button_group.addButton(radio_button, i)
        self._ch20_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch20_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch20_mute_options.index(i)))
        self._ch20_mute_callback(self.ch20_mute)
        self._ch20_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch20_mute(self._ch20_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch20_mute_group_box, 2,9,1,1)
        self._ch1_mute_options = (0, 1, )
        self._ch1_mute_labels = ('Mute', 'Unmute', )
        self._ch1_mute_group_box = Qt.QGroupBox(channel_names[1])
        self._ch1_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch1_mute_button_group = variable_chooser_button_group()
        self._ch1_mute_group_box.setLayout(self._ch1_mute_box)
        for i, label in enumerate(self._ch1_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch1_mute_box.addWidget(radio_button)
        	self._ch1_mute_button_group.addButton(radio_button, i)
        self._ch1_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch1_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch1_mute_options.index(i)))
        self._ch1_mute_callback(self.ch1_mute)
        self._ch1_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch1_mute(self._ch1_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch1_mute_group_box, 1,1,1,1)
        self._ch19_mute_options = (0, 1, )
        self._ch19_mute_labels = ('Mute', 'Unmute', )
        self._ch19_mute_group_box = Qt.QGroupBox(channel_names[19])
        self._ch19_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch19_mute_button_group = variable_chooser_button_group()
        self._ch19_mute_group_box.setLayout(self._ch19_mute_box)
        for i, label in enumerate(self._ch19_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch19_mute_box.addWidget(radio_button)
        	self._ch19_mute_button_group.addButton(radio_button, i)
        self._ch19_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch19_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch19_mute_options.index(i)))
        self._ch19_mute_callback(self.ch19_mute)
        self._ch19_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch19_mute(self._ch19_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch19_mute_group_box, 2,8,1,1)
        self._ch18_mute_options = (0, 1, )
        self._ch18_mute_labels = ('Mute', 'Unmute', )
        self._ch18_mute_group_box = Qt.QGroupBox(channel_names[18])
        self._ch18_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch18_mute_button_group = variable_chooser_button_group()
        self._ch18_mute_group_box.setLayout(self._ch18_mute_box)
        for i, label in enumerate(self._ch18_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch18_mute_box.addWidget(radio_button)
        	self._ch18_mute_button_group.addButton(radio_button, i)
        self._ch18_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch18_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch18_mute_options.index(i)))
        self._ch18_mute_callback(self.ch18_mute)
        self._ch18_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch18_mute(self._ch18_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch18_mute_group_box, 2,7,1,1)
        self._ch17_mute_options = (0, 1, )
        self._ch17_mute_labels = ('Mute', 'Unmute', )
        self._ch17_mute_group_box = Qt.QGroupBox(channel_names[17])
        self._ch17_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch17_mute_button_group = variable_chooser_button_group()
        self._ch17_mute_group_box.setLayout(self._ch17_mute_box)
        for i, label in enumerate(self._ch17_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch17_mute_box.addWidget(radio_button)
        	self._ch17_mute_button_group.addButton(radio_button, i)
        self._ch17_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch17_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch17_mute_options.index(i)))
        self._ch17_mute_callback(self.ch17_mute)
        self._ch17_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch17_mute(self._ch17_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch17_mute_group_box, 2,6,1,1)
        self._ch16_mute_options = (0, 1, )
        self._ch16_mute_labels = ('Mute', 'Unmute', )
        self._ch16_mute_group_box = Qt.QGroupBox(channel_names[16])
        self._ch16_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch16_mute_button_group = variable_chooser_button_group()
        self._ch16_mute_group_box.setLayout(self._ch16_mute_box)
        for i, label in enumerate(self._ch16_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch16_mute_box.addWidget(radio_button)
        	self._ch16_mute_button_group.addButton(radio_button, i)
        self._ch16_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch16_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch16_mute_options.index(i)))
        self._ch16_mute_callback(self.ch16_mute)
        self._ch16_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch16_mute(self._ch16_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch16_mute_group_box, 2,5,1,1)
        self._ch15_mute_options = (0, 1, )
        self._ch15_mute_labels = ('Mute', 'Unmute', )
        self._ch15_mute_group_box = Qt.QGroupBox(channel_names[15])
        self._ch15_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch15_mute_button_group = variable_chooser_button_group()
        self._ch15_mute_group_box.setLayout(self._ch15_mute_box)
        for i, label in enumerate(self._ch15_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch15_mute_box.addWidget(radio_button)
        	self._ch15_mute_button_group.addButton(radio_button, i)
        self._ch15_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch15_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch15_mute_options.index(i)))
        self._ch15_mute_callback(self.ch15_mute)
        self._ch15_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch15_mute(self._ch15_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch15_mute_group_box, 2,4,1,1)
        self._ch14_mute_options = (0, 1, )
        self._ch14_mute_labels = ('Mute', 'Unmute', )
        self._ch14_mute_group_box = Qt.QGroupBox(channel_names[14])
        self._ch14_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch14_mute_button_group = variable_chooser_button_group()
        self._ch14_mute_group_box.setLayout(self._ch14_mute_box)
        for i, label in enumerate(self._ch14_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch14_mute_box.addWidget(radio_button)
        	self._ch14_mute_button_group.addButton(radio_button, i)
        self._ch14_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch14_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch14_mute_options.index(i)))
        self._ch14_mute_callback(self.ch14_mute)
        self._ch14_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch14_mute(self._ch14_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch14_mute_group_box, 2,3,1,1)
        self._ch13_mute_options = (0, 1, )
        self._ch13_mute_labels = ('Mute', 'Unmute', )
        self._ch13_mute_group_box = Qt.QGroupBox(channel_names[13])
        self._ch13_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch13_mute_button_group = variable_chooser_button_group()
        self._ch13_mute_group_box.setLayout(self._ch13_mute_box)
        for i, label in enumerate(self._ch13_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch13_mute_box.addWidget(radio_button)
        	self._ch13_mute_button_group.addButton(radio_button, i)
        self._ch13_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch13_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch13_mute_options.index(i)))
        self._ch13_mute_callback(self.ch13_mute)
        self._ch13_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch13_mute(self._ch13_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch13_mute_group_box, 2,2,1,1)
        self._ch12_mute_options = (0, 1, )
        self._ch12_mute_labels = ('Mute', 'Unmute', )
        self._ch12_mute_group_box = Qt.QGroupBox(channel_names[12])
        self._ch12_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch12_mute_button_group = variable_chooser_button_group()
        self._ch12_mute_group_box.setLayout(self._ch12_mute_box)
        for i, label in enumerate(self._ch12_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch12_mute_box.addWidget(radio_button)
        	self._ch12_mute_button_group.addButton(radio_button, i)
        self._ch12_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch12_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch12_mute_options.index(i)))
        self._ch12_mute_callback(self.ch12_mute)
        self._ch12_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch12_mute(self._ch12_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch12_mute_group_box, 2,1,1,1)
        self._ch11_mute_options = (0, 1, )
        self._ch11_mute_labels = ('Mute', 'Unmute', )
        self._ch11_mute_group_box = Qt.QGroupBox(channel_names[11])
        self._ch11_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch11_mute_button_group = variable_chooser_button_group()
        self._ch11_mute_group_box.setLayout(self._ch11_mute_box)
        for i, label in enumerate(self._ch11_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch11_mute_box.addWidget(radio_button)
        	self._ch11_mute_button_group.addButton(radio_button, i)
        self._ch11_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch11_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch11_mute_options.index(i)))
        self._ch11_mute_callback(self.ch11_mute)
        self._ch11_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch11_mute(self._ch11_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch11_mute_group_box, 2,0,1,1)
        self._ch10_mute_options = (0, 1, )
        self._ch10_mute_labels = ('Mute', 'Unmute', )
        self._ch10_mute_group_box = Qt.QGroupBox(channel_names[10])
        self._ch10_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch10_mute_button_group = variable_chooser_button_group()
        self._ch10_mute_group_box.setLayout(self._ch10_mute_box)
        for i, label in enumerate(self._ch10_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch10_mute_box.addWidget(radio_button)
        	self._ch10_mute_button_group.addButton(radio_button, i)
        self._ch10_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch10_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch10_mute_options.index(i)))
        self._ch10_mute_callback(self.ch10_mute)
        self._ch10_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch10_mute(self._ch10_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch10_mute_group_box, 1,10,1,1)
        self._ch0_mute_options = (0, 1, )
        self._ch0_mute_labels = ('Mute', 'Unmute', )
        self._ch0_mute_group_box = Qt.QGroupBox(channel_names[0])
        self._ch0_mute_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ch0_mute_button_group = variable_chooser_button_group()
        self._ch0_mute_group_box.setLayout(self._ch0_mute_box)
        for i, label in enumerate(self._ch0_mute_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._ch0_mute_box.addWidget(radio_button)
        	self._ch0_mute_button_group.addButton(radio_button, i)
        self._ch0_mute_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ch0_mute_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ch0_mute_options.index(i)))
        self._ch0_mute_callback(self.ch0_mute)
        self._ch0_mute_button_group.buttonClicked[int].connect(
        	lambda i: self.set_ch0_mute(self._ch0_mute_options[i]))
        self.top_grid_layout.addWidget(self._ch0_mute_group_box, 1,0,1,1)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_clock_source('internal', 0)
        self.rtlsdr_source_0.set_sample_rate(hardware_rate)
        self.rtlsdr_source_0.set_center_freq(tuner_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(rf_gain, 0)
        self.rtlsdr_source_0.set_if_gain(30, 0)
        self.rtlsdr_source_0.set_bb_gain(40, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=audio_hw_rate,
                decimation=ch_spacing,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0_0_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	band_center, #fc
        	num_chans * ch_spacing, #bw
        	"Band Monitor", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(0.05)
        self.qtgui_waterfall_sink_x_0_0_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [5, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0.set_intensity_range(-100, 0)

        self._qtgui_waterfall_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_0_win, 4,0,1,9)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	audio_hw_rate, #samp_rate
        	'Audio Output', #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['Audio Out', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 5,0,1,9)
        self.pfb_channelizer_ccf = pfb.channelizer_ccf(
        	  num_chans,
        	  (pfb_taps),
        	  1.0,
        	  1)
        self.pfb_channelizer_ccf.set_channel_map((channelizer_map))
        self.pfb_channelizer_ccf.declare_sample_delay(0)

        self.nbfm_block_9ch_2 = nbfm_block_9ch(
            audio_rate=ch_spacing,
            fm_dev=fm_dev,
            mute0=ch18_mute,
            mute1=ch19_mute,
            mute2=ch20_mute,
            mute3=ch21_mute,
            mute4=ch22_mute,
            mute5=ch23_mute,
            mute6=ch24_mute,
            mute7=ch25_mute,
            mute8=ch26_mute,
            quad_rate=ch_spacing,
            sq_alpha=sq_alpha,
            sq_ramp=sq_ramp,
            squelch=squelch,
        )
        self.nbfm_block_9ch_1 = nbfm_block_9ch(
            audio_rate=ch_spacing,
            fm_dev=fm_dev,
            mute0=ch9_mute,
            mute1=ch10_mute,
            mute2=ch11_mute,
            mute3=ch12_mute,
            mute4=ch13_mute,
            mute5=ch14_mute,
            mute6=ch15_mute,
            mute7=ch16_mute,
            mute8=ch17_mute,
            quad_rate=ch_spacing,
            sq_alpha=sq_alpha,
            sq_ramp=sq_ramp,
            squelch=squelch,
        )
        self.nbfm_block_9ch_0 = nbfm_block_9ch(
            audio_rate=ch_spacing,
            fm_dev=fm_dev,
            mute0=ch0_mute,
            mute1=ch1_mute,
            mute2=ch2_mute,
            mute3=ch3_mute,
            mute4=ch4_mute,
            mute5=ch5_mute,
            mute6=ch6_mute,
            mute7=ch7_mute,
            mute8=ch8_mute,
            quad_rate=ch_spacing,
            sq_alpha=sq_alpha,
            sq_ramp=sq_ramp,
            squelch=squelch,
        )
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(decimation, (lpf_taps), tuner_offset  + ppm_corr, hardware_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self._ch0_freq_tool_bar = Qt.QToolBar(self)
        self._ch0_freq_tool_bar.addWidget(Qt.QLabel('Ch0 Freq'+": "))
        self._ch0_freq_line_edit = Qt.QLineEdit(str(self.ch0_freq))
        self._ch0_freq_tool_bar.addWidget(self._ch0_freq_line_edit)
        self._ch0_freq_line_edit.returnPressed.connect(
        	lambda: self.set_ch0_freq(eng_notation.str_to_num(str(self._ch0_freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._ch0_freq_tool_bar, 0,0,1,2)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(48000, '', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.pfb_channelizer_ccf, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.qtgui_waterfall_sink_x_0_0_0, 0))
        self.connect((self.nbfm_block_9ch_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.nbfm_block_9ch_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.nbfm_block_9ch_2, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.pfb_channelizer_ccf, 0), (self.nbfm_block_9ch_0, 0))
        self.connect((self.pfb_channelizer_ccf, 1), (self.nbfm_block_9ch_0, 1))
        self.connect((self.pfb_channelizer_ccf, 2), (self.nbfm_block_9ch_0, 2))
        self.connect((self.pfb_channelizer_ccf, 3), (self.nbfm_block_9ch_0, 3))
        self.connect((self.pfb_channelizer_ccf, 4), (self.nbfm_block_9ch_0, 4))
        self.connect((self.pfb_channelizer_ccf, 5), (self.nbfm_block_9ch_0, 5))
        self.connect((self.pfb_channelizer_ccf, 6), (self.nbfm_block_9ch_0, 6))
        self.connect((self.pfb_channelizer_ccf, 7), (self.nbfm_block_9ch_0, 7))
        self.connect((self.pfb_channelizer_ccf, 8), (self.nbfm_block_9ch_0, 8))
        self.connect((self.pfb_channelizer_ccf, 9), (self.nbfm_block_9ch_1, 0))
        self.connect((self.pfb_channelizer_ccf, 10), (self.nbfm_block_9ch_1, 1))
        self.connect((self.pfb_channelizer_ccf, 11), (self.nbfm_block_9ch_1, 2))
        self.connect((self.pfb_channelizer_ccf, 12), (self.nbfm_block_9ch_1, 3))
        self.connect((self.pfb_channelizer_ccf, 13), (self.nbfm_block_9ch_1, 4))
        self.connect((self.pfb_channelizer_ccf, 14), (self.nbfm_block_9ch_1, 5))
        self.connect((self.pfb_channelizer_ccf, 15), (self.nbfm_block_9ch_1, 6))
        self.connect((self.pfb_channelizer_ccf, 16), (self.nbfm_block_9ch_1, 7))
        self.connect((self.pfb_channelizer_ccf, 17), (self.nbfm_block_9ch_1, 8))
        self.connect((self.pfb_channelizer_ccf, 18), (self.nbfm_block_9ch_2, 0))
        self.connect((self.pfb_channelizer_ccf, 19), (self.nbfm_block_9ch_2, 1))
        self.connect((self.pfb_channelizer_ccf, 20), (self.nbfm_block_9ch_2, 2))
        self.connect((self.pfb_channelizer_ccf, 21), (self.nbfm_block_9ch_2, 3))
        self.connect((self.pfb_channelizer_ccf, 22), (self.nbfm_block_9ch_2, 4))
        self.connect((self.pfb_channelizer_ccf, 23), (self.nbfm_block_9ch_2, 5))
        self.connect((self.pfb_channelizer_ccf, 24), (self.nbfm_block_9ch_2, 6))
        self.connect((self.pfb_channelizer_ccf, 25), (self.nbfm_block_9ch_2, 7))
        self.connect((self.pfb_channelizer_ccf, 26), (self.nbfm_block_9ch_2, 8))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "nbfm_27ch")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_ch0_init(self):
        return self.ch0_init

    def set_ch0_init(self, ch0_init):
        self.ch0_init = ch0_init
        self.set_ch0_freq(self.ch0_init)

    def get_ch_spacing_init(self):
        return self.ch_spacing_init

    def set_ch_spacing_init(self, ch_spacing_init):
        self.ch_spacing_init = ch_spacing_init
        self.set_ch_spacing(self.ch_spacing_init * 1000)

    def get_num_chans(self):
        return self.num_chans

    def set_num_chans(self, num_chans):
        self.num_chans = num_chans
        self.set_sample_width(self.ch_spacing * (self.num_chans + 1))
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.band_center, self.num_chans * self.ch_spacing)
        self.set_channel_map(range(0, self.num_chans))
        self.set_band_end(self.band_start + ((self.num_chans +1) * self.ch_spacing))

    def get_ch_spacing(self):
        return self.ch_spacing

    def set_ch_spacing(self, ch_spacing):
        self.ch_spacing = ch_spacing
        self.set_channel_names(map( lambda x: "%.3fMHz" % ( (self.ch0_freq+ (x*self.ch_spacing))/1e6) , self.channel_map))
        self.set_lpf_taps(firdes.low_pass(1.0, self.hardware_rate, self.sample_width/2,self.ch_spacing, firdes.WIN_HAMMING, 6.76)
        )
        self._ch_spacing_callback(self.ch_spacing)
        self.set_sample_width(self.ch_spacing * (self.num_chans + 1))
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.band_center, self.num_chans * self.ch_spacing)
        self.nbfm_block_9ch_2.set_audio_rate(self.ch_spacing)
        self.nbfm_block_9ch_2.set_quad_rate(self.ch_spacing)
        self.nbfm_block_9ch_1.set_audio_rate(self.ch_spacing)
        self.nbfm_block_9ch_1.set_quad_rate(self.ch_spacing)
        self.nbfm_block_9ch_0.set_audio_rate(self.ch_spacing)
        self.nbfm_block_9ch_0.set_quad_rate(self.ch_spacing)
        self.set_band_start(self.ch0_freq - self.ch_spacing)
        self.set_band_end(self.band_start + ((self.num_chans +1) * self.ch_spacing))

    def get_ch0_freq(self):
        return self.ch0_freq

    def set_ch0_freq(self, ch0_freq):
        self.ch0_freq = ch0_freq
        self.set_channel_names(map( lambda x: "%.3fMHz" % ( (self.ch0_freq+ (x*self.ch_spacing))/1e6) , self.channel_map))
        Qt.QMetaObject.invokeMethod(self._ch0_freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.ch0_freq)))
        self.set_band_start(self.ch0_freq - self.ch_spacing)

    def get_sample_width(self):
        return self.sample_width

    def set_sample_width(self, sample_width):
        self.sample_width = sample_width
        self.set_pfb_taps(firdes.low_pass(2.0, self.sample_width, ((self.fm_dev*2)+3e3),2500, firdes.WIN_HAMMING, 6.76))
        self.set_lpf_taps(firdes.low_pass(1.0, self.hardware_rate, self.sample_width/2,self.ch_spacing, firdes.WIN_HAMMING, 6.76)
        )
        self.set_hardware_rate(self.sample_width * 2)

    def get_band_start(self):
        return self.band_start

    def set_band_start(self, band_start):
        self.band_start = band_start
        self.set_tuner_freq(self.band_start - (0.1* self.hardware_rate))
        self.set_band_center(self.band_start + ((self.band_end - self.band_start)/2))
        self.set_band_end(self.band_start + ((self.num_chans +1) * self.ch_spacing))

    def get_hardware_rate(self):
        return self.hardware_rate

    def set_hardware_rate(self, hardware_rate):
        self.hardware_rate = hardware_rate
        self.set_tuner_freq(self.band_start - (0.1* self.hardware_rate))
        self.set_lpf_taps(firdes.low_pass(1.0, self.hardware_rate, self.sample_width/2,self.ch_spacing, firdes.WIN_HAMMING, 6.76)
        )
        self.rtlsdr_source_0.set_sample_rate(self.hardware_rate)

    def get_band_end(self):
        return self.band_end

    def set_band_end(self, band_end):
        self.band_end = band_end
        self.set_band_center(self.band_start + ((self.band_end - self.band_start)/2))

    def get_tuner_freq(self):
        return self.tuner_freq

    def set_tuner_freq(self, tuner_freq):
        self.tuner_freq = tuner_freq
        self.set_tuner_offset(self.band_center - self.tuner_freq)
        self.rtlsdr_source_0.set_center_freq(self.tuner_freq, 0)

    def get_fm_dev(self):
        return self.fm_dev

    def set_fm_dev(self, fm_dev):
        self.fm_dev = fm_dev
        self.set_pfb_taps(firdes.low_pass(2.0, self.sample_width, ((self.fm_dev*2)+3e3),2500, firdes.WIN_HAMMING, 6.76))
        self.nbfm_block_9ch_2.set_fm_dev(self.fm_dev)
        self.nbfm_block_9ch_1.set_fm_dev(self.fm_dev)
        self.nbfm_block_9ch_0.set_fm_dev(self.fm_dev)

    def get_channel_map(self):
        return self.channel_map

    def set_channel_map(self, channel_map):
        self.channel_map = channel_map
        self.set_channel_names(map( lambda x: "%.3fMHz" % ( (self.ch0_freq+ (x*self.ch_spacing))/1e6) , self.channel_map))

    def get_band_center(self):
        return self.band_center

    def set_band_center(self, band_center):
        self.band_center = band_center
        self.set_tuner_offset(self.band_center - self.tuner_freq)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.band_center, self.num_chans * self.ch_spacing)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

    def get_tuner_offset(self):
        return self.tuner_offset

    def set_tuner_offset(self, tuner_offset):
        self.tuner_offset = tuner_offset
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.tuner_offset  + self.ppm_corr)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self.nbfm_block_9ch_2.set_squelch(self.squelch)
        self.nbfm_block_9ch_1.set_squelch(self.squelch)
        self.nbfm_block_9ch_0.set_squelch(self.squelch)

    def get_sq_ramp(self):
        return self.sq_ramp

    def set_sq_ramp(self, sq_ramp):
        self.sq_ramp = sq_ramp
        self.nbfm_block_9ch_2.set_sq_ramp(self.sq_ramp)
        self.nbfm_block_9ch_1.set_sq_ramp(self.sq_ramp)
        self.nbfm_block_9ch_0.set_sq_ramp(self.sq_ramp)

    def get_sq_alpha(self):
        return self.sq_alpha

    def set_sq_alpha(self, sq_alpha):
        self.sq_alpha = sq_alpha
        self.nbfm_block_9ch_2.set_sq_alpha(self.sq_alpha)
        self.nbfm_block_9ch_1.set_sq_alpha(self.sq_alpha)
        self.nbfm_block_9ch_0.set_sq_alpha(self.sq_alpha)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.rtlsdr_source_0.set_gain(self.rf_gain, 0)

    def get_ppm_corr(self):
        return self.ppm_corr

    def set_ppm_corr(self, ppm_corr):
        self.ppm_corr = ppm_corr
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.tuner_offset  + self.ppm_corr)

    def get_pfb_taps(self):
        return self.pfb_taps

    def set_pfb_taps(self, pfb_taps):
        self.pfb_taps = pfb_taps
        self.pfb_channelizer_ccf.set_taps((self.pfb_taps))

    def get_lpf_taps(self):
        return self.lpf_taps

    def set_lpf_taps(self, lpf_taps):
        self.lpf_taps = lpf_taps
        self.freq_xlating_fft_filter_ccc_0.set_taps((self.lpf_taps))

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_channelizer_map(self):
        return self.channelizer_map

    def set_channelizer_map(self, channelizer_map):
        self.channelizer_map = channelizer_map
        self.pfb_channelizer_ccf.set_channel_map((self.channelizer_map))

    def get_channel_names(self):
        return self.channel_names

    def set_channel_names(self, channel_names):
        self.channel_names = channel_names

    def get_ch9_mute(self):
        return self.ch9_mute

    def set_ch9_mute(self, ch9_mute):
        self.ch9_mute = ch9_mute
        self._ch9_mute_callback(self.ch9_mute)
        self.nbfm_block_9ch_1.set_mute0(self.ch9_mute)

    def get_ch8_mute(self):
        return self.ch8_mute

    def set_ch8_mute(self, ch8_mute):
        self.ch8_mute = ch8_mute
        self._ch8_mute_callback(self.ch8_mute)
        self.nbfm_block_9ch_0.set_mute8(self.ch8_mute)

    def get_ch7_mute(self):
        return self.ch7_mute

    def set_ch7_mute(self, ch7_mute):
        self.ch7_mute = ch7_mute
        self._ch7_mute_callback(self.ch7_mute)
        self.nbfm_block_9ch_0.set_mute7(self.ch7_mute)

    def get_ch6_mute(self):
        return self.ch6_mute

    def set_ch6_mute(self, ch6_mute):
        self.ch6_mute = ch6_mute
        self._ch6_mute_callback(self.ch6_mute)
        self.nbfm_block_9ch_0.set_mute6(self.ch6_mute)

    def get_ch5_mute(self):
        return self.ch5_mute

    def set_ch5_mute(self, ch5_mute):
        self.ch5_mute = ch5_mute
        self._ch5_mute_callback(self.ch5_mute)
        self.nbfm_block_9ch_0.set_mute5(self.ch5_mute)

    def get_ch4_mute(self):
        return self.ch4_mute

    def set_ch4_mute(self, ch4_mute):
        self.ch4_mute = ch4_mute
        self._ch4_mute_callback(self.ch4_mute)
        self.nbfm_block_9ch_0.set_mute4(self.ch4_mute)

    def get_ch3_mute(self):
        return self.ch3_mute

    def set_ch3_mute(self, ch3_mute):
        self.ch3_mute = ch3_mute
        self._ch3_mute_callback(self.ch3_mute)
        self.nbfm_block_9ch_0.set_mute3(self.ch3_mute)

    def get_ch2_mute(self):
        return self.ch2_mute

    def set_ch2_mute(self, ch2_mute):
        self.ch2_mute = ch2_mute
        self._ch2_mute_callback(self.ch2_mute)
        self.nbfm_block_9ch_0.set_mute2(self.ch2_mute)

    def get_ch26_mute(self):
        return self.ch26_mute

    def set_ch26_mute(self, ch26_mute):
        self.ch26_mute = ch26_mute
        self._ch26_mute_callback(self.ch26_mute)
        self.nbfm_block_9ch_2.set_mute8(self.ch26_mute)

    def get_ch25_mute(self):
        return self.ch25_mute

    def set_ch25_mute(self, ch25_mute):
        self.ch25_mute = ch25_mute
        self._ch25_mute_callback(self.ch25_mute)
        self.nbfm_block_9ch_2.set_mute7(self.ch25_mute)

    def get_ch24_mute(self):
        return self.ch24_mute

    def set_ch24_mute(self, ch24_mute):
        self.ch24_mute = ch24_mute
        self._ch24_mute_callback(self.ch24_mute)
        self.nbfm_block_9ch_2.set_mute6(self.ch24_mute)

    def get_ch23_mute(self):
        return self.ch23_mute

    def set_ch23_mute(self, ch23_mute):
        self.ch23_mute = ch23_mute
        self._ch23_mute_callback(self.ch23_mute)
        self.nbfm_block_9ch_2.set_mute5(self.ch23_mute)

    def get_ch22_mute(self):
        return self.ch22_mute

    def set_ch22_mute(self, ch22_mute):
        self.ch22_mute = ch22_mute
        self._ch22_mute_callback(self.ch22_mute)
        self.nbfm_block_9ch_2.set_mute4(self.ch22_mute)

    def get_ch21_mute(self):
        return self.ch21_mute

    def set_ch21_mute(self, ch21_mute):
        self.ch21_mute = ch21_mute
        self._ch21_mute_callback(self.ch21_mute)
        self.nbfm_block_9ch_2.set_mute3(self.ch21_mute)

    def get_ch20_mute(self):
        return self.ch20_mute

    def set_ch20_mute(self, ch20_mute):
        self.ch20_mute = ch20_mute
        self._ch20_mute_callback(self.ch20_mute)
        self.nbfm_block_9ch_2.set_mute2(self.ch20_mute)

    def get_ch1_mute(self):
        return self.ch1_mute

    def set_ch1_mute(self, ch1_mute):
        self.ch1_mute = ch1_mute
        self._ch1_mute_callback(self.ch1_mute)
        self.nbfm_block_9ch_0.set_mute1(self.ch1_mute)

    def get_ch19_mute(self):
        return self.ch19_mute

    def set_ch19_mute(self, ch19_mute):
        self.ch19_mute = ch19_mute
        self._ch19_mute_callback(self.ch19_mute)
        self.nbfm_block_9ch_2.set_mute1(self.ch19_mute)

    def get_ch18_mute(self):
        return self.ch18_mute

    def set_ch18_mute(self, ch18_mute):
        self.ch18_mute = ch18_mute
        self._ch18_mute_callback(self.ch18_mute)
        self.nbfm_block_9ch_2.set_mute0(self.ch18_mute)

    def get_ch17_mute(self):
        return self.ch17_mute

    def set_ch17_mute(self, ch17_mute):
        self.ch17_mute = ch17_mute
        self._ch17_mute_callback(self.ch17_mute)
        self.nbfm_block_9ch_1.set_mute8(self.ch17_mute)

    def get_ch16_mute(self):
        return self.ch16_mute

    def set_ch16_mute(self, ch16_mute):
        self.ch16_mute = ch16_mute
        self._ch16_mute_callback(self.ch16_mute)
        self.nbfm_block_9ch_1.set_mute7(self.ch16_mute)

    def get_ch15_mute(self):
        return self.ch15_mute

    def set_ch15_mute(self, ch15_mute):
        self.ch15_mute = ch15_mute
        self._ch15_mute_callback(self.ch15_mute)
        self.nbfm_block_9ch_1.set_mute6(self.ch15_mute)

    def get_ch14_mute(self):
        return self.ch14_mute

    def set_ch14_mute(self, ch14_mute):
        self.ch14_mute = ch14_mute
        self._ch14_mute_callback(self.ch14_mute)
        self.nbfm_block_9ch_1.set_mute5(self.ch14_mute)

    def get_ch13_mute(self):
        return self.ch13_mute

    def set_ch13_mute(self, ch13_mute):
        self.ch13_mute = ch13_mute
        self._ch13_mute_callback(self.ch13_mute)
        self.nbfm_block_9ch_1.set_mute4(self.ch13_mute)

    def get_ch12_mute(self):
        return self.ch12_mute

    def set_ch12_mute(self, ch12_mute):
        self.ch12_mute = ch12_mute
        self._ch12_mute_callback(self.ch12_mute)
        self.nbfm_block_9ch_1.set_mute3(self.ch12_mute)

    def get_ch11_mute(self):
        return self.ch11_mute

    def set_ch11_mute(self, ch11_mute):
        self.ch11_mute = ch11_mute
        self._ch11_mute_callback(self.ch11_mute)
        self.nbfm_block_9ch_1.set_mute2(self.ch11_mute)

    def get_ch10_mute(self):
        return self.ch10_mute

    def set_ch10_mute(self, ch10_mute):
        self.ch10_mute = ch10_mute
        self._ch10_mute_callback(self.ch10_mute)
        self.nbfm_block_9ch_1.set_mute1(self.ch10_mute)

    def get_ch0_mute(self):
        return self.ch0_mute

    def set_ch0_mute(self, ch0_mute):
        self.ch0_mute = ch0_mute
        self._ch0_mute_callback(self.ch0_mute)
        self.nbfm_block_9ch_0.set_mute0(self.ch0_mute)

    def get_audio_hw_rate(self):
        return self.audio_hw_rate

    def set_audio_hw_rate(self, audio_hw_rate):
        self.audio_hw_rate = audio_hw_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.audio_hw_rate)


def argument_parser():
    description = 'Derived from work by Chris Kuethe <chris.kuethe+github@gmail.com>'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "-f", "--ch0-init", dest="ch0_init", type="eng_float", default=eng_notation.num_to_str(146.61e6),
        help="Set ch0_init [default=%default]")
    parser.add_option(
        "-s", "--ch-spacing-init", dest="ch_spacing_init", type="intx", default=30,
        help="Set ch_spacing_init [default=%default]")
    return parser


def main(top_block_cls=nbfm_27ch, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(ch0_init=options.ch0_init, ch_spacing_init=options.ch_spacing_init)
    tb.start(512)
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
