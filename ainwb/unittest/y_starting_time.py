#!/usr/bin/python
import nwb
import test_utils as ut

# TESTS use of TimeSeries.starting_time

def test_nodata_series():
    #fname = "x_nodata_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    name = "starting_time"
    create_startingtime_series(fname, name, "acquisition")
    ut.verify_timeseries(fname, name, "acquisition/timeseries", "TimeSeries")
    ut.verify_absent(fname, "acquisition/timeseries/"+name, "timestamps")
    val = ut.verify_present(fname, "acquisition/timeseries/"+name, "starting_time")
    if val != 0.125:
        ut.error("Checking start time", "Incorrect value")
    val = ut.verify_attribute_present(fname, "acquisition/timeseries/starting_time/"+name, "rate")
    if val != 2:
        ut.error("Checking rate", "Incorrect value")

def create_startingtime_series(fname, name, target):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("starting time test")
    settings["overwrite"] = True
    settings["description"] = "time series starting time test"
    settings["start_time"] = "Sat Jul 04 2015 3:14:16"
    neurodata = nwb.NWB(**settings)
    #
    stime = neurodata.create_timeseries("TimeSeries", name, target)
    stime.set_data([0, 1, 2, 3], unit="n/a", conversion=1, resolution=1)
    stime.set_value("num_samples", 4)
    stime.set_time_by_rate(0.125, 2)
    #
    stime.finalize()
    neurodata.close()

test_nodata_series()
print "%s PASSED" % __file__

