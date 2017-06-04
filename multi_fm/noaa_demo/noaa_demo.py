#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: 2M Multi-RX -- 7 simultaneous channels
# Author: Chris Kuethe <chris.kuethe+github@gmail.com>
# Generated: Thu May 25 12:31:22 2017
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

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
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
from optparse import OptionParser
import osmosdr
import sip
import sys
import time


class noaa_demo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "2M Multi-RX -- 7 simultaneous channels")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("2M Multi-RX -- 7 simultaneous channels")
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

        self.settings = Qt.QSettings("GNU Radio", "noaa_demo")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.noaa_num_chans = noaa_num_chans = 7
        self.noaa_chan_width = noaa_chan_width = int(15e3)
        self.noaa_band_start = noaa_band_start = 146.475e6
        self.oversampled_width = oversampled_width = noaa_chan_width * (noaa_num_chans + 1)
        self.noaa_fm_dev = noaa_fm_dev = int(5e3)
        self.noaa_band_center = noaa_band_center = noaa_band_start + (noaa_num_chans / 2 * noaa_chan_width)
        self.hardware_rate = hardware_rate = int(1e6)
        self.tuner_freq = tuner_freq = 146.4e6
        self.target_freq = target_freq = noaa_band_center
        self.ppm = ppm = 0
        self.pfb_taps = pfb_taps = firdes.low_pass(2.0, oversampled_width, noaa_fm_dev*2 ,1000, firdes.WIN_HAMMING, 6.76)
        self.lpf_taps = lpf_taps = firdes.low_pass(1.0, hardware_rate, oversampled_width / 2,noaa_chan_width, firdes.WIN_HAMMING, 6.76)
        self.channel_map = channel_map = range(0, noaa_num_chans)
        self.volume = volume = 0.4
        self.tuner_offset = tuner_offset = target_freq - tuner_freq
        self.squelch = squelch = -55
        self.sq_ramp = sq_ramp = 10
        self.sq_alpha = sq_alpha = 0.005
        self.ppm_corr = ppm_corr = tuner_freq * (ppm/1e6)
        self.pfb_sizeof_taps = pfb_sizeof_taps = len(pfb_taps)
        self.noaa_band_width = noaa_band_width = noaa_chan_width * noaa_num_chans
        self.noaa_band_end = noaa_band_end = noaa_band_start + (noaa_num_chans * noaa_chan_width)
        self.lpf_sizeof_taps = lpf_sizeof_taps = len(lpf_taps)
        self.fftwidth = fftwidth = 512
        self.fft_interval = fft_interval = 1.0/20
        self.decimation = decimation = hardware_rate / oversampled_width
        self.channelizer_map = channelizer_map = 5,6,7,0,1,2,3
        self.channel_names = channel_names = map(lambda x: "%.3fMHz" % (146.475+ (x*0.015)), channel_map)
        self.ch6_mute = ch6_mute = 1
        self.ch5_mute = ch5_mute = 1
        self.ch4_mute = ch4_mute = 1
        self.ch3_mute = ch3_mute = 1
        self.ch2_mute = ch2_mute = 1
        self.ch1_mute = ch1_mute = 1
        self.ch0_mute = ch0_mute = 1
        self.audio_rate = audio_rate = 15000

        ##################################################
        # Blocks
        ##################################################
        self._volume_range = Range(0, 1, 0.01, 0.4, 50)
        self._volume_win = RangeWidget(self._volume_range, self.set_volume, "volume", "slider", float)
        self.top_grid_layout.addWidget(self._volume_win, 0,0,1,3)
        self._squelch_range = Range(-70, -30, 2, -55, 50)
        self._squelch_win = RangeWidget(self._squelch_range, self.set_squelch, "squelch", "slider", float)
        self.top_grid_layout.addWidget(self._squelch_win, 0,3,1,3)
        self._ch6_mute_options = (0, 1, )
        self._ch6_mute_labels = ("Mute", "Unmute", )
        self._ch6_mute_group_box = Qt.QGroupBox("Ch6")
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
        self._ch5_mute_labels = ("Mute", "Unmute", )
        self._ch5_mute_group_box = Qt.QGroupBox("Ch5")
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
        self._ch4_mute_labels = ("Mute", "Unmute", )
        self._ch4_mute_group_box = Qt.QGroupBox("Ch4")
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
        self._ch2_mute_options = (0, 1, )
        self._ch2_mute_labels = ("Mute", "Unmute", )
        self._ch2_mute_group_box = Qt.QGroupBox("Ch2")
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
        self._ch1_mute_options = (0, 1, )
        self._ch1_mute_labels = ("Mute", "Unmute", )
        self._ch1_mute_group_box = Qt.QGroupBox("Ch1")
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
        self._ch0_mute_options = (0, 1, )
        self._ch0_mute_labels = ("Mute", "Unmute", )
        self._ch0_mute_group_box = Qt.QGroupBox("Ch0")
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
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_clock_source("internal", 0)
        self.rtlsdr_source_0.set_sample_rate(hardware_rate)
        self.rtlsdr_source_0.set_center_freq(tuner_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(30, 0)
        self.rtlsdr_source_0.set_bb_gain(40, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=15,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0_0_0 = qtgui.waterfall_sink_c(
        	fftwidth, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	target_freq, #fc
        	oversampled_width, #bw
        	"Band Monitor", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(fft_interval)
        self.qtgui_waterfall_sink_x_0_0_0.enable_grid(True)
        
        if not True:
          self.qtgui_waterfall_sink_x_0_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
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
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_0_win, 2,0,1,9)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	fftwidth, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	noaa_chan_width, #bw
        	"Channelizer Output", #name
        	noaa_num_chans #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(fft_interval)
        self.qtgui_freq_sink_x_0.set_y_axis(-100, 0)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = [channel_names[0], channel_names[1], channel_names[2], channel_names[3], channel_names[4],
                  channel_names[5], channel_names[6], "channel_names[7]", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "dark red",
                  "dark green", "dark blue", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(noaa_num_chans):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 3,0,1,9)
        self._ppm_range = Range(-60, 60, 1, 0, 50)
        self._ppm_win = RangeWidget(self._ppm_range, self.set_ppm, "ppm", "slider", float)
        self.top_grid_layout.addWidget(self._ppm_win, 0,6,1,3)
        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
        	  noaa_num_chans+1,
        	  (pfb_taps),
        	  1,
        	  1)
        self.pfb_channelizer_ccf_0.set_channel_map((channelizer_map))
        self.pfb_channelizer_ccf_0.declare_sample_delay(0)
        	
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(int(decimation), (lpf_taps), tuner_offset  + ppm_corr, hardware_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self._ch3_mute_options = (0, 1, )
        self._ch3_mute_labels = ("Mute", "Unmute", )
        self._ch3_mute_group_box = Qt.QGroupBox("Ch3")
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
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_1_2_0_1 = blocks.multiply_const_vcc((ch6_mute, ))
        self.blocks_multiply_const_vxx_1_2_0_0 = blocks.multiply_const_vcc((ch5_mute, ))
        self.blocks_multiply_const_vxx_1_2_0 = blocks.multiply_const_vcc((ch4_mute, ))
        self.blocks_multiply_const_vxx_1_1_0 = blocks.multiply_const_vcc((ch2_mute, ))
        self.blocks_multiply_const_vxx_1_1 = blocks.multiply_const_vcc((ch2_mute, ))
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vcc((ch1_mute, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((ch0_mute, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
        self.blocks_add_xx_0_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_pwr_squelch_xx_0_2_0_1 = analog.pwr_squelch_cc(squelch, sq_alpha, sq_ramp, False)
        self.analog_pwr_squelch_xx_0_2_0_0 = analog.pwr_squelch_cc(squelch, sq_alpha, sq_ramp, False)
        self.analog_pwr_squelch_xx_0_2_0 = analog.pwr_squelch_cc(squelch, sq_alpha, sq_ramp, False)
        self.analog_pwr_squelch_xx_0_2 = analog.pwr_squelch_cc(squelch, sq_alpha, sq_ramp, False)
        self.analog_pwr_squelch_xx_0_1 = analog.pwr_squelch_cc(squelch, sq_alpha, sq_ramp, False)
        self.analog_pwr_squelch_xx_0_0 = analog.pwr_squelch_cc(squelch, sq_alpha, sq_ramp, False)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(squelch, sq_alpha, sq_ramp, False)
        self.analog_nbfm_rx_0_2_0_1 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )
        self.analog_nbfm_rx_0_2_0_0 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )
        self.analog_nbfm_rx_0_2_0 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )
        self.analog_nbfm_rx_0_2 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )
        self.analog_nbfm_rx_0_1 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )
        self.analog_nbfm_rx_0_0 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=audio_rate,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_add_xx_0_0, 0))    
        self.connect((self.analog_nbfm_rx_0_0, 0), (self.blocks_add_xx_0_0, 1))    
        self.connect((self.analog_nbfm_rx_0_1, 0), (self.blocks_add_xx_0_0, 2))    
        self.connect((self.analog_nbfm_rx_0_2, 0), (self.blocks_add_xx_0_0, 3))    
        self.connect((self.analog_nbfm_rx_0_2_0, 0), (self.blocks_add_xx_0_0, 4))    
        self.connect((self.analog_nbfm_rx_0_2_0_0, 0), (self.blocks_add_xx_0_0, 5))    
        self.connect((self.analog_nbfm_rx_0_2_0_1, 0), (self.blocks_add_xx_0_0, 6))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_pwr_squelch_xx_0_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0_1, 0), (self.blocks_multiply_const_vxx_1_1, 0))    
        self.connect((self.analog_pwr_squelch_xx_0_2, 0), (self.blocks_multiply_const_vxx_1_1_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0_2_0, 0), (self.blocks_multiply_const_vxx_1_2_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0_2_0_0, 0), (self.blocks_multiply_const_vxx_1_2_0_0, 0))    
        self.connect((self.analog_pwr_squelch_xx_0_2_0_1, 0), (self.blocks_multiply_const_vxx_1_2_0_1, 0))    
        self.connect((self.blocks_add_xx_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.analog_nbfm_rx_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_1, 0), (self.analog_nbfm_rx_0_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_1_0, 0), (self.analog_nbfm_rx_0_2, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_2_0, 0), (self.analog_nbfm_rx_0_2_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_2_0_0, 0), (self.analog_nbfm_rx_0_2_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_2_0_1, 0), (self.analog_nbfm_rx_0_2_0_1, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.pfb_channelizer_ccf_0, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.qtgui_waterfall_sink_x_0_0_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.analog_pwr_squelch_xx_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.analog_pwr_squelch_xx_0_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.analog_pwr_squelch_xx_0_1, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.analog_pwr_squelch_xx_0_2, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.analog_pwr_squelch_xx_0_2_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.analog_pwr_squelch_xx_0_2_0_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.analog_pwr_squelch_xx_0_2_0_1, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.blocks_null_sink_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.qtgui_freq_sink_x_0, 1))    
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.qtgui_freq_sink_x_0, 2))    
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.qtgui_freq_sink_x_0, 3))    
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.qtgui_freq_sink_x_0, 4))    
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.qtgui_freq_sink_x_0, 5))    
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.qtgui_freq_sink_x_0, 6))    
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "noaa_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_noaa_num_chans(self):
        return self.noaa_num_chans

    def set_noaa_num_chans(self, noaa_num_chans):
        self.noaa_num_chans = noaa_num_chans
        self.set_channel_map(range(0, self.noaa_num_chans))
        self.set_noaa_band_center(self.noaa_band_start + (self.noaa_num_chans / 2 * self.noaa_chan_width))
        self.set_noaa_band_end(self.noaa_band_start + (self.noaa_num_chans * self.noaa_chan_width))
        self.set_noaa_band_width(self.noaa_chan_width * self.noaa_num_chans)
        self.set_oversampled_width(self.noaa_chan_width * (self.noaa_num_chans + 1))

    def get_noaa_chan_width(self):
        return self.noaa_chan_width

    def set_noaa_chan_width(self, noaa_chan_width):
        self.noaa_chan_width = noaa_chan_width
        self.set_lpf_taps(firdes.low_pass(1.0, self.hardware_rate, self.oversampled_width / 2,self.noaa_chan_width, firdes.WIN_HAMMING, 6.76)
        )
        self.set_noaa_band_center(self.noaa_band_start + (self.noaa_num_chans / 2 * self.noaa_chan_width))
        self.set_noaa_band_end(self.noaa_band_start + (self.noaa_num_chans * self.noaa_chan_width))
        self.set_noaa_band_width(self.noaa_chan_width * self.noaa_num_chans)
        self.set_oversampled_width(self.noaa_chan_width * (self.noaa_num_chans + 1))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.noaa_chan_width)

    def get_noaa_band_start(self):
        return self.noaa_band_start

    def set_noaa_band_start(self, noaa_band_start):
        self.noaa_band_start = noaa_band_start
        self.set_noaa_band_center(self.noaa_band_start + (self.noaa_num_chans / 2 * self.noaa_chan_width))
        self.set_noaa_band_end(self.noaa_band_start + (self.noaa_num_chans * self.noaa_chan_width))

    def get_oversampled_width(self):
        return self.oversampled_width

    def set_oversampled_width(self, oversampled_width):
        self.oversampled_width = oversampled_width
        self.set_decimation(self.hardware_rate / self.oversampled_width)
        self.set_lpf_taps(firdes.low_pass(1.0, self.hardware_rate, self.oversampled_width / 2,self.noaa_chan_width, firdes.WIN_HAMMING, 6.76)
        )
        self.set_pfb_taps(firdes.low_pass(2.0, self.oversampled_width, self.noaa_fm_dev*2 ,1000, firdes.WIN_HAMMING, 6.76))
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.target_freq, self.oversampled_width)

    def get_noaa_fm_dev(self):
        return self.noaa_fm_dev

    def set_noaa_fm_dev(self, noaa_fm_dev):
        self.noaa_fm_dev = noaa_fm_dev
        self.set_pfb_taps(firdes.low_pass(2.0, self.oversampled_width, self.noaa_fm_dev*2 ,1000, firdes.WIN_HAMMING, 6.76))
        self.analog_nbfm_rx_0.set_max_deviation(self.noaa_fm_dev)
        self.analog_nbfm_rx_0_0.set_max_deviation(self.noaa_fm_dev)
        self.analog_nbfm_rx_0_1.set_max_deviation(self.noaa_fm_dev)
        self.analog_nbfm_rx_0_2.set_max_deviation(self.noaa_fm_dev)
        self.analog_nbfm_rx_0_2_0.set_max_deviation(self.noaa_fm_dev)
        self.analog_nbfm_rx_0_2_0_0.set_max_deviation(self.noaa_fm_dev)
        self.analog_nbfm_rx_0_2_0_1.set_max_deviation(self.noaa_fm_dev)

    def get_noaa_band_center(self):
        return self.noaa_band_center

    def set_noaa_band_center(self, noaa_band_center):
        self.noaa_band_center = noaa_band_center
        self.set_target_freq(self.noaa_band_center)

    def get_hardware_rate(self):
        return self.hardware_rate

    def set_hardware_rate(self, hardware_rate):
        self.hardware_rate = hardware_rate
        self.set_decimation(self.hardware_rate / self.oversampled_width)
        self.set_lpf_taps(firdes.low_pass(1.0, self.hardware_rate, self.oversampled_width / 2,self.noaa_chan_width, firdes.WIN_HAMMING, 6.76)
        )
        self.rtlsdr_source_0.set_sample_rate(self.hardware_rate)

    def get_tuner_freq(self):
        return self.tuner_freq

    def set_tuner_freq(self, tuner_freq):
        self.tuner_freq = tuner_freq
        self.set_ppm_corr(self.tuner_freq * (self.ppm/1e6))
        self.set_tuner_offset(self.target_freq - self.tuner_freq)
        self.rtlsdr_source_0.set_center_freq(self.tuner_freq, 0)

    def get_target_freq(self):
        return self.target_freq

    def set_target_freq(self, target_freq):
        self.target_freq = target_freq
        self.set_tuner_offset(self.target_freq - self.tuner_freq)
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.target_freq, self.oversampled_width)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm
        self.set_ppm_corr(self.tuner_freq * (self.ppm/1e6))

    def get_pfb_taps(self):
        return self.pfb_taps

    def set_pfb_taps(self, pfb_taps):
        self.pfb_taps = pfb_taps
        self.set_pfb_sizeof_taps(len(self.pfb_taps))
        self.pfb_channelizer_ccf_0.set_taps((self.pfb_taps))

    def get_lpf_taps(self):
        return self.lpf_taps

    def set_lpf_taps(self, lpf_taps):
        self.lpf_taps = lpf_taps
        self.set_lpf_sizeof_taps(len(self.lpf_taps))
        self.freq_xlating_fft_filter_ccc_0.set_taps((self.lpf_taps))

    def get_channel_map(self):
        return self.channel_map

    def set_channel_map(self, channel_map):
        self.channel_map = channel_map
        self.set_channel_names(map(lambda x: "%.3fMHz" % (146.475+ (x*0.015)), self.channel_map))

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
        self.analog_pwr_squelch_xx_0.set_threshold(self.squelch)
        self.analog_pwr_squelch_xx_0_0.set_threshold(self.squelch)
        self.analog_pwr_squelch_xx_0_1.set_threshold(self.squelch)
        self.analog_pwr_squelch_xx_0_2.set_threshold(self.squelch)
        self.analog_pwr_squelch_xx_0_2_0.set_threshold(self.squelch)
        self.analog_pwr_squelch_xx_0_2_0_0.set_threshold(self.squelch)
        self.analog_pwr_squelch_xx_0_2_0_1.set_threshold(self.squelch)

    def get_sq_ramp(self):
        return self.sq_ramp

    def set_sq_ramp(self, sq_ramp):
        self.sq_ramp = sq_ramp

    def get_sq_alpha(self):
        return self.sq_alpha

    def set_sq_alpha(self, sq_alpha):
        self.sq_alpha = sq_alpha
        self.analog_pwr_squelch_xx_0.set_alpha(self.sq_alpha)
        self.analog_pwr_squelch_xx_0_0.set_alpha(self.sq_alpha)
        self.analog_pwr_squelch_xx_0_1.set_alpha(self.sq_alpha)
        self.analog_pwr_squelch_xx_0_2.set_alpha(self.sq_alpha)
        self.analog_pwr_squelch_xx_0_2_0.set_alpha(self.sq_alpha)
        self.analog_pwr_squelch_xx_0_2_0_0.set_alpha(self.sq_alpha)
        self.analog_pwr_squelch_xx_0_2_0_1.set_alpha(self.sq_alpha)

    def get_ppm_corr(self):
        return self.ppm_corr

    def set_ppm_corr(self, ppm_corr):
        self.ppm_corr = ppm_corr
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.tuner_offset  + self.ppm_corr)

    def get_pfb_sizeof_taps(self):
        return self.pfb_sizeof_taps

    def set_pfb_sizeof_taps(self, pfb_sizeof_taps):
        self.pfb_sizeof_taps = pfb_sizeof_taps

    def get_noaa_band_width(self):
        return self.noaa_band_width

    def set_noaa_band_width(self, noaa_band_width):
        self.noaa_band_width = noaa_band_width

    def get_noaa_band_end(self):
        return self.noaa_band_end

    def set_noaa_band_end(self, noaa_band_end):
        self.noaa_band_end = noaa_band_end

    def get_lpf_sizeof_taps(self):
        return self.lpf_sizeof_taps

    def set_lpf_sizeof_taps(self, lpf_sizeof_taps):
        self.lpf_sizeof_taps = lpf_sizeof_taps

    def get_fftwidth(self):
        return self.fftwidth

    def set_fftwidth(self, fftwidth):
        self.fftwidth = fftwidth

    def get_fft_interval(self):
        return self.fft_interval

    def set_fft_interval(self, fft_interval):
        self.fft_interval = fft_interval
        self.qtgui_freq_sink_x_0.set_update_time(self.fft_interval)
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(self.fft_interval)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_channelizer_map(self):
        return self.channelizer_map

    def set_channelizer_map(self, channelizer_map):
        self.channelizer_map = channelizer_map
        self.pfb_channelizer_ccf_0.set_channel_map((self.channelizer_map))

    def get_channel_names(self):
        return self.channel_names

    def set_channel_names(self, channel_names):
        self.channel_names = channel_names

    def get_ch6_mute(self):
        return self.ch6_mute

    def set_ch6_mute(self, ch6_mute):
        self.ch6_mute = ch6_mute
        self._ch6_mute_callback(self.ch6_mute)
        self.blocks_multiply_const_vxx_1_2_0_1.set_k((self.ch6_mute, ))

    def get_ch5_mute(self):
        return self.ch5_mute

    def set_ch5_mute(self, ch5_mute):
        self.ch5_mute = ch5_mute
        self._ch5_mute_callback(self.ch5_mute)
        self.blocks_multiply_const_vxx_1_2_0_0.set_k((self.ch5_mute, ))

    def get_ch4_mute(self):
        return self.ch4_mute

    def set_ch4_mute(self, ch4_mute):
        self.ch4_mute = ch4_mute
        self._ch4_mute_callback(self.ch4_mute)
        self.blocks_multiply_const_vxx_1_2_0.set_k((self.ch4_mute, ))

    def get_ch3_mute(self):
        return self.ch3_mute

    def set_ch3_mute(self, ch3_mute):
        self.ch3_mute = ch3_mute
        self._ch3_mute_callback(self.ch3_mute)

    def get_ch2_mute(self):
        return self.ch2_mute

    def set_ch2_mute(self, ch2_mute):
        self.ch2_mute = ch2_mute
        self._ch2_mute_callback(self.ch2_mute)
        self.blocks_multiply_const_vxx_1_1.set_k((self.ch2_mute, ))
        self.blocks_multiply_const_vxx_1_1_0.set_k((self.ch2_mute, ))

    def get_ch1_mute(self):
        return self.ch1_mute

    def set_ch1_mute(self, ch1_mute):
        self.ch1_mute = ch1_mute
        self._ch1_mute_callback(self.ch1_mute)
        self.blocks_multiply_const_vxx_1_0.set_k((self.ch1_mute, ))

    def get_ch0_mute(self):
        return self.ch0_mute

    def set_ch0_mute(self, ch0_mute):
        self.ch0_mute = ch0_mute
        self._ch0_mute_callback(self.ch0_mute)
        self.blocks_multiply_const_vxx_1.set_k((self.ch0_mute, ))

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate


def main(top_block_cls=noaa_demo, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start(512)
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
