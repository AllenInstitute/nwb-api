#!/usr/bin/python
import nwb
from nwb.nwbco import *
import test_utils as ut

# TESTS fields stored in general/optophysiology

def test_field(fname, name, subdir):
    val = ut.verify_present(fname, "general/optophysiology/"+subdir+"/", name.lower())
    if val != name:
        ut.error("Checking metadata", "field value incorrect")

def test_general_intra():
    #fname = "x_nodata_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    create_general_intra(fname)
    #
    val = ut.verify_present(fname, "general/optophysiology/", "image_custom")
    if val != "IMAGE_CUSTOM":
        ut.error("Checking custom", "Field value incorrect")
    #

    test_field(fname, "DESCRIPTION", "p1")
    test_field(fname, "DEVICE", "p1")
    test_field(fname, "EXCITATION_LAMBDA", "p1")
    test_field(fname, "IMAGE_SITE_CUSTOM", "p1")
    test_field(fname, "IMAGING_RATE", "p1")
    test_field(fname, "INDICATOR", "p1")
    test_field(fname, "LOCATION", "p1")
    val = ut.verify_present(fname, "general/optophysiology/p1/", "manifold")
    if len(val) != 2 or len(val[0]) != 2 or len(val[0][0]) != 3:
        ut.error("Checking manifold", "Incorrect dimensions")
    val = ut.verify_present(fname, "general/optophysiology/p1/red/", "description")
    if val != "DESCRIPTION":
        ut.error("Checking metadata", "field value incorrect")
    val = ut.verify_present(fname, "general/optophysiology/p1/green/", "description")
    if val != "DESCRIPTION":
        ut.error("Checking metadata", "field value incorrect")
    val = ut.verify_present(fname, "general/optophysiology/p1/red/", "emission_lambda")
    if val != "CHANNEL_LAMBDA":
        ut.error("Checking metadata", "field value incorrect")
    val = ut.verify_present(fname, "general/optophysiology/p1/green/", "emission_lambda")
    if val != "CHANNEL_LAMBDA":
        ut.error("Checking metadata", "field value incorrect")


def create_general_intra(fname):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("general optophysiology test")
    settings["overwrite"] = True
    settings["description"] = "test top-level elements in /general/optophysiology"
    neurodata = nwb.NWB(**settings)
    #
    neurodata.set_metadata(IMAGE_CUSTOM("image_custom"), "IMAGE_CUSTOM")
    #
    neurodata.set_metadata(IMAGE_SITE_DESCRIPTION("p1"), "DESCRIPTION")
    # MANUAL CHECK
    # try storing string - -type system should balk
    #neurodata.set_metadata(IMAGE_SITE_MANIFOLD("p1"), "MANIFOLD")
    neurodata.set_metadata(IMAGE_SITE_MANIFOLD("p1"), [[[1,2,3],[2,3,4]],[[3,4,5],[4,5,6]]])
    neurodata.set_metadata(IMAGE_SITE_INDICATOR("p1"), "INDICATOR")
    neurodata.set_metadata(IMAGE_SITE_EXCITATION_LAMBDA("p1"), "EXCITATION_LAMBDA")
    neurodata.set_metadata(IMAGE_SITE_CHANNEL_LAMBDA("p1", "red"), "CHANNEL_LAMBDA")
    neurodata.set_metadata(IMAGE_SITE_CHANNEL_DESCRIPTION("p1", "red"), "DESCRIPTION")
    neurodata.set_metadata(IMAGE_SITE_CHANNEL_LAMBDA("p1", "green"), "CHANNEL_LAMBDA")
    neurodata.set_metadata(IMAGE_SITE_CHANNEL_DESCRIPTION("p1", "green"), "DESCRIPTION")
    neurodata.set_metadata(IMAGE_SITE_IMAGING_RATE("p1"), "IMAGING_RATE")
    neurodata.set_metadata(IMAGE_SITE_LOCATION("p1"), "LOCATION")
    neurodata.set_metadata(IMAGE_SITE_DEVICE("p1"), "DEVICE")
    neurodata.set_metadata(IMAGE_SITE_CUSTOM("p1", "image_site_custom"), "IMAGE_SITE_CUSTOM")
    #
    neurodata.close()

test_general_intra()
print "%s PASSED" % __file__

