#!/usr/bin/python
import sys
import nwb
import test_utils as ut

# creates time series without 'data' field
# TESTS softlink of TimeSeries.data

def test_softlink():
    if __file__.startswith("./"):
        fname1 = "x" + __file__[3:-3] + "1" + ".nwb"
        fname2 = "x" + __file__[3:-3] + "2" + ".nwb"
    else:
        fname1 = "x" + __file__[1:-3] + "1" + ".nwb"
        fname2 = "x" + __file__[1:-3] + "2" + ".nwb"
    name1 = "softlink_source"
    name2 = "softlink_reader"
    create_softlink_source(fname1, name1, "acquisition")
    create_softlink_reader(fname2, name2, fname1, name1, "acquisition")
    #
    ut.verify_timeseries(fname1, name1, "acquisition/timeseries", "TimeSeries")
    ut.verify_timeseries(fname2, name2, "acquisition/timeseries", "TimeSeries")
    ##
    val = ut.verify_present(fname2, "acquisition/timeseries/"+name2, "data")

def create_softlink_reader(fname, name, src_fname, src_name, target):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("softlink reader")
    settings["overwrite"] = True
    settings["description"] = "softlink test"
    neurodata = nwb.NWB(**settings)
    source = neurodata.create_timeseries("TimeSeries", name, target)
    source.set_data_as_remote_link(src_fname, "acquisition/timeseries/"+src_name+"/data")
    source.set_time([345])
    source.finalize()
    neurodata.close()

def create_softlink_source(fname, name, target):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("softlink source")
    settings["overwrite"] = True
    settings["description"] = "time series no data test"
    settings["start_time"] = "Sat Jul 04 2015 3:14:16"
    neurodata = nwb.NWB(**settings)
    source = neurodata.create_timeseries("TimeSeries", name, target)
    source.set_data([234], unit="parsec", conversion=1, resolution=1e-3)
    source.set_time([123])
    source.finalize()
    neurodata.close()

test_softlink()
print("%s PASSED" % __file__)

