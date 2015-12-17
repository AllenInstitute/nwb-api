#!/usr/bin/python
import test_utils as ut
import numpy as np
import nwb

# test opening file in append mode
# TESTS creating a module
# TESTS creating an interface
# TESTS adding a timeseries to an interface

def test_file():
    if __file__.startswith("./"):
        fname = "x" + __file__[3:-3] + ".nwb"
    else:
        fname = "x" + __file__[1:-3] + ".nwb"
    create_iface_series(fname, True)
    name1 = "Ones"
    ut.verify_timeseries(fname, name1, "processing/test module/BehavioralEvents", "TimeSeries")


def create_iface_series(fname, newfile):
    settings = {}
    settings["filename"] = fname
    if newfile:
        settings["identifier"] = nwb.create_identifier("interface timeseries example")
        settings["overwrite"] = True
        settings["start_time"] = "Sat Jul 04 2015 3:14:16"
        settings["description"] = "Test interface timeseries file"
    else:
        settings["modify"] = True
    neurodata = nwb.NWB(**settings)
    #
    mod = neurodata.create_module("test module")
    iface = mod.create_interface("BehavioralEvents")
    ts = neurodata.create_timeseries("TimeSeries", "Ones")
    ts.set_data(np.ones(10), unit="Event", conversion=1.0, resolution=float('nan'))
    ts.set_value("num_samples", 10)
    ts.set_time(np.arange(10))
    iface.add_timeseries(ts)
    iface.finalize()
    mod.finalize()
    #
    neurodata.close()

test_file()
print("%s PASSED" % __file__)

