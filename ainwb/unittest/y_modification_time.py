#!/usr/bin/python
import h5py
import sys
import nwb
from nwb.nwbco import *
import test_utils as ut
import time

# creates file and modifies it multiple times

if __file__.startswith("./"):
    fname = "x" + __file__[3:-3] + ".nwb"
else:
    fname = "x" + __file__[1:-3] + ".nwb"

settings = {}
settings["filename"] = fname
settings["identifier"] = nwb.create_identifier("Modification example")
settings["overwrite"] = True
settings["description"] = "Modified empty file"
settings["start_time"] = "Sat Jul 04 2015 3:14:16"
neurodata = nwb.NWB(**settings)
neurodata.close()

#time.sleep(1)
settings = {}
settings["filename"] = fname
settings["overwrite"] = False
settings["modify"] = True
neurodata = nwb.NWB(**settings)
neurodata.set_metadata(INSTITUTION, "Allen Institute for Brain Science")
neurodata.close()

#time.sleep(1)
settings = {}
settings["filename"] = fname
settings["overwrite"] = False
settings["modify"] = True
attrs = {}
attrs["phrasebook"] = "Sir William, I cannot wait until lunchtime"
neurodata.set_metadata(EXPERIMENT_DESCRIPTION, "My hovercraft is full of eels", **attrs)
neurodata = nwb.NWB(**settings)
neurodata.close()

f = h5py.File(fname)
dates = f["file_create_date"]
if len(dates) != 3:
    ut.error(__file__, "Expected 3 entries in file_create_date; found %d" % len(dates))

print("%s PASSED" % __file__)

