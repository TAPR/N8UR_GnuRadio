#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: B200 VHF NBFM transceiver
# Author: John Petrich, W7FU 12/15/15
# Description: B200 version VHF NBFM transceiver
# Generated: Sun Apr 17 12:49:17 2016
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
from gnuradio.filter import pfb
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class B200_NBFM_VHF_RX_TX_ver_10_5(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="B200 VHF NBFM transceiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.tx_rx_choice = tx_rx_choice = 1
        self.tx_gain = tx_gain = .615
        self.tune_minus_20 = tune_minus_20 = 0
        self.tune_minus_10 = tune_minus_10 = 0
        self.tune_20 = tune_20 = 0
        self.tune_10 = tune_10 = 0
        self.tone = tone = 100
        self.squelch = squelch = -70.32
        self.samp_rate = samp_rate = 4000000
        self.rx_offset = rx_offset = 0
        self.rit_tune = rit_tune = 0
        self.offset = offset = 600000
        self.chooser_fm = chooser_fm = 147.34e6
        self.audio_gain = audio_gain = .7

        ##################################################
        # Blocks
        ##################################################
        self._tx_rx_choice_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.tx_rx_choice,
        	callback=self.set_tx_rx_choice,
        	label="TX-RX",
        	choices=[0, 1],
        	labels=['TX', 'RX'],
        )
        self.GridAdd(self._tx_rx_choice_chooser, 0, 3, 1, 1)
        _tx_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._tx_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_tx_gain_sizer,
        	value=self.tx_gain,
        	callback=self.set_tx_gain,
        	label="TX Gain: 144= .6, 220= .70, 440= .72",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._tx_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_tx_gain_sizer,
        	value=self.tx_gain,
        	callback=self.set_tx_gain,
        	minimum=.6,
        	maximum=.75,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_tx_gain_sizer)
        self._tune_minus_20_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.tune_minus_20,
        	callback=self.set_tune_minus_20,
        	label="-20 Tune",
        	choices=[0, 20e3, 40e3, 60e3, 80e3, 100e3, 120e3, 140e3, 0],
        	labels=[0, -20, -40, -60, -80, -100, -120, -140, 0],
        )
        self.GridAdd(self._tune_minus_20_chooser, 0, 1, 1, 1)
        self._tune_minus_10_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.tune_minus_10,
        	callback=self.set_tune_minus_10,
        	label="-10 Tune",
        	choices=[0,-10e3, -20e3, -30e3, -40e3,-50e3,0],
        	labels=[0, -10, -20, -30, -40,-50,0],
        )
        self.GridAdd(self._tune_minus_10_chooser, 1, 1, 1, 1)
        self._tune_20_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.tune_20,
        	callback=self.set_tune_20,
        	label="+20 Tune",
        	choices=[0, 20e3, 40e3, 60e3, 80e3, 100e3, 120e3, 140e3,0],
        	labels=[0, '+20', '+40', '+60', '+80', '+100', '+120', '+140','0'],
        )
        self.GridAdd(self._tune_20_chooser, 0, 0, 1, 1)
        self._tune_10_chooser = forms.button(
        	parent=self.GetWin(),
        	value=self.tune_10,
        	callback=self.set_tune_10,
        	label="+10 Tune",
        	choices=[0,10e3, 20e3, 30e3, 40e3,50e3,0],
        	labels=[0,'+10', '+20', '+30', '+40','+50','0'],
        )
        self.GridAdd(self._tune_10_chooser, 1, 0, 1, 1)
        self._tone_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.tone,
        	callback=self.set_tone,
        	label="CTCSS",
        	choices=[100,103.5, 110.9, 118.8, 123.0,127.3,179.5],
        	labels=['100', '103.5', '110.9','118.8', '123.0', '127.3','179.5'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._tone_chooser, 0, 5, 1, 1)
        _squelch_sizer = wx.BoxSizer(wx.VERTICAL)
        self._squelch_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_squelch_sizer,
        	value=self.squelch,
        	callback=self.set_squelch,
        	label="Squelch",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._squelch_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_squelch_sizer,
        	value=self.squelch,
        	callback=self.set_squelch,
        	minimum=-95,
        	maximum=-55,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_squelch_sizer, 0, 6, 1, 1)
        self._rx_offset_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.rx_offset,
        	callback=self.set_rx_offset,
        	label="RX offset",
        	choices=[0, 600000, -600000,5e6],
        	labels=['0', '+', '-','+5M'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._rx_offset_chooser, 1, 6, 1, 1)
        _rit_tune_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rit_tune_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rit_tune_sizer,
        	value=self.rit_tune,
        	callback=self.set_rit_tune,
        	label="RIT",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rit_tune_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rit_tune_sizer,
        	value=self.rit_tune,
        	callback=self.set_rit_tune,
        	minimum=-30e3,
        	maximum=+30e3,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_rit_tune_sizer, 1, 2, 1, 3)
        self._offset_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.offset,
        	callback=self.set_offset,
        	label="TX offset",
        	choices=[600000, -600000, 0,5e6],
        	labels=['+', '-', '0','5MHz'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._offset_chooser, 0, 4, 1, 1)
        self._chooser_fm_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.chooser_fm,
        	callback=self.set_chooser_fm,
        	label="Preset",
        	choices=[145.13e6,145.33e6, 145.88e6, 146.46e6, 146.49e6, 146.52e6,146.58e6, 146.64e6,146.74e6, 146.82e6, 146.86e6, 146.92e6, 146.96e6, 147.0e6,147.06e6, 147.08e6, 147.20e6, 147.22e6, 147.34e6, 223.5e6,441.825e6, 432.25e6],
        	labels=[145.13,145.33, 145.88, 146.46, 146.49, 146.52, 146.58, 146.64, 146.74, 146.82, 146.860, 146.92, 146.96,  147.00, 147.06, 147.08,147.200, 147.220, 147.34, 223.5,441.825, 432.25],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._chooser_fm_chooser)
        _audio_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._audio_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_audio_gain_sizer,
        	value=self.audio_gain,
        	callback=self.set_audio_gain,
        	label="Audio gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._audio_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_audio_gain_sizer,
        	value=self.audio_gain,
        	callback=self.set_audio_gain,
        	minimum=.1,
        	maximum=4,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_audio_gain_sizer, 0, 2, 1, 1)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=(((((chooser_fm+tune_20)-tune_minus_20)+tune_10)+tune_minus_10)+rx_offset),
        	y_per_div=5,
        	y_divs=16,
        	ref_level=-55,
        	ref_scale=2.0,
        	sample_rate=samp_rate/2,
        	fft_size=1024*0+2048*0+4096,
        	fft_rate=12,
        	average=True,
        	avg_alpha=.4,
        	title="RF Bandpass",
        	peak_hold=False,
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 2, 0, 5, 14)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate((samp_rate))
        self.uhd_usrp_source_0.set_center_freq((((((chooser_fm+tune_20)-tune_minus_20)+tune_10)+tune_minus_10)+rx_offset)-10e3, 0)
        self.uhd_usrp_source_0.set_normalized_gain(.520*.8, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(1.99e6, 0)
        self.uhd_usrp_sink_1 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_1.set_samp_rate(320000)
        self.uhd_usrp_sink_1.set_center_freq((((((chooser_fm+offset)+tune_20)-tune_minus_20)+tune_10)+tune_minus_10)+rit_tune, 0)
        self.uhd_usrp_sink_1.set_normalized_gain((.83*0+.72)*0+tx_gain, 0)
        self.uhd_usrp_sink_1.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_1.set_bandwidth(200000, 0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=32000,
                decimation=40000,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=samp_rate/2,
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
        	  2,
        	  (firdes.low_pass(.1, (samp_rate), (samp_rate)/4.05,10e3)),
        	  0,
        	  100,
                  True,
                  True)
        self.pfb_decimator_ccf_0.declare_sample_delay(0)
        	
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, 32000, 4400, 300, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(1, firdes.low_pass(
        	1, 32000, 4500, 600, firdes.WIN_HAMMING, 6.76))
        self.high_pass_filter_0 = filter.fir_filter_fff(1, firdes.high_pass(
        	1, 32000, 300, 100, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(50, (firdes.low_pass(1,samp_rate/2,18e3,600)), 0+rit_tune+10e3, samp_rate/2)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vcc((.8, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((125, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((audio_gain*tx_rx_choice, ))
        self.blocks_add_xx_1 = blocks.add_vff(1)
        self.blks2_selector_0_1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=1+(tx_rx_choice),
        	output_index=0,
        )
        self.audio_source_1 = audio.source(32000, "", True)
        self.audio_sink_0 = audio.sink(32000, "", True)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(squelch, .0001)
        self.analog_sig_source_x_0 = analog.sig_source_f(32000, analog.GR_COS_WAVE, tone, .091, 0)
        self.analog_nbfm_tx_1 = analog.nbfm_tx(
        	audio_rate=32000,
        	quad_rate=320000,
        	tau=(75e-6)*0+90e-6,
        	max_dev=5e3,
                )
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=32000,
        	quad_rate=32000,
        	tau=75e-6,
        	max_dev=5e3,
          )
        self.analog_fm_preemph_0 = analog.fm_preemph(fs=32e3, tau=75e-6)
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=32000, tau=75e-6)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_deemph_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.analog_fm_preemph_0, 0), (self.blocks_add_xx_1, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.analog_fm_deemph_0, 0))    
        self.connect((self.analog_nbfm_tx_1, 0), (self.blocks_multiply_const_vxx_2, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_add_xx_1, 1))    
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.audio_source_1, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.blks2_selector_0_1, 0), (self.uhd_usrp_sink_1, 0))    
        self.connect((self.blocks_add_xx_1, 0), (self.analog_nbfm_tx_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.high_pass_filter_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blks2_selector_0_1, 1))    
        self.connect((self.blocks_null_source_0, 0), (self.blks2_selector_0_1, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_simple_squelch_cc_0, 0))    
        self.connect((self.high_pass_filter_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_fm_preemph_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.pfb_decimator_ccf_0, 0), (self.wxgui_fftsink2_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.pfb_decimator_ccf_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.rational_resampler_xxx_0, 0))    

    def get_tx_rx_choice(self):
        return self.tx_rx_choice

    def set_tx_rx_choice(self, tx_rx_choice):
        self.tx_rx_choice = tx_rx_choice
        self._tx_rx_choice_chooser.set_value(self.tx_rx_choice)
        self.blks2_selector_0_1.set_input_index(int(1+(self.tx_rx_choice)))
        self.blocks_multiply_const_vxx_0.set_k((self.audio_gain*self.tx_rx_choice, ))

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self._tx_gain_slider.set_value(self.tx_gain)
        self._tx_gain_text_box.set_value(self.tx_gain)
        self.uhd_usrp_sink_1.set_normalized_gain((.83*0+.72)*0+self.tx_gain, 0)
        	

    def get_tune_minus_20(self):
        return self.tune_minus_20

    def set_tune_minus_20(self, tune_minus_20):
        self.tune_minus_20 = tune_minus_20
        self._tune_minus_20_chooser.set_value(self.tune_minus_20)
        self.uhd_usrp_sink_1.set_center_freq((((((self.chooser_fm+self.offset)+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rit_tune, 0)
        self.uhd_usrp_source_0.set_center_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset)-10e3, 0)
        self.wxgui_fftsink2_0.set_baseband_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset))

    def get_tune_minus_10(self):
        return self.tune_minus_10

    def set_tune_minus_10(self, tune_minus_10):
        self.tune_minus_10 = tune_minus_10
        self._tune_minus_10_chooser.set_value(self.tune_minus_10)
        self.uhd_usrp_sink_1.set_center_freq((((((self.chooser_fm+self.offset)+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rit_tune, 0)
        self.uhd_usrp_source_0.set_center_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset)-10e3, 0)
        self.wxgui_fftsink2_0.set_baseband_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset))

    def get_tune_20(self):
        return self.tune_20

    def set_tune_20(self, tune_20):
        self.tune_20 = tune_20
        self._tune_20_chooser.set_value(self.tune_20)
        self.uhd_usrp_sink_1.set_center_freq((((((self.chooser_fm+self.offset)+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rit_tune, 0)
        self.uhd_usrp_source_0.set_center_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset)-10e3, 0)
        self.wxgui_fftsink2_0.set_baseband_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset))

    def get_tune_10(self):
        return self.tune_10

    def set_tune_10(self, tune_10):
        self.tune_10 = tune_10
        self._tune_10_chooser.set_value(self.tune_10)
        self.uhd_usrp_sink_1.set_center_freq((((((self.chooser_fm+self.offset)+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rit_tune, 0)
        self.uhd_usrp_source_0.set_center_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset)-10e3, 0)
        self.wxgui_fftsink2_0.set_baseband_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset))

    def get_tone(self):
        return self.tone

    def set_tone(self, tone):
        self.tone = tone
        self._tone_chooser.set_value(self.tone)
        self.analog_sig_source_x_0.set_frequency(self.tone)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self._squelch_slider.set_value(self.squelch)
        self._squelch_text_box.set_value(self.squelch)
        self.analog_simple_squelch_cc_0.set_threshold(self.squelch)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1,self.samp_rate/2,18e3,600)))
        self.pfb_decimator_ccf_0.set_taps((firdes.low_pass(.1, (self.samp_rate), (self.samp_rate)/4.05,10e3)))
        self.uhd_usrp_source_0.set_samp_rate((self.samp_rate))
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate/2)

    def get_rx_offset(self):
        return self.rx_offset

    def set_rx_offset(self, rx_offset):
        self.rx_offset = rx_offset
        self._rx_offset_chooser.set_value(self.rx_offset)
        self.uhd_usrp_source_0.set_center_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset)-10e3, 0)
        self.wxgui_fftsink2_0.set_baseband_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset))

    def get_rit_tune(self):
        return self.rit_tune

    def set_rit_tune(self, rit_tune):
        self.rit_tune = rit_tune
        self._rit_tune_slider.set_value(self.rit_tune)
        self._rit_tune_text_box.set_value(self.rit_tune)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(0+self.rit_tune+10e3)
        self.uhd_usrp_sink_1.set_center_freq((((((self.chooser_fm+self.offset)+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rit_tune, 0)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self._offset_chooser.set_value(self.offset)
        self.uhd_usrp_sink_1.set_center_freq((((((self.chooser_fm+self.offset)+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rit_tune, 0)

    def get_chooser_fm(self):
        return self.chooser_fm

    def set_chooser_fm(self, chooser_fm):
        self.chooser_fm = chooser_fm
        self._chooser_fm_chooser.set_value(self.chooser_fm)
        self.uhd_usrp_sink_1.set_center_freq((((((self.chooser_fm+self.offset)+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rit_tune, 0)
        self.uhd_usrp_source_0.set_center_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset)-10e3, 0)
        self.wxgui_fftsink2_0.set_baseband_freq((((((self.chooser_fm+self.tune_20)-self.tune_minus_20)+self.tune_10)+self.tune_minus_10)+self.rx_offset))

    def get_audio_gain(self):
        return self.audio_gain

    def set_audio_gain(self, audio_gain):
        self.audio_gain = audio_gain
        self._audio_gain_slider.set_value(self.audio_gain)
        self._audio_gain_text_box.set_value(self.audio_gain)
        self.blocks_multiply_const_vxx_0.set_k((self.audio_gain*self.tx_rx_choice, ))


def main(top_block_cls=B200_NBFM_VHF_RX_TX_ver_10_5, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
