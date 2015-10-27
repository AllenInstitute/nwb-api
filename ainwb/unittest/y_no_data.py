#!/usr/bin/python
import sys
import nwb
import test_utils as ut

# creates time series without 'data' field
# TESTS TimeSeries.ignore_data()

def test_nodata_series():
    #fname = "x_nodata_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    name = "nodata"
    create_nodata_series(fname, name, "acquisition")
    ut.verify_timeseries(fname, name, "acquisition/timeseries", "TimeSeries")
    ut.verify_absent(fname, "acquisition/timeseries/"+name, "data")

def create_nodata_series(fname, name, target):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("nodata example")
    settings["overwrite"] = True
    settings["description"] = "time series no data test"
    settings["start_time"] = "Sat Jul 04 2015 3:14:16"
    neurodata = nwb.NWB(**settings)
    #
    nodata = neurodata.create_timeseries("TimeSeries", name, target)
    nodata.ignore_data()
    nodata.set_time([0])
    #
    nodata.finalize()
    neurodata.close()

test_nodata_series()
print("%s PASSED" % __file__)

