#!/usr/bin/python
import sys
import nwb
import test_utils as ut

# test creation of annotation time series
# TESTS AnnotationSeries creation
# TESTS TimeSeries ancestry


def test_annotation_series():
    if __file__.startswith("./"):
        fname = "x" + __file__[3:-3] + ".nwb"
    else:
        fname = "x" + __file__[1:-3] + ".nwb"
    name = "annot"
    create_annotation_series(fname, name, "acquisition")
    ut.verify_timeseries(fname, name, "acquisition/timeseries", "TimeSeries")
    ut.verify_timeseries(fname, name, "acquisition/timeseries", "AnnotationSeries")
    create_annotation_series(fname, name, "stimulus")
    ut.verify_timeseries(fname, name, "stimulus/presentation", "TimeSeries")
    ut.verify_timeseries(fname, name, "stimulus/presentation", "AnnotationSeries")

def create_annotation_series(fname, name, target):
    settings = {}
    settings["filename"] = fname
    settings["identifier"] = nwb.create_identifier("annotation example")
    settings["overwrite"] = True
    settings["start_time"] = "Sat Jul 04 2015 3:14:16"
    settings["description"] = "Test file with AnnotationSeries"
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

test_annotation_series()
print("%s PASSED" % __file__)

