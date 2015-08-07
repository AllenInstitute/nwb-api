#!/usr/bin/python
import nwb
from nwb.nwbco import *
import test_utils as ut

# TESTS fields stored in general/extracellular_ephys

def test_field(fname, name, subdir):
    val = ut.verify_present(fname, "general/extracellular_ephys/"+subdir+"/", name.lower())
    if val != name:
        ut.error("Checking metadata", "field value incorrect")

def test_general_extra():
    #fname = "x_nodata_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    create_general_extra(fname)
    #
    val = ut.verify_present(fname, "general/extracellular_ephys", "electrode_map")
    if len(val) != 2 and len(val[0]) != 3:
        ut.error("Checking electrode map", "incorrect dimensions")
    #
    val = ut.verify_present(fname, "general/extracellular_ephys", "electrode_group")
    if len(val) != 2:
        ut.error("Checking electrode group", "incorrect dimensions")
    if val[0] != "p1" or val[1] != "p2":
        ut.error("Checking electrode group", "incorrect values")
    #
    val = ut.verify_present(fname, "general/extracellular_ephys", "impedance")
    if len(val) != 2:
        ut.error("Checking electrode impedance", "incorrect dimensions")
    #
    val = ut.verify_present(fname, "general/extracellular_ephys/", "filtering")
    if val != "EXTRA_FILTERING":
        ut.error("Checking filtering", "Field value incorrect")
    #
    val = ut.verify_present(fname, "general/extracellular_ephys/", "EXTRA_CUSTOM")
    if val != "EXTRA_CUSTOM":
        ut.error("Checking custom", "Field value incorrect")
    #

    test_field(fname, "DESCRIPTION", "p1")
    test_field(fname, "LOCATION", "p1")
    test_field(fname, "DEVICE", "p1")
    test_field(fname, "EXTRA_SHANK_CUSTOM", "p1")
    test_field(fname, "DESCRIPTION", "p2")
    test_field(fname, "LOCATION", "p2")
    test_field(fname, "DEVICE", "p2")
    test_field(fname, "EXTRA_SHANK_CUSTOM", "p2")


def create_general_extra(fname):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("general extracellular test")
    settings["overwrite"] = True
    settings["description"] = "test elements in /general/extracellular_ephys"
    neurodata = nwb.NWB(**settings)
    #
    neurodata.set_metadata(EXTRA_ELECTRODE_MAP, [[1,1,1], [1,2,3]])
    neurodata.set_metadata(EXTRA_ELECTRODE_GROUP, ["p1", "p2"])
    neurodata.set_metadata(EXTRA_IMPEDANCE, [1.0e6, 2.0e6])
    neurodata.set_metadata(EXTRA_FILTERING, "EXTRA_FILTERING")
    neurodata.set_metadata(EXTRA_CUSTOM("EXTRA_CUSTOM"), "EXTRA_CUSTOM")

    neurodata.set_metadata(EXTRA_SHANK_DESCRIPTION("p1"), "DESCRIPTION")
    neurodata.set_metadata(EXTRA_SHANK_LOCATION("p1"), "LOCATION")
    neurodata.set_metadata(EXTRA_SHANK_DEVICE("p1"), "DEVICE")
    neurodata.set_metadata(EXTRA_SHANK_CUSTOM("p1", "extra_shank_custom"), "EXTRA_SHANK_CUSTOM")
    #
    neurodata.set_metadata(EXTRA_SHANK_DESCRIPTION("p2"), "DESCRIPTION")
    neurodata.set_metadata(EXTRA_SHANK_LOCATION("p2"), "LOCATION")
    neurodata.set_metadata(EXTRA_SHANK_DEVICE("p2"), "DEVICE")
    neurodata.set_metadata(EXTRA_SHANK_CUSTOM("p2", "extra_shank_custom"), "EXTRA_SHANK_CUSTOM")
    #
    neurodata.close()

test_general_extra()
print "%s PASSED" % __file__

