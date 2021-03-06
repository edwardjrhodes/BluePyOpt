"""bluepyopt.ephys.simulators tests"""

"""
Copyright (c) 2016, EPFL/Blue Brain Project

 This file is part of BluePyOpt <https://github.com/BlueBrain/BluePyOpt>

 This library is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License version 3.0 as published
 by the Free Software Foundation.

 This library is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 details.

 You should have received a copy of the GNU Lesser General Public License
 along with this library; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# pylint:disable=W0612

import types
import nose.tools as nt
from nose.plugins.attrib import attr

import bluepyopt.ephys as ephys


@attr('unit')
def test_nrnsimulator_init():
    """ephys.simulators: test if NrnSimulator constructor works"""

    neuron_sim = ephys.simulators.NrnSimulator()
    nt.assert_is_instance(neuron_sim, ephys.simulators.NrnSimulator)


@attr('unit')
def test_neuron_import():
    """ephys.simulators: test if bluepyopt.neuron import was successful"""
    from bluepyopt import ephys  # NOQA
    neuron_sim = ephys.simulators.NrnSimulator()
    nt.assert_is_instance(neuron_sim.neuron, types.ModuleType)
