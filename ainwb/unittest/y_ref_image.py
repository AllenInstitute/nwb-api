#!/usr/bin/python
import nwb
import test_utils as ut

# TESTS storage of reference image

def test_refimage_series():
    #fname = "x_refimage_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    name = "refimage"
    create_refimage(fname, name)
    val = ut.verify_present(fname, "acquisition/images/", name)
    #if len(val) != 6:
    if len(val) != 5:
        ut.error("Checking ref image contents", "wrong dimension")
    val = ut.verify_attribute_present(fname, "acquisition/images/"+name, "format")
    #if val != "rawx":
    if val != "raw":
        ut.error("Checking ref image format", "Wrong value")
    val = ut.verify_attribute_present(fname, "acquisition/images/"+name, "description")
    #if val != "tests":
    if val != "test":
        ut.error("Checking ref image description", "Wrong value")

def create_refimage(fname, name):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("reference image test")
    settings["overwrite"] = True
    settings["description"] = "reference image test"
    neurodata = nwb.NWB(**settings)
    neurodata.create_reference_image([1,2,3,4,5], name, "raw", "test")
    neurodata.close()

test_refimage_series()
print("%s PASSED" % __file__)

