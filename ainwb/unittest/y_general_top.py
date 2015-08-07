#!/usr/bin/python
import nwb
from nwb.nwbco import *
import test_utils as ut

# TESTS top-level fields stored in general
# TESTS storing metadata from file
# TESTS 'Custom' tagging on custom attributes

def test_field(fname, name):
    val = ut.verify_present(fname, "general/", name.lower())
    if val != name:
        ut.error("Checking metadata", "field value incorrect")

def test_general_top():
    #fname = "x_nodata_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    create_general_top(fname)
    test_field(fname, "DATA_COLLECTION")
    test_field(fname, "EXPERIMENT_DESCRIPTION")
    test_field(fname, "EXPERIMENTER")
    test_field(fname, "INSTITUTION")
    test_field(fname, "LAB")
    test_field(fname, "NOTES")
    test_field(fname, "PROTOCOL")
    test_field(fname, "PHARMACOLOGY")
    test_field(fname, "RELATED_PUBLICATIONS")
    test_field(fname, "SESSION_ID")
    test_field(fname, "SLICES")
    test_field(fname, "STIMULUS")
    test_field(fname, "SURGERY")
    test_field(fname, "VIRUS")
    val = ut.verify_present(fname, "general/", "source_script")
    if len(val) < 1000:
        ut.error("Checking metadata_from_file", "unexpected field size")
    val = ut.verify_attribute_present(fname, "general/source_script", "neurodata_type")
    if val != "Custom":
        ut.error("Checking custom tag", "neurodata_type incorrect")


def create_general_top(fname):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("general top test")
    settings["overwrite"] = True
    settings["description"] = "test top-level elements in /general"
    neurodata = nwb.NWB(**settings)
    #
    neurodata.set_metadata(DATA_COLLECTION, "DATA_COLLECTION")
    neurodata.set_metadata(EXPERIMENT_DESCRIPTION, "EXPERIMENT_DESCRIPTION")
    neurodata.set_metadata(EXPERIMENTER, "EXPERIMENTER")
    neurodata.set_metadata(INSTITUTION, "INSTITUTION")
    neurodata.set_metadata(LAB, "LAB")
    neurodata.set_metadata(NOTES, "NOTES")
    neurodata.set_metadata(PROTOCOL, "PROTOCOL")
    neurodata.set_metadata(PHARMACOLOGY, "PHARMACOLOGY")
    neurodata.set_metadata(RELATED_PUBLICATIONS, "RELATED_PUBLICATIONS")
    neurodata.set_metadata(SESSION_ID, "SESSION_ID")
    neurodata.set_metadata(SLICES, "SLICES")
    neurodata.set_metadata(STIMULUS, "STIMULUS")
    neurodata.set_metadata(SURGERY, "SURGERY")
    neurodata.set_metadata(VIRUS, "VIRUS")
    #
    neurodata.set_metadata_from_file("source_script", __file__)
    #
    neurodata.close()

test_general_top()
print "%s PASSED" % __file__

