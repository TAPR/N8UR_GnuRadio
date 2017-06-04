#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Complex Multiplier RX SDRstick HF1 with PBT & Variable BW
# Author: John Petrich, W7FU
# Description: Complex Multiplier RX SDRstick HF1 with PBT & Variable BW
# Generated: Sat Jun  6 15:22:17 2015
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
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import hpsdr
import wx

class Complex_Multiplier_RX_SDRstick_HF1_PBT_Var_BW(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Complex Multiplier RX SDRstick HF1 with PBT & Variable BW")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.kHz = kHz = 0
        self.MHz = MHz = 10
        self.Hz = Hz = 0
        self.samp_rate = samp_rate = 384000
        self.pbt = pbt = 0
        self.freq = freq = MHz*1000000 + kHz*1000 + Hz
        self.bw = bw = 1500
        self.AF_gain = AF_gain = 2

        ##################################################
        # Blocks
        ##################################################
        _pbt_sizer = wx.BoxSizer(wx.VERTICAL)
        self._pbt_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_pbt_sizer,
        	value=self.pbt,
        	callback=self.set_pbt,
        	label="  Passband Tuning",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._pbt_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_pbt_sizer,
        	value=self.pbt,
        	callback=self.set_pbt,
        	minimum=-.000190,
        	maximum=.000190,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_pbt_sizer)
        self._bw_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.bw,
        	callback=self.set_bw,
        	label="  Bandwidth",
        	choices=[500,1500,3000,10000],
        	labels=['500','1.5K','3K','10K'],
        	style=wx.RA_HORIZONTAL,
        )
        self.Add(self._bw_chooser)
        _AF_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._AF_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_AF_gain_sizer,
        	value=self.AF_gain,
        	callback=self.set_AF_gain,
        	label="  Audio Gain",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._AF_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_AF_gain_sizer,
        	value=self.AF_gain,
        	callback=self.set_AF_gain,
        	minimum=0,
        	maximum=10,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_AF_gain_sizer)
        self.wxgui_fftsink2_1 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=-30,
        	ref_scale=2.0,
        	sample_rate=(samp_rate),
        	fft_size=4096,
        	fft_rate=15,
        	average=True,
        	avg_alpha=.5,
        	title="             LSB          Baseband Frequency kHz        USB",
        	peak_hold=False,
        	size=(850,400),
        )
        self.Add(self.wxgui_fftsink2_1.win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(samp_rate/48000, firdes.low_pass(
        	1, samp_rate, bw/2, 100, firdes.WIN_HAMMING, 6.76))
        _kHz_sizer = wx.BoxSizer(wx.VERTICAL)
        self._kHz_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_kHz_sizer,
        	value=self.kHz,
        	callback=self.set_kHz,
        	label="kHz",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._kHz_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_kHz_sizer,
        	value=self.kHz,
        	callback=self.set_kHz,
        	minimum=-500,
        	maximum=500,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_kHz_sizer)
        self.hpsdr_hermesNB_0 = hpsdr.hermesNB(freq, freq, freq, 0, 0, 1, 1, 0, 384000, "eth0", "0xF0", 0xa0, 0, 0x00, 0x00, 0, 1)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vcc((1, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((AF_gain, ))
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.audio_sink_0_0 = audio.sink(48000, "", True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate/48000, analog.GR_COS_WAVE, ((bw/2)*pbt), .99, 0)
        self.analog_agc3_xx_0 = analog.agc3_cc(1, 1e-5, 0.5, 1.0, 1)
        self.analog_agc3_xx_0.set_max_gain(65536)
        _MHz_sizer = wx.BoxSizer(wx.VERTICAL)
        self._MHz_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_MHz_sizer,
        	value=self.MHz,
        	callback=self.set_MHz,
        	label="MHz",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._MHz_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_MHz_sizer,
        	value=self.MHz,
        	callback=self.set_MHz,
        	minimum=0,
        	maximum=50,
        	num_steps=50,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_MHz_sizer)
        _Hz_sizer = wx.BoxSizer(wx.VERTICAL)
        self._Hz_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_Hz_sizer,
        	value=self.Hz,
        	callback=self.set_Hz,
        	label="Fine",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._Hz_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_Hz_sizer,
        	value=self.Hz,
        	callback=self.set_Hz,
        	minimum=-1000,
        	maximum=1000,
        	num_steps=200,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_Hz_sizer)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc3_xx_0, 0), (self.blocks_complex_to_float_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.audio_sink_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.wxgui_fftsink2_1, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_agc3_xx_0, 0))    
        self.connect((self.blocks_null_source_0, 0), (self.hpsdr_hermesNB_0, 0))    
        self.connect((self.hpsdr_hermesNB_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_multiply_xx_0, 0))    


    def get_kHz(self):
        return self.kHz

    def set_kHz(self, kHz):
        self.kHz = kHz
        self.set_freq(self.MHz*1000000 + self.kHz*1000 + self.Hz)
        self._kHz_slider.set_value(self.kHz)
        self._kHz_text_box.set_value(self.kHz)

    def get_MHz(self):
        return self.MHz

    def set_MHz(self, MHz):
        self.MHz = MHz
        self.set_freq(self.MHz*1000000 + self.kHz*1000 + self.Hz)
        self._MHz_slider.set_value(self.MHz)
        self._MHz_text_box.set_value(self.MHz)

    def get_Hz(self):
        return self.Hz

    def set_Hz(self, Hz):
        self.Hz = Hz
        self.set_freq(self.MHz*1000000 + self.kHz*1000 + self.Hz)
        self._Hz_slider.set_value(self.Hz)
        self._Hz_text_box.set_value(self.Hz)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bw/2, 100, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate/48000)
        self.wxgui_fftsink2_1.set_sample_rate((self.samp_rate))

    def get_pbt(self):
        return self.pbt

    def set_pbt(self, pbt):
        self.pbt = pbt
        self._pbt_slider.set_value(self.pbt)
        self._pbt_text_box.set_value(self.pbt)
        self.analog_sig_source_x_0.set_frequency(((self.bw/2)*self.pbt))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.hpsdr_hermesNB_0.set_Receive0Frequency(self.freq)
        self.hpsdr_hermesNB_0.set_Receive1Frequency(self.freq)
        self.hpsdr_hermesNB_0.set_TransmitFrequency(self.freq)
        self.wxgui_fftsink2_1.set_baseband_freq(self.freq)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bw/2, 100, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_frequency(((self.bw/2)*self.pbt))
        self._bw_chooser.set_value(self.bw)

    def get_AF_gain(self):
        return self.AF_gain

    def set_AF_gain(self, AF_gain):
        self.AF_gain = AF_gain
        self.blocks_multiply_const_vxx_0_0.set_k((self.AF_gain, ))
        self._AF_gain_slider.set_value(self.AF_gain)
        self._AF_gain_text_box.set_value(self.AF_gain)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = Complex_Multiplier_RX_SDRstick_HF1_PBT_Var_BW()
    tb.Start(True)
    tb.Wait()
