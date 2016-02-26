#!/usr/bin/python
import h5py
import sys
import nwb
import test_utils as ut

# TESTS creation of UnitTimes interface and data stored within


def test_unit_times():
    if __file__.startswith("./"):
        fname = "x" + __file__[3:-3] + ".nwb"
    else:
        fname = "x" + __file__[1:-3] + ".nwb"
    # create the file we're going to use
    ndata = create_empty_file(fname)
    # create a module to store processed data
    mod = ndata.create_module("my spike times")
    # ad a unit times interface to the module
    iface = mod.create_interface("UnitTimes")
    # make some data to store
    spikes = create_spikes()
    for i in range(len(spikes)):
        iface.add_unit(unit_name = "unit-%d" % i, 
                      unit_times = spikes[i], 
                     description = "<description of unit>",
                          source = "Data spike-sorted by B. Bunny")

    # clean up and close objects
    iface.finalize()
    mod.finalize()
    ndata.close()

    # test random sample to make sure data was stored correctly
    h5 = h5py.File(fname)
    times = h5["processing/my spike times/UnitTimes/unit-0/times"].value
    assert len(times) == len(spikes[0]), "Spike count for unit-0 wrong"
    assert abs(times[1] - spikes[0][1]) < 0.001, "Wrong time found in file"
    h5.close()


def create_spikes():
    spikes = []
    spikes.append([1.3, 1.4, 1.9, 2.1, 2.2, 2.3])
    spikes.append([2.2, 3.0])
    spikes.append([0.3, 0.4, 1.0, 1.1, 1.45, 1.8, 1.81, 2.2])
    return spikes

def create_empty_file(fname):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("UnitTimes example")
    settings["overwrite"] = True
    settings["start_time"] = "Sat Jul 04 2015 3:14:16"
    settings["description"] = "Test file with spike times in processing module"
    neurodata = nwb.NWB(**settings)
    return neurodata

test_unit_times()
print("%s PASSED" % __file__)

