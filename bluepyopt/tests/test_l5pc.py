"""Test l5pc example"""

import os
import sys
from contextlib import contextmanager
from StringIO import StringIO

import nose.tools as nt

L5PC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '../../examples/l5pc'))

sys.path.insert(0, L5PC_PATH)

import bluepyopt
from bluepyopt import ephys

neuron_sim = ephys.simulators.NrnSimulator()

neuron_sim.neuron.h.nrn_load_dll(
    os.path.join(
        L5PC_PATH,
        'x86_64/.libs/libnrnmech.so'))


# Parameters in release circuit model
release_parameters = {
    'gNaTs2_tbar_NaTs2_t.apical': 0.026145,
    'gSKv3_1bar_SKv3_1.apical': 0.004226,
    'gImbar_Im.apical': 0.000143,
    'gNaTa_tbar_NaTa_t.axonal': 3.137968,
    'gK_Tstbar_K_Tst.axonal': 0.089259,
    'gamma_CaDynamics_E2.axonal': 0.002910,
    'gNap_Et2bar_Nap_Et2.axonal': 0.006827,
    'gSK_E2bar_SK_E2.axonal': 0.007104,
    'gCa_HVAbar_Ca_HVA.axonal': 0.000990,
    'gK_Pstbar_K_Pst.axonal': 0.973538,
    'gSKv3_1bar_SKv3_1.axonal': 1.021945,
    'decay_CaDynamics_E2.axonal': 287.198731,
    'gCa_LVAstbar_Ca_LVAst.axonal': 0.008752,
    'gamma_CaDynamics_E2.somatic': 0.000609,
    'gSKv3_1bar_SKv3_1.somatic': 0.303472,
    'gSK_E2bar_SK_E2.somatic': 0.008407,
    'gCa_HVAbar_Ca_HVA.somatic': 0.000994,
    'gNaTs2_tbar_NaTs2_t.somatic': 0.983955,
    'decay_CaDynamics_E2.somatic': 210.485284,
    'gCa_LVAstbar_Ca_LVAst.somatic': 0.000333
}


def load_from_json(filename):
    """Load structure from json"""

    import json

    with open(filename) as json_file:
        return json.load(json_file)


def dump_to_json(content, filename):
    """Dump structure to json"""

    import json

    with open(filename, 'w') as json_file:
        return json.dump(content, json_file, indent=4, separators=(',', ': '))


def test_import():
    """L5PC: test import"""

    import l5pc_model  # NOQA
    import l5pc_evaluator  # NOQA
    import opt_l5pc  # NOQA

    # Delete the optimisation inside the module
    del opt_l5pc.opt


class TestL5PCModel(object):

    """Test L5PC model"""

    def __init__(self):
        self.l5pc_cell = None
        self.nrn = None

    def setup(self):
        """Set up class"""
        sys.path.insert(0, L5PC_PATH)

        import l5pc_model  # NOQA
        self.l5pc_cell = l5pc_model.create()
        nt.assert_is_instance(
            self.l5pc_cell,
            bluepyopt.ephys.models.CellModel)
        self.nrn = ephys.simulators.NrnSimulator()

    def test_instantiate(self):
        """L5PC: test instantiation of l5pc cell model"""
        self.l5pc_cell.freeze(release_parameters)
        self.l5pc_cell.instantiate(sim=self.nrn)

    def teardown(self):
        """Teardown"""
        self.l5pc_cell.destroy()


class TestL5PCEvaluator(object):

    """Test L5PC evaluator"""

    def __init__(self):
        self.l5pc_evaluator = None

    def setup(self):
        """Set up class"""

        import l5pc_evaluator  # NOQA

        self.l5pc_evaluator = l5pc_evaluator.create()

        nt.assert_is_instance(
            self.l5pc_evaluator,
            bluepyopt.ephys.evaluators.CellEvaluator)

    def test_eval(self):
        """L5PC: test evaluation of l5pc evaluator"""

        result = self.l5pc_evaluator.evaluate_with_dicts(
            param_dict=release_parameters)

        expected_results = load_from_json('expected_results.json')

        # Use two lines below to update expected result
        # expected_results['TestL5PCEvaluator.test_eval'] = result
        # dump_to_json(expected_results, 'expected_results.json')

        nt.assert_items_equal(
            result,
            expected_results['TestL5PCEvaluator.test_eval'])

    def teardown(self):
        """Teardown"""
        pass


# backport from python 3.4
@contextmanager
def stdout_redirector(stream):
    """Stdout redirector"""
    old_stdout = sys.stdout
    sys.stdout = stream
    try:
        yield
    finally:
        sys.stdout = old_stdout


def test_exec():
    """L5PC Notebook: test execution"""
    old_cwd = os.getcwd()
    output = StringIO()
    try:
        os.chdir(L5PC_PATH)
        with stdout_redirector(output):
            # When using import instead of execfile this doesn't work
            # Probably because multiprocessing doesn't work correctly during
            # import
            execfile('L5PC.py')  # NOQA
        stdout = output.getvalue()
        # first and last values of optimal individual
        nt.ok_('0.001017834439738432' in stdout)
        nt.ok_('202.18814057682334' in stdout)
        nt.ok_(
            "u'gamma_CaDynamics_E2.somatic': 0.03229357096515606" in stdout)
    finally:
        os.chdir(old_cwd)
        output.close()
