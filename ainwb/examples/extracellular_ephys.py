#!/usr/bin/python
import sys
import nwb
import numpy as np
from nwb.nwbco import *

""" 
Store extracellular ephys data

"""

########################################################################
# create a new NWB file
# several settings are specified when doing so. these can be supplied within
#   the NWB constructor or defined in a dict, as in in this example
settings = {}
settings["filename"] = "sample_extracellular_ephys.nwb"

# each file should have a descriptive globally unique identifier 
#   that specifies the lab and this experiment session
# the function nwb.create_identifier() is recommended to use as it takes
#   the string and appends the present date and time
settings["identifier"] = nwb.create_identifier("extracellular ephys example")

# indicate that it's OK to overwrite exting file
settings["overwrite"] = True

# specify the start time of the experiment. all times in the NWB file
#   are relative to experiment start time
# if the start time is not specified the present time will be used
settings["start_time"] = "Sat Jul 04 2015 3:14:16"

# provide one or two sentences that describe the experiment and what
#   data is in the file
settings["description"] = "Test file demonstrating a simple extracellular ephys recording"

# create the NWB object. this manages the file
print "Creating " + settings["filename"]
neurodata = nwb.NWB(**settings)

########################################################################
# create two electrical series, one with a single electrode and one with many
# then create a spike event series

# first create the electrode map
# example simulated recording is made from two 2-electrode probes named
#   'p0' and 'p1'. we need to define the locations of the electrodes
#   relative to each probe, and the location of the probes
# electrode coordinates are in meters and their positions 
#   are relative to each other. the location of the probe itself is
#   stored separately. using absolute coordinates here, if they are known, 
#   is still OK
electrode_map = [[0, 0, 0], [0, 1.5e-6, 0], [0, 0, 0], [0, 3.0e-5, 0]]
electrode_group = [ "p0", "p0", "p1", "p1" ]
neurodata.set_metadata(EXTRA_ELECTRODE_MAP, electrode_map)
neurodata.set_metadata(EXTRA_ELECTRODE_GROUP, electrode_group)
# set electrode impedances
neurodata.set_metadata(EXTRA_IMPEDANCE, [ 1e6, 1.1e6, 1.2e6, 1.3e6 ])

# define the placement of each probe
neurodata.set_metadata(EXTRA_SHANK_LOCATION("p0"), "CA1, left hemisphere, stereotactic coordinates xx, yy")
neurodata.set_metadata(EXTRA_SHANK_LOCATION("p1"), "CA3, left hemisphere, stereotactic coordinates xx, yy")

# define timestamp data (eg, 1 second at 10KHz)
timestamps = np.arange(10000) * 0.0001
# define data (here is all zeros -- real data will of course be different)
data = np.zeros(10000)

# the example is of two 2-electrode probes. the electrode data from these
#   probes can be stored individually, grouped as probes (eg, 2-electrode
#   pair) or all stored together. these approaches are all exampled here 

# create time series with single electrode
single = neurodata.create_timeseries("ElectricalSeries", "mono", "acquisition")
single.set_comment("Data corresponds to recording from a single electrode")
single.set_data(data)
single.set_time(timestamps)
# indicate that we're recording from the first electrode defined in the
#   above map (electrode numbers start at zero, so electrodes are 
#   0, 1, 2 and 3
single.set_value("electrode_idx", 0)
# finish the time series and write data to disk
single.finalize()

########################################################################
# here is a time series storing data from a single probe (ie, 2 electrodes)
double = neurodata.create_timeseries("ElectricalSeries", "duo", "acquisition")
double.set_comment("Data corresponds to two electrodes (one probe)")
double.set_data(np.zeros((10000, 2)))
# timestamps were already stored in the 'single' time series. we can link
#   to that instance, which saves space
double.set_time_as_link(single)
# when setting time as a link, we need to set the value num_samples
double.set_value("num_samples", len(timestamps))
# define the electrode mapping -- this is 'p0' which take slots 0 and 1
#   in the global electrode map
double.set_value("electrode_idx", [0, 1])
# finish the time series and write data to disk
double.finalize()

########################################################################
# here is a time series storing data from both probes together
quad = neurodata.create_timeseries("ElectricalSeries", "quad", "acquisition")
quad.set_comment("Data corresponds to four electrodes (two probes)")
quad.set_data(np.zeros((10000, 4)))
quad.set_time_as_link(single)
quad.set_value("num_samples", len(timestamps))
quad.set_value("electrode_idx", [0, 1, 2, 3])
quad.finalize()


# close file, otherwise it will fail to write properly
neurodata.close()

