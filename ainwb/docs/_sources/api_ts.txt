==============
**TimeSeries**
==============

The specification defines many different time series. All store data 
and the timestamps for each data sample. Many are more specialized
and have additional fields appropriate for their intended use.

Here is a listing of the different defined time series and the 
fields in each. The user is free to define any additional fields --
the list here provides the minimum of what is expected.

The organization of TimeSeries is hierarchical and object-oriented.
All time series extend the TimeSeries object, meaning that each of
them have all of the elements defined for a TimeSeries as well as
elements that are specific to the new object. Each time series is
defined both with the time series object that it extends as well as
the new fields that it defines for itself.

*Note: The definitions below are abbreviated. A more thorough description is
available in the file format specification documentation*


**TimeSeries**

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
|                     | (see below for details)          | Description                                           |
+=====================+==================================+=======================================================+
| data                | set_data()                **or** | Sets the data to be stored in the time series         |
|                     |                                  |                                                       |
|                     | set_data_as_link()        **or** |                                                       |
|                     |                                  |                                                       |
|                     | set_data_as_remote_link()        |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| timestamps          | set_time()                **or** | The timestamps associated with the samples stored in  |
| *(double array)*    |                                  | data                                                  |
|                     | set_time_as_link()        **or** |                                                       |
|                     |                                  |                                                       |
|                     | set_time_by_rate()               |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| num_samples         | set_value("num_samples", ...)    | The number of samples. This is automatically set      |
| *(int)*             |                                  | except in edge cases -- the API will alert you if     |
|                     |                                  | such a case arises                                    | 
+---------------------+----------------------------------+-------------------------------------------------------+
| control             | set_value("control", ...)        | This is an optional field that stores a control or    |
| *(byte array)*      |                                  | state value for each data sample                      |
+---------------------+----------------------------------+-------------------------------------------------------+
| control_description | set_value("control_description", | This describes the different control states, if any   |
| *(text array)*      | ...)                             | are specified                                         |
+---------------------+----------------------------------+-------------------------------------------------------+


**AbstractFeatureSeries** extends **TimeSeries**

Abstract features, such as quantitative descriptions of sensory stimuli. The TimeSeries::data field is a 2D array, storing those features (e.g., for visual grating stimulus this might be orientation, spatial frequency and contrast). Array structure: [num frames] [num features]. Null stimuli (eg, uniform gray) can be marked as being an independent feature (eg, 1.0 for gray, 0.0 for actual stimulus) or by storing NaNs for feature values, or through use of the TimeSeries::control fields. A set of features is considered to persist until the next set of features is defined. The final set of features stored should be the null set.


+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| feature             | set_features()              *or* | Declare the abstract features                         |
| *(text array)*      |                                  |                                                       |
|                     | set_value("feature", ...)        |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| feature_units       | set_features()              *or* | The units for the abstract features                   |
| *(text array)*      |                                  |                                                       |
|                     | set_value("feature_units", ...)  |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+

**AnnotationSeries** extends **TimeSeries**

Stores, eg, user annotations made during an experiment. The TimeSeries::data[] field stores a text array, and timestamps are stored for each annotation (ie, interval=1). This is largely an alias to a standard TimeSeries storing a text array but that is identifiable as storing annotations in a machine-readable way.

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| data, timestamps    | add_annotation()                 | Convenience function that should be used instead of   |
|                     |                                  | set_data() and set_time                               |
+---------------------+----------------------------------+-------------------------------------------------------+


**IndexSeries** extends **TimeSeries**

Stores indices to image frames stored in an ImageSeries. The purpose of the ImageIndexSeries is to allow a static image stack to be stored somewhere, and the images in the stack to be referenced out-of-order. This can be for the display of individual images, or of movie segments (as a movie is simply a series of images). The data field stores the index of the frame in the referenced ImageSeries, and the timestamps array indicates when that image was displayed. The ImageIndexSeries containes all datasets of TimeSeries plus the following:

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| indexed_timeseries  | set_value("indexed_timeseries",  | HDF5 link to *TimeSeries* containing images that are  |
| *(TimeSeries obj    | ...)                             | indexed                                               |
| or text path)*      |                                  |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+

**IntervalSeries** extends **TimeSeries**

