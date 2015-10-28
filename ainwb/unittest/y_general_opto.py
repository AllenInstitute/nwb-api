#!/usr/bin/python
import nwb
from nwb.nwbco import *
import test_utils as ut

# TESTS fields stored in general/optogenetics

def test_field(fname, name, subdir):
    val = ut.verify_present(fname, "general/optogenetics/"+subdir+"/", name.lower())
    if not ut.strcmp(val, name):
        ut.error("Checking metadata", "field value incorrect")

def test_general_optogen():
    if __file__.startswith("./"):
        fname = "x" + __file__[3:-3] + ".nwb"
    else:
        fname = "x" + __file__[1:-3] + ".nwb"
    create_general_optogen(fname)
    #
    val = ut.verify_present(fname, "general/optogenetics/", "optogen_custom")
    if not ut.strcmp(val, "OPTOGEN_CUSTOM"):
        ut.error("Checking custom", "Field value incorrect")
    #

    test_field(fname, "DESCRIPTION", "p1")
    #test_field(fname, "DESCRIPTIONx", "p1")
    #test_field(fname, "DESCRIPTION", "p1x")
    test_field(fname, "DEVICE", "p1")
    test_field(fname, "LAMBDA", "p1")
    test_field(fname, "LOCATION", "p1")
    val = ut.verify_present(fname, "general/optogenetics/p1/", "optogen_site_custom") 
    if not ut.strcmp(val, "OPTOGEN_SITE_CUSTOM"):
        ut.error("Checking metadata", "field value incorrect")


def create_general_optogen(fname):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("metadata optogenetic test")
    settings["overwrite"] = True
    settings["description"] = "test elements in /general/optogentics"
    neurodata = nwb.NWB(**settings)
    #
    neurodata.set_metadata(OPTOGEN_CUSTOM("optogen_custom"), "OPTOGEN_CUSTOM")
    #
    neurodata.set_metadata(OPTOGEN_SITE_DESCRIPTION("p1"), "DESCRIPTION")
    neurodata.set_metadata(OPTOGEN_SITE_DEVICE("p1"), "DEVICE")
    neurodata.set_metadata(OPTOGEN_SITE_LAMBDA("p1"), "LAMBDA")
    neurodata.set_metadata(OPTOGEN_SITE_LOCATION("p1"), "LOCATION")
    neurodata.set_metadata(OPTOGEN_SITE_CUSTOM("p1", "optogen_site_custom"), "OPTOGEN_SITE_CUSTOM")
    #
    neurodata.close()

test_general_optogen()
print("%s PASSED" % __file__)

