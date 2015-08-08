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
settings["filename"] = "sample_extracellular_spikes.nwb"

# each file should have a descriptive globally unique identifier 
#   that specifies the lab and this experiment session
# the function nwb.create_identifier() is recommended to use as it takes
#   the string and appends the present date and time
settings["identifier"] = nwb.create_identifier("extracellular spikes example")

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

########################################################################
# the example is of two 2-electrode probes. the electrode data from these
#   probes can be stored individually, grouped as probes (eg, 2-electrode
#   pair) or all stored together. these approaches are all exampled here 

# create time series with all electrode data stored together
quad = neurodata.create_timeseries("ElectricalSeries", "quad", "acquisition")
quad.set_comment("Data corresponds to four electrodes (two probes)")
quad.set_data(np.zeros((10000, 4)), resolution=1.2345e-6)
quad.set_time(np.arange(10000) * 0.0001)
# indicate that we're recording from the first electrode defined in the
#   above map (electrode numbers start at zero, so electrodes are 
#   0, 1, 2 and 3
quad.set_value("electrode_idx", [0, 1, 2, 3])
# finish the time series and write data to disk
quad.finalize()

########################################################################
# spikes can be reported by hardware or be detected by software
# in both cases, they are considered to be processed data and so belong
#   in a processing module

# create the module
spike_mod = neurodata.create_module("my spikes")

# create an interface that stores the events. here they will be stored
#   with their waveforms, such as would be the input to a spike-sorting
#   algorithm
spike_iface = spike_mod.create_interface("EventWaveform")
spike_iface.set_source("Data from device FooBar-X1 using dynamic multi-phasic threshold of 5xRMS")

# the event waveform interface publishes a SpikeEventSeries. make 
#   that series
spike = neurodata.create_timeseries("SpikeEventSeries", "my waveforms")
spike.set_comment("Snapshots of spike events pulled from a recording")
spike.set_value("electrode_idx", [2, 3])    # probe 'p1'
# describe the source of the data (may be redundant w/ interface source)
spike.set_value("source", "Data from device FooBar-X1 using dynamic multi-phasic threshold of 5xRMS")
# make some bogus simulated data
# this is 20 events all having the same shape and a pseudorandom time
evt = np.zeros((8,2))
evt[3][0] = 0.01
evt[4][0] = -0.005
evt[3][1] = 0.005
evt[4][1] = -0.0025
data = []
t = []
last = 1.0
for i in range(20):
    data.append(evt)
    last = last + (i * 17) % 29
    t.append(last)
# 
spike.set_time(t)
spike.set_data(data, resolution=1.2345e-6)
# if data were stored in another unit such as microvolts, it would be
#   necessary to specify a converstion between that unit and Volts.
#   that would be done using the following:
#spike.set_data(data, conversion=1.0e-6)

# add the time series to the interface. the interface will manage 
#   finalizing the time series
spike_iface.add_timeseries(spike)

# now close the interface and its parent module
spike_iface.finalize()
spike_mod.finalize()

# close file, otherwise it will fail to write properly
neurodata.close()

