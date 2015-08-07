#!/usr/bin/python
import nwb
from nwb.nwbco import *
import test_utils as ut

# TESTS fields stored in general/intracellular_ephys

def test_field(fname, name, subdir):
    val = ut.verify_present(fname, "general/intracellular_ephys/"+subdir+"/", name.lower())
    if val != name:
        ut.error("Checking metadata", "field value incorrect")

def test_general_intra():
    #fname = "x_nodata_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    create_general_intra(fname)
    #
    val = ut.verify_present(fname, "general/intracellular_ephys/", "intra_custom")
    if val != "INTRA_CUSTOM":
        ut.error("Checking custom", "Field value incorrect")
    #

    test_field(fname, "DESCRIPTION", "p1")
    test_field(fname, "FILTERING", "p1")
    test_field(fname, "DEVICE", "p1")
    test_field(fname, "LOCATION", "p1")
    test_field(fname, "RESISTANCE", "p1")
    test_field(fname, "SLICE", "p1")
    test_field(fname, "SEAL", "p1")
    test_field(fname, "INITIAL_ACCESS_RESISTANCE", "p1")
    test_field(fname, "INTRA_ELECTRODE_CUSTOM", "p1")
    #
    test_field(fname, "DESCRIPTION", "e2")
    test_field(fname, "FILTERING", "e2")
    test_field(fname, "DEVICE", "e2")
    test_field(fname, "LOCATION", "e2")
    test_field(fname, "RESISTANCE", "e2")
    test_field(fname, "SLICE", "e2")
    test_field(fname, "SEAL", "e2")
    test_field(fname, "INITIAL_ACCESS_RESISTANCE", "e2")
    test_field(fname, "INTRA_ELECTRODE_CUSTOM", "e2")


def create_general_intra(fname):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("general intracellular test")
    settings["overwrite"] = True
    settings["description"] = "test top-level elements in /general/intracellular_ephys"
    neurodata = nwb.NWB(**settings)
    #
    neurodata.set_metadata(INTRA_CUSTOM("intra_custom"), "INTRA_CUSTOM")
    #
    neurodata.set_metadata(INTRA_ELECTRODE_DESCRIPTION("p1"), "DESCRIPTION")
    neurodata.set_metadata(INTRA_ELECTRODE_FILTERING("p1"), "FILTERING")
    neurodata.set_metadata(INTRA_ELECTRODE_DEVICE("p1"), "DEVICE")
    neurodata.set_metadata(INTRA_ELECTRODE_LOCATION("p1"), "LOCATION")
    neurodata.set_metadata(INTRA_ELECTRODE_RESISTANCE("p1"), "RESISTANCE")
    neurodata.set_metadata(INTRA_ELECTRODE_SEAL("p1"), "SEAL")
    neurodata.set_metadata(INTRA_ELECTRODE_SLICE("p1"), "SLICE")
    neurodata.set_metadata(INTRA_ELECTRODE_INIT_ACCESS_RESISTANCE("p1"), "INITIAL_ACCESS_RESISTANCE")
    neurodata.set_metadata(INTRA_ELECTRODE_CUSTOM("p1", "intra_electrode_custom"), "INTRA_ELECTRODE_CUSTOM")
    #
    neurodata.set_metadata(INTRA_ELECTRODE_DESCRIPTION("e2"), "DESCRIPTION")
    neurodata.set_metadata(INTRA_ELECTRODE_FILTERING("e2"), "FILTERING")
    neurodata.set_metadata(INTRA_ELECTRODE_DEVICE("e2"), "DEVICE")
    neurodata.set_metadata(INTRA_ELECTRODE_LOCATION("e2"), "LOCATION")
    neurodata.set_metadata(INTRA_ELECTRODE_RESISTANCE("e2"), "RESISTANCE")
    neurodata.set_metadata(INTRA_ELECTRODE_SEAL("e2"), "SEAL")
    neurodata.set_metadata(INTRA_ELECTRODE_SLICE("e2"), "SLICE")
    neurodata.set_metadata(INTRA_ELECTRODE_INIT_ACCESS_RESISTANCE("e2"), "INITIAL_ACCESS_RESISTANCE")
    neurodata.set_metadata(INTRA_ELECTRODE_CUSTOM("e2", "intra_electrode_custom"), "INTRA_ELECTRODE_CUSTOM")
    #
    neurodata.close()

test_general_intra()
print "%s PASSED" % __file__

