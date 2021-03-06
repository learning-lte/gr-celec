#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

fsm_args = {"awgn1o2_8": (2, 8, 4,
        (0, 4, 0, 4, 1, 5, 1, 5, 2, 6, 2, 6, 3, 7, 3, 7),
        (0, 3, 3, 0, 1, 2, 2, 1, 3, 0, 0, 3, 2, 1, 1, 2),
        ), 
      "awgn1o2_16": ( 2,16,4,
        (0, 8, 0, 8, 1, 9, 1, 9, 2, 10, 2, 10, 3, 11, 3, 11, 4, 12, 4, 12, 5, 13, 5, 13, 6, 14, 6, 14, 7, 15, 7, 15),
        (0, 3, 3, 0, 1, 2, 2, 1, 1, 2, 2, 1, 0, 3, 3, 0, 2, 1, 1, 2, 3, 0, 0, 3, 3, 0, 0, 3, 2, 1, 1, 2)),
        } 

from gnuradio import gr, gr_unittest
from gnuradio import blocks, trellis, digital
import numpy
import celec_swig as celec

class qa_max_log_map_f (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):

        # Setup parameters of the System
        fsm = fsm_args["awgn1o2_16"]
        os = numpy.array(fsm[4], dtype=int) 
        data = numpy.array([-5,-5,-5,-5,5,5,-5,5,5,-5])
        expected_data = numpy.array([0,0,0,0,1,1,0,1,1,0])
        print data

        data_src = blocks.vector_source_f(map(float, data))

        # Set up TX
        src_head = blocks.head(gr.sizeof_float*1, 10)
        
        shuffle = numpy.array([0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,], dtype=int)
        # Setup RX
        max_log_map_cel = celec.max_log_map_f(2, 4, 10, 0, -1, shuffle, os)
        conv = blocks.float_to_char()
        rx_sink = blocks.vector_sink_f(1)


        self.tb.connect(data_src, src_head, max_log_map_cel, rx_sink)

        # set up fg
        self.tb.run ()

        print rx_sink.data()
        # check data


if __name__ == '__main__':
    gr_unittest.run(qa_max_log_map_f, "qa_max_log_map_f.xml")
