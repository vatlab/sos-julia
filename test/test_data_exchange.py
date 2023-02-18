#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import random

from sos_notebook.test_utils import NotebookTest


class TestDataExchange(NotebookTest):

    def _var_name(self):
        if not hasattr(self, '_var_idx'):
            self._var_idx = 0
        self._var_idx += 1
        return f'var{self._var_idx}'

    def get_from_SoS(self, notebook, sos_expr, expect_error=False):
        var_name = self._var_name()
        notebook.call(
            f'import pandas\nimport numpy\n{var_name} = {sos_expr}',
            kernel='SoS')
        return notebook.check_output(
            f'''\
            %get {var_name}
            {var_name}''',
            kernel='Julia',
            expect_error=expect_error)

    def put_to_SoS(self, notebook, julia_expr):
        var_name = self._var_name()
        if 'DataFrame' in julia_expr:
            notebook.call(
                f'''\
                try
                    using DataFrames
                catch
                    Pkg.add("DataFrames")
                    using DataFrames
                end
                ''',
                kernel='Julia')
        notebook.call(
            f'''\
            %put {var_name}
            {var_name} = {julia_expr}
            ''',
            kernel='Julia')
        return notebook.check_output(f'print(repr({var_name}))', kernel='SoS')

    def test_get_none(self, notebook):
        assert 'NaN' == self.get_from_SoS(notebook, 'None')

    def test_put_nan(self, notebook):
        assert 'None' == self.put_to_SoS(notebook, 'NaN')

    def test_get_int(self, notebook):
        assert '123' == self.get_from_SoS(notebook, '123')
        assert '1234567891234' == self.get_from_SoS(notebook, '1234567891234')
        assert '123456789123456789' == self.get_from_SoS(
            notebook, '123456789123456789')

    def test_put_int(self, notebook):
        assert '123' == self.put_to_SoS(notebook, '123')
        assert '1234567891234' == self.put_to_SoS(notebook, '1234567891234')
        assert '123456789123456789' == self.put_to_SoS(notebook,
                                                       '123456789123456789')

    def test_get_double(self, notebook):
        # FIXME: can we improve the precision here? Passing float as string
        # is certainly a bad idea.
        val = str(random.random())
        assert abs(float(val) - float(self.get_from_SoS(notebook, val))) < 1e-10

    def test_put_double(self, notebook):
        val = str(random.random())
        assert abs(float(val) - float(self.put_to_SoS(notebook, val))) < 1e-10

    def test_get_logic(self, notebook):
        assert 'true' == self.get_from_SoS(notebook, 'True')
        assert 'false' == self.get_from_SoS(notebook, 'False')

    def test_put_logic(self, notebook):
        assert 'True' == self.put_to_SoS(notebook, 'true')
        assert 'False' == self.put_to_SoS(notebook, 'false')

    def test_get_num_array(self, notebook):
        output = self.get_from_SoS(notebook, '[99]')
        assert 'Array' in output and 'Int' in output and '99' in output

        output = self.get_from_SoS(notebook, '[11, 22]')
        assert 'Array' in output and 'Int' in output and '22' in output
        #
        output = self.get_from_SoS(notebook, '[1.4, 2]')
        assert 'Array' in output and 'Float' in output and '1.4' in output

    def test_put_num_array(self, notebook):
        assert 'array([ 99, 200])' == self.put_to_SoS(notebook, '[99, 200]')
        #
        assert 'array([1.4, 2. ])' == self.put_to_SoS(notebook, '[1.4, 2]')

    def test_get_num_colarray(self, notebook):
        output = self.get_from_SoS(notebook, 'numpy.array([[11], [22], [33]])')
        assert 'Array' in output and 'Int' in output and '22' in output

        output = self.get_from_SoS(notebook,
                                   'numpy.array([[11.11], [22.22], [33]])')
        assert 'Array' in output and 'Float' in output and '22.22' in output
        output = self.get_from_SoS(
            notebook, 'numpy.array([[11.11, 13.1], [22.22, 35.1], [33, 27]])')
        assert 'Array' in output and 'Float' in output and '22.22' in output

    def test_get_num_matrix(self, notebook):
        notebook.call(
            '''\
            import warnings
            warnings.simplefilter(action='ignore', category=FutureWarning)
            import feather''',
            kernel='SoS')
        output = self.get_from_SoS(
            notebook, 'numpy.matrix([[11, 22], [22, 23], [33, 35]])')
        assert 'Array' in output and 'Int64' in output
        assert '22' in output and '3×2' in output

        output = self.get_from_SoS(
            notebook,
            'numpy.matrix([[11.11, 2, 3], [22.22, 4, 5], [33, 6, 7]])',
            expect_error=False)
        assert 'Array' in output and 'Float' in output and '22.22' in output

    def test_get_dataframe(self, notebook):
        output = self.get_from_SoS(
            notebook, 'pandas.DataFrame([[11, 22], [22, 23], [33, 35]])')
        assert 'rows' in output and 'columns' in output and '22' in output and '35' in output

        output = self.get_from_SoS(
            notebook,
            '''pandas.DataFrame(dict(a=['aa', 'bb', 'cc'], val=[2, 4333, 5]))'''
        )
        assert '3 rows × 2 columns' in output and 'aa' in output and '4333' in output

    def test_put_dataframe(self, notebook):
        output = self.put_to_SoS(
            notebook, 'DataFrame(A = 1:4, B = ["MMM", "FFFF", "FMF", "MFM"])')
        assert 'MFM' in output and 'FFFF' in output

    def test_put_matrix(self, notebook):
        output = self.put_to_SoS(notebook, '[99 200]')
        assert 'matrix' in output and '99' in output and '200' in output
        #
        output = self.put_to_SoS(notebook, '[88, 2200]')
        assert 'array' in output and '88' in output and '2200' in output

    def test_get_logic_array(self, notebook):
        output = self.get_from_SoS(notebook, '[True, False, True]')
        assert 'Array' in output and 'Bool' in output

    def test_put_logic_array(self, notebook):
        # Note that single element numeric array is treated as single value
        assert '[True, False, True]' == self.put_to_SoS(notebook,
                                                        '[true, false, true]')

    def test_get_str(self, notebook):
        assert '"ab c d"' == self.get_from_SoS(notebook, "'ab c d'")
        assert '"ab\\td"' == self.get_from_SoS(notebook, r"'ab\td'")

    def test_put_str(self, notebook):
        assert "'ab c d'" == self.put_to_SoS(notebook, '"ab c d"')
        assert "'ab\\td'" == self.put_to_SoS(notebook, '"ab\td"')

    def test_get_mixed_list(self, notebook):
        output = self.get_from_SoS(notebook, '[1.4, True, "asd"]')
        assert 'Array' in output and '1.4' in output and '"asd"' in output

    def test_put_mixed_list(self, notebook):
        output = self.put_to_SoS(notebook, '[2.5, true, "haha"]')
        assert '2.5' in output and 'True' in output and 'haha' in output

    def test_get_dict(self, notebook):
        # Python does not have named ordered list, so get dictionary
        output = self.get_from_SoS(notebook, "dict(a=1, b=2.5, c='3')")
        assert 'Dict{String,Any}' in output and '"c"' in output and '"3"' in output and '2.5' in output

    def test_put_dict(self, notebook):
        output = self.put_to_SoS(notebook, """Dict([("A", 1), ("B", 2)])""")
        assert "'B': 2" in output and "'A': 1" in output

    def test_get_set(self, notebook):
        output = self.get_from_SoS(notebook, "{1.5, 'abc'}")
        assert '"abc"' in output and 'Set' in output and '1.5' in output

    def test_put_set(self, notebook):
        output = self.put_to_SoS(notebook, """Set([23, 45, 76])""")
        assert '23' in output and '45' in output and '76' in output and '{' in output and '}' in output

    def test_get_complex(self, notebook):
        assert "1.0 + 2.2im" == self.get_from_SoS(notebook, "complex(1, 2.2)")

    def test_put_complex(self, notebook):
        assert "(4+5j)" == self.put_to_SoS(notebook, "4 + 5im")

    def test_get_recursive(self, notebook):
        output = self.get_from_SoS(notebook,
                                   "{'a': 1, 'b': {'c': 3, 'd': 'whatever'}}")
        assert 'Dict' in output, '"whatever"' in output

    def test_put_recursive(self, notebook):
        output = self.put_to_SoS(
            notebook, 'Dict("a" => 1, "b" => Dict("c" => 3),"d" => "whatever")')
        assert "'b':" in output and "'d': 'whatever'" in output and "'c': 3" in output