Stores intervals of data. The timestamps field stores the beginning and end of intervals. The data field stores whether the interval just started (>0 value) or ended (<0 value). Different interval types can be represented in the same series by using multiple key values (eg, 1 for feature A, 2 for feature B, 3 for feature C, etc). The field data stores an 8-bit integer. This is largely an alias of a standard TimeSeries but that is identifiable as representing time intervals in a machine-readable way.

**OptogeneticSeries** extends **TimeSeries**

Optogenetic stimulus. The data[] field represents laser power and is in units of watts. 

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| site *(text)*       | set_value("site", ...)           | Name of site description in general/optogentics       |
+---------------------+----------------------------------+-------------------------------------------------------+


**RoiResponseSeries** extends **TimeSeries**
ROI responses over an imaging plane. Each row in data[] should correspond to the signal from one ROI.

+------------------------+-------------------------------------+-------------------------------------------------+
| Name                   | API call to set                     | Description                                     |
+========================+=====================================+=================================================+
| segmentation_interface | set_value("segmentation_interface", | HDF5 link to image segmentation module defining |
| *(Interface obj        | ...)                                | regions of interest (ROIs)                      |
| or text path)*         |                                     |                                                 |
+------------------------+-------------------------------------+-------------------------------------------------+
| roi_names              | set_value("roi_names", ...)         | List of ROIs represented, one name for each row |
| *(text array)*         |                                     | of *data[]*                                     |
+------------------------+-------------------------------------+-------------------------------------------------+


**SpatialSeries** extends **TimeSeries**

Direction, e.g., of gaze or travel, or position. The TimeSeries::data field is a 2D array storing position or direction relative to some reference frame. Array structure: [num measurements] [num dimensions]. Each SpatialSeries has a text dataset reference_frame that indicates the zero-position, or the zero-axes for direction. For example, if representing gaze direction, “straight-ahead” might be a specific pixel on the monitor, or some other point in space. For position data, the 0,0 point might be the top-left corner of an enclosure, as viewed from the tracking camera. The units of data will indicate how to interpret SpatialSeries values. A SpatialSeries has all the datasets of a TimeSeries plus the following:

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| reference_frame     | set_value("reference_frame",     | Description defining what “straight-ahead” means      |
| *(text)*            | ...)                             |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+


**ElectricalSeries** extends **TimeSeries**

Stores acquired voltage data from extracellular recordings. The data field of an ElectricalSeries is an int or float array storing data in Volts. Array structure: [num time samples] [num channels]. It contains all of the datasets of the basic TimeSeries as well as the following:

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| electrode_idx       | set_value("electrode_idx",       | Indices to electrodes described in the experiment's   |
| *(int array)*       | ...)                             | electrode map array in /general/extracellular_ephys   |
+---------------------+----------------------------------+-------------------------------------------------------+


**SpikeEventSeries** extends **ElectricalSeries**

Stores “snapshots” of spike events (i.e., threshold crossings) in data. This may also be raw data, as reported by ephys hardware. If so, the TimeSeries::description field should describing how events were detected. All SpikeEventSeries should reside in a module (under EventWaveform interface) even if the spikes were reported and stored by hardware. All events span the same recording channels and store snapshots of equal duration. TimeSeries::data array structure: [num events] [num channels] [num samples] (or [num events][num samples] for single electrode). 


**PatchClampSeries** extends **TimeSeries**

Stores stimulus or response current or voltage. These are regular TimeSeries except for the addition of the following field:
	electrode_name (text)		Name of electrode entry in /general/intracellular_ephys

**VoltageClampStimulusSeries** extends **PatchClampSeries**

**CurrentClampStimulusSeries** extends **PatchClampSeries**

These are aliases to standard PatchClampSeries. Their functionality is to better tag PatchClampSeries for machine (and human) readability of the file.

**VoltageClampSeries** extends **PatchClampSeries**

Stores current data recorded from intracellular voltage-clamp recordings. A corresponding VoltageClampStimulusSeries (stored separately as a stimulus) is used to store the voltage injected. The VoltageClampSeries has all of the datasets of an PatchClampSeries as well as the following:

