#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lesson 3 - FM Rx
# Author: John Malsbury - Ettus Research
# Description: Working with the USRP!
# Generated: Sun Apr 17 12:53:42 2016
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

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class fm_receiver(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Lesson 3 - FM Rx")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.var_freq = var_freq = 0
        self.samp_rate = samp_rate = 0.888889e6
        self.fine_tune = fine_tune = 0
        self.band_segment = band_segment = 88.5e6
        self.audio_gain = audio_gain = .1
        self.RF = RF = 0

        ##################################################
        # Blocks
        ##################################################
        _var_freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._var_freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_var_freq_sizer,
        	value=self.var_freq,
        	callback=self.set_var_freq,
        	label='var_freq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._var_freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_var_freq_sizer,
        	value=self.var_freq,
        	callback=self.set_var_freq,
        	minimum=-5.5e6,
        	maximum=5.5e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_var_freq_sizer)
        _fine_tune_sizer = wx.BoxSizer(wx.VERTICAL)
        self._fine_tune_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_fine_tune_sizer,
        	value=self.fine_tune,
        	callback=self.set_fine_tune,
        	label="fine_tune",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._fine_tune_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_fine_tune_sizer,
        	value=self.fine_tune,
        	callback=self.set_fine_tune,
        	minimum=-2.5e5,
        	maximum=2.5e5,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_fine_tune_sizer)
        self._band_segment_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.band_segment,
        	callback=self.set_band_segment,
        	label="band segment",
        	choices=[88.5e6,94.9e6,98.1e6,162.55e6,162.425e6],
        	labels=[88.5,94.9,98.1,'NOAA SEA','NOAA Seaside'],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._band_segment_chooser)
        _audio_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._audio_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_audio_gain_sizer,
        	value=self.audio_gain,
        	callback=self.set_audio_gain,
        	label="audio gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._audio_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_audio_gain_sizer,
        	value=self.audio_gain,
        	callback=self.set_audio_gain,
        	minimum=0,
        	maximum=10,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_audio_gain_sizer)
        _RF_sizer = wx.BoxSizer(wx.VERTICAL)
        self._RF_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_RF_sizer,
        	value=self.RF,
        	callback=self.set_RF,
        	label="RX Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._RF_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_RF_sizer,
        	value=self.RF,
        	callback=self.set_RF,
        	minimum=0,
        	maximum=30,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_RF_sizer)
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=var_freq+fine_tune+band_segment,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title="IF bandpass",
        	peak_hold=False,
        )
        self.GridAdd(self.wxgui_fftsink2_1.win, 0, 1, 1, 1)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=var_freq+fine_tune+band_segment,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-20,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=20,
        	average=True,
        	avg_alpha=.5,
        	title="RF spectrum",
        	peak_hold=False,
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 0, 0, 1, 1)
        def wxgui_fftsink2_0_callback(x, y):
        	self.set_0(x)
        
        self.wxgui_fftsink2_0.set_callback(wxgui_fftsink2_0_callback)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq((var_freq+fine_tune+band_segment), 0)
        self.uhd_usrp_source_0.set_normalized_gain(RF, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(1e6, 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=int(48),
                decimation=111,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_2 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, samp_rate/2, 3e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, samp_rate/8, 10.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(4*2, firdes.low_pass(
        	10, samp_rate, 50e3, 5e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((audio_gain, ))
        self.audio_sink_0 = audio.sink(48000, "", False)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate/8,
        	audio_decimation=1,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_1, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.low_pass_filter_2, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_2, 0))    

    def get_var_freq(self):
        return self.var_freq

    def set_var_freq(self, var_freq):
        self.var_freq = var_freq
        self._var_freq_slider.set_value(self.var_freq)
        self._var_freq_text_box.set_value(self.var_freq)
        self.uhd_usrp_source_0.set_center_freq((self.var_freq+self.fine_tune+self.band_segment), 0)
        self.wxgui_fftsink2_0.set_baseband_freq(self.var_freq+self.fine_tune+self.band_segment)
        self.wxgui_fftsink2_1.set_baseband_freq(self.var_freq+self.fine_tune+self.band_segment)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(10, self.samp_rate, 50e3, 5e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate/8, 10.5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_2.set_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/2, 3e3, firdes.WIN_HAMMING, 6.76))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate)

    def get_fine_tune(self):
        return self.fine_tune

    def set_fine_tune(self, fine_tune):
        self.fine_tune = fine_tune
        self._fine_tune_slider.set_value(self.fine_tune)
        self._fine_tune_text_box.set_value(self.fine_tune)
        self.uhd_usrp_source_0.set_center_freq((self.var_freq+self.fine_tune+self.band_segment), 0)
        self.wxgui_fftsink2_0.set_baseband_freq(self.var_freq+self.fine_tune+self.band_segment)
        self.wxgui_fftsink2_1.set_baseband_freq(self.var_freq+self.fine_tune+self.band_segment)

    def get_band_segment(self):
        return self.band_segment

    def set_band_segment(self, band_segment):
        self.band_segment = band_segment
        self._band_segment_chooser.set_value(self.band_segment)
        self.uhd_usrp_source_0.set_center_freq((self.var_freq+self.fine_tune+self.band_segment), 0)
        self.wxgui_fftsink2_0.set_baseband_freq(self.var_freq+self.fine_tune+self.band_segment)
        self.wxgui_fftsink2_1.set_baseband_freq(self.var_freq+self.fine_tune+self.band_segment)

    def get_audio_gain(self):
        return self.audio_gain

    def set_audio_gain(self, audio_gain):
        self.audio_gain = audio_gain
        self._audio_gain_slider.set_value(self.audio_gain)
        self._audio_gain_text_box.set_value(self.audio_gain)
        self.blocks_multiply_const_vxx_0.set_k((self.audio_gain, ))

    def get_RF(self):
        return self.RF

    def set_RF(self, RF):
        self.RF = RF
        self._RF_slider.set_value(self.RF)
        self._RF_text_box.set_value(self.RF)
        self.uhd_usrp_source_0.set_normalized_gain(self.RF, 0)
        	


def main(top_block_cls=fm_receiver, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
