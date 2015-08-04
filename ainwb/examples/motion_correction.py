#!/usr/bin/python
import sys
import numpy as np
import nwb
# nwbco stores constants that are useful for setting experiment-level
#   metadata
from nwb.nwbco import *

""" 
An example of using the MotionCorrection interface

Modules and interfaces address intermediate processing of experimental
data. Intermediate processing is processing that's necessary to
convert the acquired data into a form that scientific analysis can
be performed on. In this example, that process is motion-correcting
an image. 

Processing and storing data in modules will typically be done
by people writing software that perform the processing tasks. The
software writer is free to store whatever additional data they wish
to store in a module. All that's required is the minimum data
required by each interface is included.

The MotionCorrection interface stores an unregistered image,
the xy translation necessary to motion-correct it, and the
corrected image. In this example, a time series storing 2-photon
image data is created, as if it were the original image coming
from a 2-photon microscope. Another time series is created that stores
the XY delta for each imaging frame necessary to correct for motion.
A third time series is created pointing to the corrected image.
"""

########################################################################
# create a new NWB file
# several settings are specified when doing so. these can be supplied within
#   the NWB constructor or defined in a dict, as in in this example
settings = {}
settings["filename"] = "sample_motion_correction.nwb"

# each file should have a descriptive globally unique identifier 
#   that specifies the lab and this experiment session
# the function nwb.create_identifier() is recommended to use as it takes
#   the string and appends the present date and time
settings["identifier"] = nwb.create_identifier("motion correction example")

# indicate that it's OK to overwrite exting file
settings["overwrite"] = True

# specify the start time of the experiment. all times in the NWB file
#   are relative to experiment start time
# if the start time is not specified the present time will be used
settings["start_time"] = "Sat Jul 04 2015 3:14:16"

# provide one or two sentences that describe the experiment and what
#   data is in the file
settings["description"] = "Test file demonstrating use of the MotionCorrection interface"

# create the NWB object. this manages the file
print "Creating " + settings["filename"]
neurodata = nwb.NWB(**settings)

########################################################################
# this is a sample optophysiology dataset storing simulated 2-photon
#   image stacks. these must refer to an imaging plane that's defined
#   in the general metadata section. define that metadata here
# the metadata fields (all caps) are defined in nwbco
# 
# define the recording device
neurodata.set_metadata(DEVICE("Acme 2-photon microscope"), "Information about device goes here")
# declare information about a particular site and/or imaging plane
neurodata.set_metadata(IMAGE_SITE_EXCITATION_LAMBDA("camera1"), "1000 nm") 
neurodata.set_metadata(IMAGE_SITE_INDICATOR("camera1"), "GCaMP6s") 
neurodata.set_metadata(IMAGE_SITE_DEVICE("camera1"), "Acme 2-photon microscope") 
########################################################################
# create different examples of image series
# image can be stored directly, for example by reading a .tif file into
#   memory and storing this data as a byte stream in data[]
# most(all?) examples here will have the time series reference data
#   that is stored externally in the file system

# first, a simple image. this could be a simple ImageSeries. in this
#   example we're using a TwoPhotonSeries, which is an ImageSeries
#   with some extra data fields
orig = neurodata.create_timeseries("TwoPhotonSeries", "source image", "acquisition")
orig.set_description("Pointer to a 640x480 image stored in the file system")
orig.set_source("Data acquired from Acme 2-photon microscope")
# assume the file is stored externally in the file system
orig.set_value("format", "external")
# specify the file
orig.set_value("external_file", "/path/to/file/stack.tif")
# information about the image
orig.set_value("bits_per_pixel", 16)
orig.set_value("dimension", [640, 480])
###########################
# TwoPhoton-specific fields
orig.set_value("pmt_gain", 1.0)
# field of view is in meters
orig.set_value("field_of_view", [0.0003, 0.0003])
# imaging plane value is the site/imaging-plane defined as metadata above
orig.set_value("imaging_plane", "cameria1")
orig.set_value("scan_line_rate", 16000)
###########################
# store time -- this example has 3 frames
orig.set_time([0, 1, 2])
# there's no data to store in the NWB file as the data is in an image
#   file in the file system
orig.ignore_data()
# when we ignore data, we must explicitly set number of samples (this is
#   otherwise handled automatically)
orig.set_value("num_samples", 3)
# this is simulated acquired data
# finish the time series so data is written to disk
orig.finalize()

# this example is for storing motion corrected 2-photon images
# store the pixel delta for each frame in the source stack
xy = neurodata.create_timeseries("TimeSeries", "x,y adjustments")
xy.set_description("X,Y adjustments to original image necessary for registration")
xy.set_data([[1.23, -3.45], [3.14, 2.18], [-4.2, 1.35]])
xy.set_time_as_link(orig)
# setting time as link also requires setting number of samples manually 
#   FIXME
# if you try to create a time series and a required field is absent, the
#   API will give an error about the missing field (try commenting out 
#   the line set_data(), set_time() or set_value("num_samples") to see this
#   behavior in action
xy.set_value("num_samples", 3)
# 'xy' is motion corrected data and is part of the processing module
# module time series are finalized by the module interface that they're
#   added to, so don't do it here

# the module interface also stores the corrected image. assume that
#   it's in the file system too
corr = neurodata.create_timeseries("ImageSeries", "corrected_image", "acquisition")
corr.set_description("Corrected image")
corr.set_comments("Motion correction calculated manually in photoshop")
corr.set_value("format", "external")
corr.set_value("external_file", "/path/to/file/corrected_stack.tif")
corr.set_value("bits_per_pixel", 16)
corr.set_value("dimension", [640, 480])
corr.set_time_as_link(orig)
corr.set_value("num_samples", 3)
corr.ignore_data()
corr.finalize()


# create the module and MotionCorrection interface
mod = neurodata.create_module("my module")
# the module can store as many interfaces as we like. in this case we 
#   only have one. create it
iface = mod.create_interface("MotionCorrection")
# add the time series to the interface
iface.add_corrected_image("2photon", orig, xy, corr)
# the time series can be added by providing the python object or 
#   by specifying the paths to these objects, whichever is more
#   convenient. the following calls are equivalent:
#iface.add_corrected_image("2photon", orig.full_path(), xy.full_path(), corr)
#iface.add_corrected_image("2photon", orig, xy, corr.full_path())
#   as would be specifying the paths to the time series manually 
#   (eg, as stored in a variable)

# provide information in the interface about the source of the data
iface.set_source(orig.full_path())

iface.set_value("random comment", "Note that the 'original' field under 2photon is an HDF5 link to the time series '/acquisition/timeseries/source image'")

# finish off the interface
iface.finalize()

# finish off the module
mod.finalize()

# when all data is entered, close the file
neurodata.close()

