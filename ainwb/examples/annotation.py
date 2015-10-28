#!/usr/bin/python
import sys
import nwb

"""
Create and store experiment annotations

Annotations are text strings that mark specific times in an 
experiment, for example "rat placed in enclosure" or "observed
start of seizure activity".
"""

########################################################################
# create a new NWB file
# several settings are specified when doing so. these can be supplied within
#   the NWB constructor or defined in a dict, as in in this example
settings = {}
settings["filename"] = "sample_annotations.nwb"

# each file should have a descriptive globally unique identifier 
#   that specifies the lab and this experiment session
# the function nwb.create_identifier() is recommended to use as it takes
#   the string and appends the present date and time
settings["identifier"] = nwb.create_identifier("annotation example")

# indicate that it's OK to overwrite exting file
settings["overwrite"] = True

# specify the start time of the experiment. all times in the NWB file
#   are relative to experiment start time
# if the start time is not specified the present time will be used

settings["start_time"] = "Sat Jul 04 2015 3:14:16"
# provide one or two sentences that describe the experiment and what
#   data is in the file

settings["description"] = "Test file demonstrating use of the AbstractFeatureSeries"

# create the NWB object. this manages the file
print("Creating " + settings["filename"])
neurodata = nwb.NWB(**settings)

########################################################################
# create an AnnotationSeries
# this will be stored in 'acquisiiton' as annotations are an
#   observation or a record of something else that happened.
# this means that it will be stored in the following location in the hdf5
#   file: acquisition/timeseries
annot = neurodata.create_timeseries("AnnotationSeries", "notes", "acquisition")
annot.set_description("This is an AnnotationSeries with sample data")
annot.set_comment("The comment and description fields can store arbitrary human-readable data")
annot.set_source("Observation of Dr. J Doe")

# store pretend data
# all time is stored as seconds
annot.add_annotation("Rat in bed, beginning sleep 1", 15.0)
annot.add_annotation("Rat placed in enclosure, start run 1", 933.0)
annot.add_annotation("Rat taken out of enclosure, end run 1", 1456.0)
annot.add_annotation("Rat in bed, start sleep 2", 1461.0)
annot.add_annotation("Rat placed in enclosure, start run 2", 2401.0)
annot.add_annotation("Rat taken out of enclosure, end run 2", 3210.0)
annot.add_annotation("Rat in bed, start sleep 3", 3218.0)
annot.add_annotation("End sleep 3", 4193.0)

# the time series must be finalized to be complete. this writes changes
#   to disk and allows freeing some memory resources
annot.finalize()

########################################################################
# it can sometimes be useful to import documenting data from a file
# in this case, we'll store this script in the metadata section of the
#   file, for a record of how the file was created
neurodata.set_metadata_from_file("source_script", __file__)

# when all data is entered, close the file
neurodata.close()

