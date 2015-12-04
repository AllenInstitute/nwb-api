#!/usr/bin/python
import nwb
import test_utils as ut

# TESTS storage of retonotopic imaging data

def test_axis(fname, iname, num):
    val = ut.verify_present(fname, iname, "axis_"+num+"_phase_map")
    if len(val) != 2 or len(val[0]) != 3:
        ut.error("Checking axis-"+num, "wrong dimension")
    if num == "1": 
        if val[0][0] != 1.0:
            ut.error("Checking axis-"+num, "wrong contents")
    elif num == "2":
        if val[0][0] != 3.0:
            ut.error("Checking axis-"+num+" contents", "wrong contents")
    val = ut.verify_attribute_present(fname, iname+"/axis_"+num+"_phase_map", "unit")
    if not ut.strcmp(val, "degrees"):
        ut.error("Checking axis-"+num+" unit", "Wrong value")
    val = ut.verify_attribute_present(fname, iname+"/axis_"+num+"_phase_map", "dimension")
    if val[0] != 2 or val[1] != 3:
        ut.error("Double-checking axis-"+num+" dimension", "Wrong value")
    val = ut.verify_attribute_present(fname, iname+"/axis_"+num+"_phase_map", "field_of_view")
    if val[0] != .1 or val[1] != .1:
        ut.error("Checking axis-"+num+" field-of-view", "Wrong value")
    # now check power map. it only exists for axis 1
    if num == "1":
        val = ut.verify_present(fname, iname, "axis_"+num+"_phase_map")
        if len(val) != 2 or len(val[0]) != 3:
            ut.error("Checking axis-"+num+" power map", "wrong dimension")
        val = ut.verify_attribute_present(fname, iname+"/axis_"+num+"_power_map", "dimension")
        if val[0] != 2 or val[1] != 3:
            ut.error("Double-checking axis-"+num+"-power dimension", "Wrong value")
        val = ut.verify_attribute_present(fname, iname+"/axis_"+num+"_power_map", "field_of_view")
        if val[0] != .1 or val[1] != .1:
            ut.error("Checking axis-"+num+"-power field-of-view", "Wrong value")

def test_image(fname, iname, img):
    val = ut.verify_present(fname, iname, img)
    if len(val) != 2 or len(val[0]) != 3:
        ut.error("Checking image "+img, "wrong dimension")
    if val[1][1] != 144:
        ut.error("Checking image "+img, "wrong contents")
    val = ut.verify_attribute_present(fname, iname+"/"+img, "format")
    if not ut.strcmp(val, "raw"):
        ut.error("Checking image "+img+" format", "wrong contents")
    val = ut.verify_attribute_present(fname, iname+"/"+img, "dimension")
    if len(val) != 2 or val[0] != 2 or val[1] != 3:
        ut.error("Checking image "+img+" dimension", "wrong contents")
    val = ut.verify_attribute_present(fname, iname+"/"+img, "bits_per_pixel")
    if val != 8:
        ut.error("Checking image "+img+" bpp", "wrong contents")

def test_sign_map(fname, iname):
    val = ut.verify_present(fname, iname, "sign_map")
    if len(val) != 2 or len(val[0]) != 3:
        ut.error("Checking sign map", "wrong dimension")
    if val[1][1] != -.5:
        ut.error("Checking sign map", "wrong content")
    val = ut.verify_attribute_present(fname, iname+"/sign_map", "dimension")
    if len(val) != 2 or val[0] != 2 or val[1] != 3:
        ut.error("Checking sign map dimension", "wrong contents")


def test_isi_iface():
    if __file__.startswith("./"):
        fname = "x" + __file__[3:-3] + ".nwb"
    else:
        fname = "x" + __file__[1:-3] + ".nwb"
    name = "test_module"
    iname = "processing/" + name + "/Imaging_Retinotopy"
    create_isi_iface(fname, name)

    test_axis(fname, iname, "1")
    test_axis(fname, iname, "2")
    val = ut.verify_present(fname, iname, "axis_descriptions")
    if len(val) != 2:
        ut.error("Checking axis_description", "wrong dimension")
    if not ut.strcmp(val[0], "altitude") or not ut.strcmp(val[1], "azimuth"):
        ut.error("Checking axis_description", "wrong contents")
    test_image(fname, iname, "vasculature_image")
    test_image(fname, iname, "focal_depth_image")
    test_sign_map(fname, iname)


# TODO sign map
# TODO dimension of response axes

def create_isi_iface(fname, name):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("reference image test")
    settings["overwrite"] = True
    settings["description"] = "reference image test"
    neurodata = nwb.NWB(**settings)
    module = neurodata.create_module(name)
    iface = module.create_interface("Imaging_Retinotopy")
    iface.add_axis_1_phase_map([[1.0, 1.1, 1.2],[2.0,2.1,2.2]], "altitude", .1, .1)
    iface.add_axis_2_phase_map([[3.0, 3.1, 3.2],[4.0,4.1,4.2]], "azimuth", .1, .1, unit="degrees")
    iface.add_axis_1_power_map([[0.1, 0.2, 0.3],[0.4, 0.5, 0.6]], .1, .1)
    iface.add_sign_map([[-.1, .2, -.3],[.4,-.5,.6]])
    iface.add_vasculature_image([[1,0,129],[2,144,0]])
    iface.add_focal_depth_image([[1,0,129],[2,144,0]], 8)
    iface.finalize()
    module.finalize()
    neurodata.close()

test_isi_iface()
print("%s PASSED" % __file__)

