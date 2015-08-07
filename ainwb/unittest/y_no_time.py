#!/usr/bin/python
import sys
import nwb
import test_utils as ut

# creates time series without 'timestamps' or 'starting_time' fields
# TESTS TimeSeries.ignore_time()
# TESTS timeseries placement in acquisition, stimulus, templates

def test_notime_series():
    #fname = "x_notime_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    name = "notime"
    create_notime_series(fname, name, "acquisition")
    ut.verify_timeseries(fname, name, "acquisition/timeseries", "TimeSeries")
    ut.verify_absent(fname, "acquisition/timeseries/"+name, "timestamps")
    ut.verify_absent(fname, "acquisition/timeseries/"+name, "starting_time")

    create_notime_series(fname, name, "stimulus")
    ut.verify_timeseries(fname, name, "stimulus/presentation", "TimeSeries")
    create_notime_series(fname, name, "template")
    ut.verify_timeseries(fname, name, "stimulus/templates", "TimeSeries")

def create_notime_series(fname, name, target):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("notime example")
    settings["overwrite"] = True
    settings["start_time"] = "Sat Jul 04 2015 3:14:16"
    settings["description"] = "Test no time"
    neurodata = nwb.NWB(**settings)
    #
    notime = neurodata.create_timeseries("TimeSeries", name, target)
    notime.ignore_time()
    notime.set_data([0], unit="n/a", conversion=1, resolution=1)
    #
    notime.finalize()
    neurodata.close()

test_notime_series()
print "%s PASSED" % __file__

