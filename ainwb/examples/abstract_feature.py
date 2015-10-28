#!/usr/bin/python
import sys
import numpy as np
import nwb

""" 
Store the Salient Features of a Drifting Gratings Visual Stimulus

This example demonstrates how to use an AbstractFeatureSeries to store
data that can be summarized by certain high-level features, such as the 
salient features of a visual stimulus. The standard example of this is 
for drifting gratings -- the spatial frequency, orientation, phase, 
contrast and temporal frequency are the most important characteristics 
for analysis using drifting gratings, not necessarily the stack of all 
frames displayed by the graphics card.
"""

########################################################################
# create a new NWB file
# several settings are specified when doing so. these can be supplied within
#   the NWB constructor or defined in a dict, as in in this example
settings = {}
settings["filename"] = "sample_abstract_features.nwb"

# each file should have a descriptive globally unique identifier 
#   that specifies the lab and this experiment session
# the function nwb.create_identifier() is recommended to use as it takes
#   the string and appends the present date and time
settings["identifier"] = nwb.create_identifier("abstract-feature example")

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
# create an AbstractFeatureSeries
# this will be stored as a 'stimulus' in this example for this example. that
#   means that it will be stored in the following location in the hdf5
#   file: stimulus/presentation/
abstract = neurodata.create_timeseries("AbstractFeatureSeries", "my_drifting_grating_features", "stimulus")
abstract.set_description("This is a simulated visual stimulus that presents a moving grating")

# an AbstractFeatureSeries is an instance of a TimeSeries, with addition
#   of the following fields:
#       features -- describes the abstract features
#       feature_units -- the units that these features are measured in
# define the abstract features that we're storing, as well as the units
#   of those features (any number of features can be specified)
features = [ "orientation", "spatial frequency", "phase", "temporal frequency"]
units = [ "degrees", "Hz", "radians", "degrees"]
# store them
abstract.set_features(features, units)

abstract.set_source("Simulated data. Normally this would be the device presenting stimulus")

# create some pretend data
data = np.arange(4000).reshape(1000, 4)

# add data to the time series. for now, ignore the last 3 parameters
abstract.set_data(data)
t = np.arange(1000) * 0.001
abstract.set_time(t)

# the time series must be finalized to be complete. this writes changes
#   to disk and allows freeing some memory resources
abstract.finalize()

########################################################################
# it can sometimes be useful to import documenting data from a file
# in this case, we'll store this script in the metadata section of the
#   file, for a record of how the file was created
neurodata.set_metadata_from_file("source_script", sys.argv[0])

# when all data is entered, close the file
neurodata.close()

