#!/usr/bin/python
import nwb
import test_utils as ut

# TESTS top-level datasets

def test_refimage_series():
    #fname = "x_refimage_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    name = "refimage"
    create_refimage(fname, name)
    val = ut.verify_present(fname, "/", "identifier")
    #if val != "vwxa":
    if val != "vwx":
        ut.error("Checking file idenfier", "wrong contents")
    val = ut.verify_present(fname, "/", "file_create_date")
    val = ut.verify_present(fname, "/", "session_start_time")
    #if val != "xyza":
    if val != "xyz":
        ut.error("Checking session start time", "wrong contents")
    val = ut.verify_present(fname, "/", "session_description")
    #if val != "wxya":
    if val != "wxy":
        ut.error("Checking session start time", "wrong contents")

def create_refimage(fname, name):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = "vwx"
    settings["overwrite"] = True
    settings["description"] = "wxy"
    settings["start_time"] = "xyz"
    neurodata = nwb.NWB(**settings)
    neurodata.close()

test_refimage_series()
print("%s PASSED" % __file__)

