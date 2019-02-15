#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

#
# NOTE: for some namespace reason, this test can only be tested using
# nose.
#
# % nosetests test_kernel.py
#
#
import os
import unittest
import ipykernel.tests.utils
ipykernel.tests.utils.TIMEOUT = 180

from ipykernel.tests.utils import execute, wait_for_idle
from sos_notebook.test_utils import sos_kernel, get_result, get_display_data, \
    clear_channels, get_std_output


class TestJuliaKernel(unittest.TestCase):
    #
    # Beacuse these tests would be called from sos/test, we
    # should switch to this directory so that some location
    # dependent tests could run successfully
    #
    def setUp(self):
        self.olddir = os.getcwd()
        if os.path.dirname(__file__):
            os.chdir(os.path.dirname(__file__))

    def tearDown(self):
        os.chdir(self.olddir)

    def testGetPythonDataFrameFromJulia(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
import pandas as pd
import numpy as np
arr = np.random.randn(1000)
arr[::10] = np.nan
df = pd.DataFrame({'column_{0}'.format(i): arr for i in range(10)})
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            _, stderr = get_std_output(iopub)
            self.assertEqual(stderr, '', "GOT ERROR {}".format(stderr))
            execute(kc=kc, code="%get df")
            wait_for_idle(kc)
            execute(kc=kc, code="size(df)")
            res = get_display_data(iopub)
            self.assertEqual(res, '(1000, 10)')
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)

    def testGetPythonMatrixFromJulia(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
import numpy as np
mat_var = np.matrix([[1,2],[3,4]])
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get mat_var")
            wait_for_idle(kc)
            execute(kc=kc, code="size(mat_var)")
            res = get_display_data(iopub)
            self.assertEqual(res, '(2, 2)')
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            #

    def testGetPythonNoneFromJulia(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
null_var = None
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get null_var")
            wait_for_idle(kc)
            execute(kc=kc, code="null_var === NaN")
            res = get_display_data(iopub)
            self.assertEqual(res, 'true')
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            #

    def testGetPythonDataFromJulia_num_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
num_var = 123
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get num_var")
            wait_for_idle(kc)
            execute(kc=kc, code="num_var === 123")
            res = get_display_data(iopub)
            self.assertEqual(res, 'true')
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put num_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict num_var")
            res = get_result(iopub)
            self.assertEqual(res['num_var'], 123)
            #

    def testGetPythonDataFromJulia_num_arr_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
import numpy
num_arr_var = numpy.array([1, 2, 3])
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get num_arr_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put num_arr_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict num_arr_var")
            res = get_result(iopub)
            self.assertEqual(list(res['num_arr_var']), [1, 2, 3])

    def testGetPythonDataFromJulia_logic_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
logic_var = True
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get logic_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put logic_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict logic_var")
            res = get_result(iopub)
            self.assertEqual((res['logic_var']), True)

    def testGetPythonDataFromJulia_logic_arr_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
logic_arr_var = [True, False, True]
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get logic_arr_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put logic_arr_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict logic_arr_var")
            res = get_result(iopub)
            self.assertEqual((res['logic_arr_var']), [True, False, True])

    def testGetPythonDataFromJulia_char_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
char_var = '1"23'
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get char_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put char_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict char_var")
            res = get_result(iopub)
            self.assertEqual((res['char_var']), '1"23')

    def testGetPythonDataFromJulia_char_arr_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
char_arr_var = ['1', '2', '3']
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get char_arr_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put char_arr_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict char_arr_var")
            res = get_result(iopub)
            self.assertEqual((res['char_arr_var']), ['1', '2', '3'])

    def testGetPythonDataFromJulia_list_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
list_var = [1, 2, '3']
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get list_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put list_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict list_var")
            res = get_result(iopub)
            self.assertEqual((res['list_var']), [1, 2, '3'])

    def testGetPythonDataFromJulia_dict_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
dict_var = dict(a=1, b=2, c='3')
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get dict_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put dict_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict dict_var")
            res = get_result(iopub)
            self.assertEqual((res['dict_var']), {'a': 1, 'b': 2, 'c': '3'})

    def testGetPythonDataFromJulia_set_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
set_var = {1, 2, '3'}
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get set_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put set_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict set_var")
            res = get_result(iopub)
            self.assertEqual((res['set_var']), {1, 2, '3'})

    def testGetPythonDataFromJulia_recursive_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
recursive_var = {'a': {'b': 123}, 'c': True}
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get recursive_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put recursive_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict recursive_var")
            res = get_result(iopub)
            self.assertEqual(res['recursive_var'],  {
                             'a': {'b': 123}, 'c': True})

    def testGetPythonDataFromJulia_comp_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
comp_var = 1+2j
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get comp_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put comp_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict comp_var")
            res = get_result(iopub)
            self.assertEqual((res['comp_var']), 1+2j)

    def testGetPythonDataFromJulia_seri_var(self):
        # Python -> Julia
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code='''
%use sos
import pandas
seri_var = pandas.Series([1,2,3,3,3,3])
''')
            clear_channels(iopub)
            execute(kc=kc, code="%use Julia")
            wait_for_idle(kc)
            execute(kc=kc, code="%get seri_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict -r")
            wait_for_idle(kc)
            execute(kc=kc, code="%put seri_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)
            execute(kc=kc, code="seri_var = list(seri_var)")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict seri_var")
            res = get_result(iopub)
            self.assertEqual(list(res['seri_var']), [1, 2, 3, 3, 3, 3])

    def testPutJuliaDataToPython(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            # create a data frame
            execute(kc=kc, code="""
%use Julia
null_var = NaN
num_var = 123
num_arr_var = [1, 2, 3]
logic_var = true
logic_arr_var = [true, true, false]
char_var = "123"
char_arr_var = [1, 2, "3"]
using NamedArrays
named_list_var = NamedArray([1,2,3],(["a","b","c"],))
mat_var = [1 2; 3 4]
recursive_var = Dict("a" => 1, "b" => Dict("c" => 3),"d" => "whatever")
comp_var = 1+2im
single_char_var = 'a'
""")
            wait_for_idle(kc)
            execute(kc=kc, code="%put null_var num_var num_arr_var logic_var logic_arr_var char_var char_arr_var mat_var recursive_var comp_var single_char_var")
            wait_for_idle(kc)
            execute(kc=kc, code="%dict null_var num_var num_arr_var logic_var logic_arr_var char_var char_arr_var mat_var recursive_var comp_var single_char_var")
            res = get_result(iopub)
            self.assertEqual(res['null_var'], None)
            self.assertEqual(res['num_var'], 123)
            self.assertEqual(list(res['num_arr_var']), [1, 2, 3])
            self.assertEqual(res['logic_var'], True)
            self.assertEqual(res['logic_arr_var'], [True, True, False])
            self.assertEqual(res['char_var'], '123')
            self.assertEqual(res['char_arr_var'], [1, 2, '3'])
            #self.assertEqual(len(res['named_list_var']), 3)
            self.assertEqual(res['mat_var'].shape, (2, 2))
            self.assertEqual(res['recursive_var'], {
                             'a': 1, 'b': {'c': 3}, 'd': 'whatever'})
            self.assertEqual(res['comp_var'], 1 + 2j)
            self.assertEqual(res['single_char_var'], 'a')
            #self.assertEqual(res['seri_var'], [1,2,3,3,3,3])
            execute(kc=kc, code="%use sos")
            wait_for_idle(kc)

"""
    def testGetPythonDataFromJulia(self):
        with sos_kernel() as kc:
            iopub = kc.iopub_channel
            execute(kc=kc, code='''
%use sos
import numpy
import pandas
first_var = 234
num_arr_var = numpy.array([1, 2, 3])
logic_var = True
logic_arr_var = [True, False, True]
char_var = '1"23'
char_arr_var = ['1', '2', '3']
list_var = [1, 2, '3']
dict_var = dict(a=1, b=2, c='3')
set_var = {1, 2, '3'}
recursive_var = {'a': {'b': 123}, 'c': True}
comp_var = 1+2j
seri_var = pandas.Series([1,2,3,3,3,3])
''')
            wait_for_idle(kc)
            execute(kc=kc, code='''\
%use Julia
%get first_var num_arr_var logic_var logic_arr_var char_var char_arr_var set_var list_var dict_var recursive_var comp_var seri_var
%dict -r
%put first_var num_arr_var logic_var logic_arr_var char_var char_arr_var set_var list_var dict_var recursive_var comp_var seri_var
%use sos
seri_var = list(seri_var)
''')
            wait_for_idle(kc)
            execute(kc=kc, code='''
%dict first_var num_arr_var logic_var logic_arr_var char_var char_arr_var set_var list_var dict_var recursive_var comp_var seri_var
''')
            res = get_result(iopub)
            self.assertEqual(list(res['num_arr_var']), [1, 2, 3])
            self.assertEqual(res['logic_var'], True)
            self.assertEqual(res['logic_arr_var'], [True, False, True])
            self.assertEqual(res['char_var'], '1"23')
            self.assertEqual(res['char_arr_var'], ['1', '2', '3'])
            self.assertEqual(res['set_var'], {1, 2, '3'})
            self.assertEqual(res['list_var'], [1, 2, '3'])
            self.assertEqual(res['dict_var'], {'a': 1, 'b': 2, 'c': '3'})
            self.assertEqual(res['recursive_var'],  {
                             'a': {'b': 123}, 'c': True})
            self.assertEqual(res['comp_var'], 1 + 2j)
            self.assertEqual(res['seri_var'], [1, 2, 3, 3, 3, 3])
"""


if __name__ == '__main__':
    unittest.main()
