#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: PFB Channelizer Demo
# Author: Chris Kuethe <chris.kuethe+github@gmail.com>
# Generated: Mon May 16 09:40:51 2016
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


class pfb_channelizer_demo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "PFB Channelizer Demo")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("PFB Channelizer Demo")
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

        self.settings = Qt.QSettings("GNU Radio", "pfb_channelizer_demo")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.noaa_num_chans = noaa_num_chans = 7
        self.noaa_chan_width = noaa_chan_width = int(25e3)
        self.noaa_band_start = noaa_band_start = 162.4e6
        self.oversampled_width = oversampled_width = noaa_chan_width * (noaa_num_chans + 1)
        self.noaa_fm_dev = noaa_fm_dev = int(5e3)
        self.noaa_band_width = noaa_band_width = noaa_chan_width * noaa_num_chans
        self.noaa_band_center = noaa_band_center = noaa_band_start + (noaa_num_chans / 2 * noaa_chan_width)
        self.hardware_rate = hardware_rate = int(1e6)
        self.tuner_freq = tuner_freq = 162.3e6
        self.target_freq = target_freq = noaa_band_center
        self.ppm = ppm = 0
        
        self.pfb_taps = pfb_taps = firdes.low_pass(2.0, oversampled_width, noaa_fm_dev * 2, 2500, firdes.WIN_HAMMING, 6.76)
          
        
        self.lpf_taps = lpf_taps = firdes.low_pass(1.0, hardware_rate, noaa_band_width / 2, noaa_chan_width, firdes.WIN_HAMMING, 6.76)
          
        self.channel_map = channel_map = range(0, noaa_num_chans+1)
        self.tuner_offset = tuner_offset = target_freq - tuner_freq
        self.ppm_corr = ppm_corr = tuner_freq * (ppm/1e6)
        self.pfb_sizeof_taps = pfb_sizeof_taps = len(pfb_taps)
        self.noaa_band_end = noaa_band_end = noaa_band_start + (noaa_num_chans * noaa_chan_width)
        self.lpf_sizeof_taps = lpf_sizeof_taps = len(lpf_taps)
        self.fftwidth = fftwidth = 512
        self.fft_interval = fft_interval = 1.0/20
        self.decimation = decimation = hardware_rate / oversampled_width
        self.channel_names = channel_names = map(lambda x: "%.3fMHz" % (162.4 + (x*0.025)), channel_map)
        self.chan_num = chan_num = channel_map[0]

        ##################################################
        # Blocks
        ##################################################
        self._chan_num_options = channel_map
        self._chan_num_labels = channel_names
        self._chan_num_tool_bar = Qt.QToolBar(self)
        self._chan_num_tool_bar.addWidget(Qt.QLabel("Channel"+": "))
        self._chan_num_combo_box = Qt.QComboBox()
        self._chan_num_tool_bar.addWidget(self._chan_num_combo_box)
        for label in self._chan_num_labels: self._chan_num_combo_box.addItem(label)
        self._chan_num_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chan_num_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._chan_num_options.index(i)))
        self._chan_num_callback(self.chan_num)
        self._chan_num_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_chan_num(self._chan_num_options[i]))
        self.top_grid_layout.addWidget(self._chan_num_tool_bar, 0,0,1,2)
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
        
        self.qtgui_waterfall_sink_x_0_0_0.set_intensity_range(-80, -35)
        
        self._qtgui_waterfall_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_0_win, 1,0,1,2)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
        	fftwidth, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	noaa_chan_width, #bw
        	"Channel Monitor", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(fft_interval)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(True)
        
        if not True:
          self.qtgui_waterfall_sink_x_0_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [5, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-67, -37)
        
        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 1,2,1,2)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	fftwidth, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	noaa_chan_width, #bw
        	"Channelizer Output", #name
        	noaa_num_chans +1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(fft_interval)
        self.qtgui_freq_sink_x_0.set_y_axis(-80, -35)
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
                  channel_names[5], channel_names[6], channel_names[7], "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(noaa_num_chans +1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2,0,1,4)
        self._ppm_range = Range(-20, 20, 0.5, 0, 100)
        self._ppm_win = RangeWidget(self._ppm_range, self.set_ppm, "ppm", "counter_slider", float)
        self.top_grid_layout.addWidget(self._ppm_win, 0,2,1,2)
        self.pfb_channelizer_ccf_0 = pfb.channelizer_ccf(
        	  noaa_num_chans+1,
        	  (pfb_taps),
        	  1,
        	  100)
        self.pfb_channelizer_ccf_0.set_channel_map((channel_map))
        self.pfb_channelizer_ccf_0.declare_sample_delay(0)
        	
        self.osmosdr_source_0_0 = osmosdr.source( args="numchan=" + str(1) + " " + "type=usrp2" )
        self.osmosdr_source_0_0.set_sample_rate(hardware_rate)
        self.osmosdr_source_0_0.set_center_freq(tuner_freq, 0)
        self.osmosdr_source_0_0.set_freq_corr(0, 0)
        self.osmosdr_source_0_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0_0.set_gain_mode(True, 0)
        self.osmosdr_source_0_0.set_gain(10, 0)
        self.osmosdr_source_0_0.set_if_gain(20, 0)
        self.osmosdr_source_0_0.set_bb_gain(20, 0)
        self.osmosdr_source_0_0.set_antenna("TX/RX", 0)
        self.osmosdr_source_0_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(int(decimation), (lpf_taps), tuner_offset  + ppm_corr, hardware_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_0_5_0 = blocks.multiply_const_vcc((1, ))
        self.blocks_multiply_const_vxx_0_5 = blocks.multiply_const_vcc((1 if chan_num is 6 else 0, ))
        self.blocks_multiply_const_vxx_0_4 = blocks.multiply_const_vcc((1 if chan_num is 5 else 0, ))
        self.blocks_multiply_const_vxx_0_3 = blocks.multiply_const_vcc((1 if chan_num is 4 else 0, ))
        self.blocks_multiply_const_vxx_0_2 = blocks.multiply_const_vcc((1 if chan_num is 3 else 0, ))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vcc((1 if chan_num is 2 else 0, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((1 if chan_num is 1 else 0, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1 if chan_num is 0 else 0, ))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.audio_sink_0 = audio.sink(24000, "", True)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=noaa_chan_width,
        	quad_rate=noaa_chan_width,
        	tau=75e-6,
        	max_dev=noaa_fm_dev,
          )
        (self.analog_nbfm_rx_0).set_max_output_buffer(512)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blocks_add_xx_0, 2))    
        self.connect((self.blocks_multiply_const_vxx_0_2, 0), (self.blocks_add_xx_0, 3))    
        self.connect((self.blocks_multiply_const_vxx_0_3, 0), (self.blocks_add_xx_0, 4))    
        self.connect((self.blocks_multiply_const_vxx_0_4, 0), (self.blocks_add_xx_0, 5))    
        self.connect((self.blocks_multiply_const_vxx_0_5, 0), (self.blocks_add_xx_0, 6))    
        self.connect((self.blocks_multiply_const_vxx_0_5_0, 0), (self.blocks_add_xx_0, 7))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.pfb_channelizer_ccf_0, 0))    
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.qtgui_waterfall_sink_x_0_0_0, 0))    
        self.connect((self.osmosdr_source_0_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.blocks_multiply_const_vxx_0_1, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.blocks_multiply_const_vxx_0_2, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.blocks_multiply_const_vxx_0_3, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.blocks_multiply_const_vxx_0_4, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.blocks_multiply_const_vxx_0_5, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.blocks_multiply_const_vxx_0_5_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.pfb_channelizer_ccf_0, 1), (self.qtgui_freq_sink_x_0, 1))    
        self.connect((self.pfb_channelizer_ccf_0, 2), (self.qtgui_freq_sink_x_0, 2))    
        self.connect((self.pfb_channelizer_ccf_0, 3), (self.qtgui_freq_sink_x_0, 3))    
        self.connect((self.pfb_channelizer_ccf_0, 4), (self.qtgui_freq_sink_x_0, 4))    
        self.connect((self.pfb_channelizer_ccf_0, 5), (self.qtgui_freq_sink_x_0, 5))    
        self.connect((self.pfb_channelizer_ccf_0, 6), (self.qtgui_freq_sink_x_0, 6))    
        self.connect((self.pfb_channelizer_ccf_0, 7), (self.qtgui_freq_sink_x_0, 7))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "pfb_channelizer_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_noaa_num_chans(self):
        return self.noaa_num_chans

    def set_noaa_num_chans(self, noaa_num_chans):
        self.noaa_num_chans = noaa_num_chans
        self.set_channel_map(range(0, self.noaa_num_chans+1))
        self.set_noaa_band_center(self.noaa_band_start + (self.noaa_num_chans / 2 * self.noaa_chan_width))
        self.set_noaa_band_end(self.noaa_band_start + (self.noaa_num_chans * self.noaa_chan_width))
        self.set_noaa_band_width(self.noaa_chan_width * self.noaa_num_chans)
        self.set_oversampled_width(self.noaa_chan_width * (self.noaa_num_chans + 1))

    def get_noaa_chan_width(self):
        return self.noaa_chan_width

    def set_noaa_chan_width(self, noaa_chan_width):
        self.noaa_chan_width = noaa_chan_width
        self.set_noaa_band_center(self.noaa_band_start + (self.noaa_num_chans / 2 * self.noaa_chan_width))
        self.set_noaa_band_end(self.noaa_band_start + (self.noaa_num_chans * self.noaa_chan_width))
        self.set_noaa_band_width(self.noaa_chan_width * self.noaa_num_chans)
        self.set_oversampled_width(self.noaa_chan_width * (self.noaa_num_chans + 1))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.noaa_chan_width)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(0, self.noaa_chan_width)

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
        self.qtgui_waterfall_sink_x_0_0_0.set_frequency_range(self.target_freq, self.oversampled_width)

    def get_noaa_fm_dev(self):
        return self.noaa_fm_dev

    def set_noaa_fm_dev(self, noaa_fm_dev):
        self.noaa_fm_dev = noaa_fm_dev
        self.analog_nbfm_rx_0.set_max_deviation(self.noaa_fm_dev)

    def get_noaa_band_width(self):
        return self.noaa_band_width

    def set_noaa_band_width(self, noaa_band_width):
        self.noaa_band_width = noaa_band_width

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
        self.osmosdr_source_0_0.set_sample_rate(self.hardware_rate)

    def get_tuner_freq(self):
        return self.tuner_freq

    def set_tuner_freq(self, tuner_freq):
        self.tuner_freq = tuner_freq
        self.set_ppm_corr(self.tuner_freq * (self.ppm/1e6))
        self.set_tuner_offset(self.target_freq - self.tuner_freq)
        self.osmosdr_source_0_0.set_center_freq(self.tuner_freq, 0)

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
        self.set_chan_num(self.channel_map[0])
        self.set_channel_names(map(lambda x: "%.3fMHz" % (162.4 + (x*0.025)), self.channel_map))
        self.pfb_channelizer_ccf_0.set_channel_map((self.channel_map))

    def get_tuner_offset(self):
        return self.tuner_offset

    def set_tuner_offset(self, tuner_offset):
        self.tuner_offset = tuner_offset
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.tuner_offset  + self.ppm_corr)

    def get_ppm_corr(self):
        return self.ppm_corr

    def set_ppm_corr(self, ppm_corr):
        self.ppm_corr = ppm_corr
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.tuner_offset  + self.ppm_corr)

    def get_pfb_sizeof_taps(self):
        return self.pfb_sizeof_taps

    def set_pfb_sizeof_taps(self, pfb_sizeof_taps):
        self.pfb_sizeof_taps = pfb_sizeof_taps

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
        self.qtgui_waterfall_sink_x_0_0.set_update_time(self.fft_interval)
        self.qtgui_waterfall_sink_x_0_0_0.set_update_time(self.fft_interval)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation

    def get_channel_names(self):
        return self.channel_names

    def set_channel_names(self, channel_names):
        self.channel_names = channel_names

    def get_chan_num(self):
        return self.chan_num

    def set_chan_num(self, chan_num):
        self.chan_num = chan_num
        self._chan_num_callback(self.chan_num)
        self.blocks_multiply_const_vxx_0.set_k((1 if self.chan_num is 0 else 0, ))
        self.blocks_multiply_const_vxx_0_0.set_k((1 if self.chan_num is 1 else 0, ))
        self.blocks_multiply_const_vxx_0_1.set_k((1 if self.chan_num is 2 else 0, ))
        self.blocks_multiply_const_vxx_0_2.set_k((1 if self.chan_num is 3 else 0, ))
        self.blocks_multiply_const_vxx_0_3.set_k((1 if self.chan_num is 4 else 0, ))
        self.blocks_multiply_const_vxx_0_4.set_k((1 if self.chan_num is 5 else 0, ))
        self.blocks_multiply_const_vxx_0_5.set_k((1 if self.chan_num is 6 else 0, ))


def main(top_block_cls=pfb_channelizer_demo, options=None):

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
