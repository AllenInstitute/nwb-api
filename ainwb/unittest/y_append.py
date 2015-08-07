#!/usr/bin/python
import test_utils as ut
import nwb

# test opening file in append mode
# TESTS modifying existing file
# TESTS creation of modification_time
# TESTS addition of TimeSeries to existing file
# TESTS preservation of TimeSeries when file modified

def test_append():
    #fname = "x_annotation_series_acq.nwb"
    fname = "x" + __file__[3:-3] + ".nwb"
    name1 = "annot1"
    name2 = "annot2"
    create_annotation_series(fname, name1, "acquisition", True)
    create_annotation_series(fname, name2, "acquisition", False)
    ut.verify_timeseries(fname, name1, "acquisition/timeseries", "TimeSeries")
    ut.verify_timeseries(fname, name1, "acquisition/timeseries", "AnnotationSeries")
    ut.verify_timeseries(fname, name2, "acquisition/timeseries", "TimeSeries")
    ut.verify_timeseries(fname, name2, "acquisition/timeseries", "AnnotationSeries")
    ut.verify_attribute_present(fname, "file_create_date", "modification_time")


def create_annotation_series(fname, name, target, newfile):
    settings = {}
    settings["filename"] = fname
    if newfile:
        settings["identifier"] = nwb.create_identifier("annotation example")
        settings["overwrite"] = True
        settings["start_time"] = "Sat Jul 04 2015 3:14:16"
        settings["description"] = "Test file with AnnotationSeries"
    else:
        settings["modify"] = True
    neurodata = nwb.NWB(**settings)
    #
    annot = neurodata.create_timeseries("AnnotationSeries", name, target)
    annot.set_description("This is an AnnotationSeries with sample data")
    annot.set_comment("The comment and description fields can store arbitrary human-readable data")
    annot.set_source("Observation of Dr. J Doe")
    #
    annot.add_annotation("Rat in bed, beginning sleep 1", 15.0)
    annot.add_annotation("Rat placed in enclosure, start run 1", 933.0)
    annot.add_annotation("Rat taken out of enclosure, end run 1", 1456.0)
    annot.add_annotation("Rat in bed, start sleep 2", 1461.0)
    annot.add_annotation("Rat placed in enclosure, start run 2", 2401.0)
    annot.add_annotation("Rat taken out of enclosure, end run 2", 3210.0)
    annot.add_annotation("Rat in bed, start sleep 3", 3218.0)
    annot.add_annotation("End sleep 3", 4193.0)
    #
    annot.finalize()
    neurodata.close()

test_append()
print "%s PASSED" % __file__

