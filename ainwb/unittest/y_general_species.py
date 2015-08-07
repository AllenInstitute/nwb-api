#!/usr/bin/python
import nwb
from nwb.nwbco import *
import test_utils as ut

# TESTS top-level fields stored in general

def test_field(fname, name):
    val = ut.verify_present(fname, "general/subject/", name.lower())
    if val != name:
        ut.error("Checking metadata", "field value incorrect")

def test_general_subject():
    #fname = "x_nodata_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    create_general_subject(fname)
    val = ut.verify_present(fname, "general/subject/", "description")
    if val != "SUBJECT":
        ut.error("Checking metadata", "field value incorrect")
    test_field(fname, "SUBJECT_ID")
    test_field(fname, "SPECIES")
    test_field(fname, "GENOTYPE")
    test_field(fname, "SEX")
    test_field(fname, "AGE")
    test_field(fname, "WEIGHT")


def create_general_subject(fname):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("general top test")
    settings["overwrite"] = True
    settings["description"] = "test top-level elements in /general"
    neurodata = nwb.NWB(**settings)
    #
    neurodata.set_metadata(SUBJECT, "SUBJECT")
    neurodata.set_metadata(SUBJECT_ID, "SUBJECT_ID")
    neurodata.set_metadata(SPECIES, "SPECIES")
    neurodata.set_metadata(GENOTYPE, "GENOTYPE")
    neurodata.set_metadata(SEX, "SEX")
    neurodata.set_metadata(AGE, "AGE")
    neurodata.set_metadata(WEIGHT, "WEIGHT")
    #
    neurodata.close()

test_general_subject()
print "%s PASSED" % __file__