+------------------------------+-----------------------------------------+---------------------------------------+
| Name                         | API call to set                         | Description                           |
+==============================+=========================================+=======================================+
| capacitance_fast *(float)*   | set_value("capacitance_fast", ...)      | Unit: Farads                          |
+------------------------------+-----------------------------------------+---------------------------------------+
| capacitance_slow *(float)*   | set_value("capacitance_slow", ...)      | Unit: Farads                          |
+------------------------------+-----------------------------------------+---------------------------------------+
| resistance_comp_bandwidth    | set_value("resistance_comp_bandwidth",  | Unit: Hz                              |
| *(float)*                    | ...)                                    |                                       |
+------------------------------+-----------------------------------------+---------------------------------------+
| resistance_comp_correction   | set_value("resistance_comp_correction", | Unit: %                               |
| *(float)*                    | ...)                                    |                                       |
+------------------------------+-----------------------------------------+---------------------------------------+
| resistance_comp_prediction   | set_value("resistance_comp_prediction", | Unit: %                               |
| *(float)*                    | ...)                                    |                                       |
+------------------------------+-----------------------------------------+---------------------------------------+
| whole_cell_capacitance_comp  | set_value("whole_cell_capacitance_comp  | Unit: Farads                          |
| *(float)*                    | ", ...)                                 |                                       |
+------------------------------+-----------------------------------------+---------------------------------------+
| whole_cell_series_resistance | set_value("whole_cell_series_resistance | Unit: Ohms                            |
| _comp *(float)*              | _comp", ...)                            |                                       |
+------------------------------+-----------------------------------------+---------------------------------------+
| gain *(float)*               | set_value("gain", ...)                  | Unit: Volt/Amp                        |
+------------------------------+-----------------------------------------+---------------------------------------+


**CurrentClampSeries** extends **PatchClampSeries**

Stores voltage data recorded from intracellular current-clamp recordings. A corresponding CurrentClampStimulusSeries (stored separately as a stimulus) is used to store the current injected.  The CurrentClampSeries has all of the datasets of an PatchClampSeries as well as the following:

+--------------------------+---------------------------------------+---------------------------------------------+
| Name                     | API call to set                       | Description                                 |
+==========================+=======================================+=============================================+
| bias_current             | set_value("bias_current", ...)        | Unit: Amps                                  |
| *(float)*                |                                       |                                             |
+--------------------------+---------------------------------------+---------------------------------------------+
| bridge_balance           | set_value("bridge_balance",           | Unit: Ohms                                  |
| *(float)*                | ...)                                  |                                             |
+--------------------------+---------------------------------------+---------------------------------------------+
| capacitance_compensation | set_value("capacitance_compensation", | Unit: Farads                                |
| *(float)*                | ...)                                  |                                             |
+--------------------------+---------------------------------------+---------------------------------------------+
| resistance_compensation  | set_value("resistance_compensation",  | Unit: Ohms                                  |
| *(float)*                | ...)                                  |                                             |
+--------------------------+---------------------------------------+---------------------------------------------+
| gain *(float)*           | set_value("gain", ...)                | Unit: Volt/Volt                             |
+--------------------------+---------------------------------------+---------------------------------------------+


**ImageSeries** extends **TimeSeries**

General image data that is common between acquisition and stimulus time series. Sometimes the image data is stored in the HDF5 file in a raw format while other times it will be stored as an external image file in the host file system. The data field will either be binary data or empty. TimeSeries::data array structure: [frame][y][x] (or [frame][z][y][x]). The ImageSeries contains all of the datasets of the TimeSeries as well as the following:

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| format *(text)*     | set_value("format", ...)         | Format of image. If this is “external” then the field |
|                     |                                  | external_file contains the path or URL information to |
|                     |                                  | that file. For tiff, png, jpg, etc, the binary        |
|                     |                                  | representation of the image is stored in *data*. If   |
|                     |                                  | the format is “raw” then the fields bit_per_pixel and |
|                     |                                  | dimension are used.  For raw images, only a single    |
|                     |                                  | channel is stored (eg, red)                           |
+---------------------+----------------------------------+-------------------------------------------------------+
| external_file       | set_value("external_file", ...)  | Path or URL to external file, if format = “external”  |
| *(text)*            |                                  |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| bits_per_pixel      | set_value("bits_per_pixel",      | Number of bits per image pixel                        |
| *(int)*             | ...)                             |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| dimension           | set_value("dimension", ...)      | Number of pixels on x, y and z axes                   |
| *(int array)*       |                                  |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+


**ImageMaskSeries** extends **ImageSeries**

An alpha mask that is applied to a presented visual stimulus. The data[] array contains an array of mask values that are applied to the displayed image. Mask values are stored as RGBA. Mask can vary with time.  The timestamps array indicates the starting time of a mask, and that mask pattern continues until it's explicitly changed.

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| masked_imageseries  | set_value("masked_imageseries",  | HDF5 link to *ImageSeriesSeries* that mask is applied |
| *(ImageSeries obj   | ...)                             | to                                                    |
| or text path)*      |                                  |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+


**TwoPhotonSeries** extends **ImageSeries**

A special case of optical imaging. The TwoPhotonSeries has all the datasets of the ImageSeries as well as the following:

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| pmt_gain *(float)*  | set_value("pmt_gain", ...)       | photomultiplier gain                                  |
+---------------------+----------------------------------+-------------------------------------------------------+
| field_of_view       | set_value("field_of_view", ...)  | Width, height and depth of image, or imaged area      |
| *(float array)*     |                                  | (meters)                                              |
+---------------------+----------------------------------+-------------------------------------------------------+
| imaging_plane       | set_value("imaging_plane",       | Name of imaging plane description in                  |
| *(text)*            | ...)                             | /general/optophysiology                               |
+---------------------+----------------------------------+-------------------------------------------------------+
| scan_line_rate      | set_value("scan_line_rate", ...) | Lines imaged per second. This is device information   |
| *(float)*           |                                  | that is stored w/ the data for analysis convenience   |
+---------------------+----------------------------------+-------------------------------------------------------+


**OpticalSeries** extends **ImageSeries**

Image data that is presented or recorded. A stimulus template movie will be stored only as an image. When the image is presented as stimulus, additional data is required, such as field of view (eg, how much of the visual field the image covers, or how what is the area of the target being imaged). If the OpticalSeries represents acquired imaging data, orientation is also important. The OpticalSeries has all datasets of the ImageSeries as well as the following

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| orientation         | set_value("orientation",         | Description of image relative to some reference frame |
| *(float)*           | ...)                             | (e.g., which way is 'up'). Must also specify frame of |
|                     |                                  | reference                                             |
+---------------------+----------------------------------+-------------------------------------------------------+
| distance *(float)*  | set_value("distance", ...)       | Distance of camera/monitor from target/eye            |
+---------------------+----------------------------------+-------------------------------------------------------+
| field_of_view       | set_value("field_of_view", ...)  | Width, height and depth of image, or imaged area      |
| *(float array)*     |                                  | (meters)                                              |
+---------------------+----------------------------------+-------------------------------------------------------+


**WidefieldSeries** extends **OpticalSeries**

Imagestack recorded from wide-field imaging

+---------------------+----------------------------------+-------------------------------------------------------+
| Name                | API call to set                  | Description                                           |
+=====================+==================================+=======================================================+
| indicator *(text)*  | set_value("indicator", ...)      |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| illumination_power  | set_value("illumination_power",  | Unit: Watts                                           |
| *(float)*           | ...)                             |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| exposure_time       | set_value("exposure_time",       | Unit: Seconds                                         |
| *(float)*           | ...)                             |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| pixel_binning       | set_value("pixel_binning", ...)  | Array structure [x, y, t]                             |
| *(float array)*     |                                  |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+
| counts_per_bit      | set_value("counts_per_bit",      |                                                       |
| *(float)*           | ...)                             |                                                       |
+---------------------+----------------------------------+-------------------------------------------------------+




**root TimeSeries object**
---------------------------

.. autoclass:: nwbts.TimeSeries
   :members:

The below time series instances have additional fields, sometimes for
conveninece and sometimes to add additional safety checks

**AnnotationSeries**
--------------------

.. autoclass:: nwbts.AnnotationSeries
   :members:

**AbstractFeatureSeries**
-------------------------

.. autoclass:: nwbts.AbstractFeatureSeries
   :members:

