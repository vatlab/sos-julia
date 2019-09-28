    #!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import os
import tempfile
from sos_notebook.test_utils import NotebookTest


class TestInterface(NotebookTest):
    def test_prompt_color(self, notebook):
        '''test color of input and output prompt'''
        idx = notebook.call('''\
            println("This is Julia")
            ''',
                            kernel="Julia")
        assert [235, 216, 235] == notebook.get_input_backgroundColor(idx)
        assert [235, 216, 235] == notebook.get_output_backgroundColor(idx)

    def test_cd(self, notebook):
        '''Support for change of directory with magic %cd'''
        output1 = notebook.check_output('pwd()', kernel="Julia")
        notebook.call('%cd ..', kernel="SoS")
        output2 = notebook.check_output('pwd()', kernel="Julia")
        assert len(output1) > len(output2)
        assert output1.strip('"').startswith(output2.strip('"'))
        #
        # cd to a specific directory
        tmpdir = os.path.join(tempfile.gettempdir(), 'somedir')
        os.makedirs(tmpdir, exist_ok=True)
        notebook.call(f'%cd {tmpdir}', kernel="SoS")
        output = notebook.check_output('pwd()', kernel="Julia")
        assert os.path.realpath(tmpdir) == os.path.realpath(output.strip('"'))

    def test_sessioninfo(self, notebook):
        '''test support for %sessioninfo'''
        notebook.call('println("This is Julia")', kernel="Julia")
        assert 'Julia' in notebook.check_output('%sessioninfo',
                                                    kernel="SoS")


    # missing test preview
    # missing test name change
