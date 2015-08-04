=========================
**Module and interfaces**
=========================

Modules are separate groups stored in the root 'processing/' group.
Modules are designed to store the results of intermediate data
processing that is required before scientific analysis can be performed
on experimental data (e.g., spike sorting or image segmentation).
Each module publishes one or more 'interfaces', which are units that
present a specific aspect of the data. For example, the *Clustering* 
interface provides the time of an event with its cluster number.
See the standard documentation for a description of each interface and
a list of what data each interface publishes.

Many interfaces share the same API, while some more complex interfaces
require additional functions and procedures. Each interface is 
described below, followed by the API.


**BehavioralEvents**

**BehavioralEpochs**

**BehavioralTimeSeries**

The objective of these interfaces is to provide generic hooks for software tools/scripts. This allows a tool/script to take the output one specific interface (e.g., UnitTimes) and plot that data relative to another modality data (e.g., behavioral events) without having to define all possible modalities in advance. Declaring one of these interfaces means that one or more TimeSeries of the specified type is published. These TimeSeries should reside in a folder having the same name as the interface. For example, if a BehavioralTimeSeries interface is declared, the module will have one or more TimeSeries defined in the module sub-folder “BehavioralTimeSeries”. BehavioralEpochs should use IntervalSeries. BehavioralEvents is used for irregular events. BehavioralTimeSeries is for continuous data.

**Clustering**

Clustered spike data, whether from automatic clustering tools (e.g., klustakwik) or as a result of manual sorting. A Clustering module publishes the following datasets:

+------------------------+---------------------------+-----------------------------------------------------------+
| Name                   | API call to set           | Description                                               |
+========================+===========================+===========================================================+
| times, number,         | set_clusters()            | Convenience function to set fields 'num', 'times' and     |
| peak_over_rms          | ...)                      | peak_over_rms (see API description below)                 |
+------------------------+---------------------------+-----------------------------------------------------------+
| description *(text)*   | set_value("description",  | Description of clusters or clustering (e.g., cluster 0    |
|                        | ...)                      | is electrical noise, clusters curated using Klusters,     |
|                        |                           | etc)                                                      |
+------------------------+---------------------------+-----------------------------------------------------------+


**ClusterWaveforms**

The mean waveform shape, including standard deviation, of the different clusters. Ideally, the waveform analysis should be performed on data that is only high-pass filtered. This is a separate module because it is expected to require updating. For example, IMEC probes may require different storage requirements to store/display mean waveforms, requiring a new interface or an extension of this one. A ClusterWaveform module publishes the following datasets:

+------------------------+--------------------------------+------------------------------------------------------+
| Name                   | API call to set                | Description                                          |
+========================+================================+======================================================+
| waveform_mean          | set_value("waveform_mean",     | The mean waveform for each cluster, using the same   |
| *(float array)*        | ...)                           | indices for each wave as cluster numbers in the      |
|                        |                                | associated Clustering module (i.e, cluster 3 is in   |
|                        |                                | array slot [3]). Waveforms corresponding to gaps in  |
|                        |                                | cluster sequence should be empty (e.g., zero-filled) |
+------------------------+--------------------------------+------------------------------------------------------+
| waveform_sd            | set_value("waveform_sd", ...)  | Times of events that features correspond to (can be  |
| *(float array)*        |                                | a link). Array structure: [# events]                 |
+------------------------+--------------------------------+------------------------------------------------------+
| waveform_filtering     | set_value("waveform_filtering" | Filtering applied to data before generating mean/sd  |
| *(text)*               | , ...)                         |                                                      |
+------------------------+--------------------------------+------------------------------------------------------+
| clustering_interface   | set_value_as_link(             | HDF5 link to Clustering interface that was the       |
| *(Clustering object    | "clustering_interface", ...)   | source of the clustered data                         |
| or text path)*         |                                |                                                      |
+------------------------+--------------------------------+------------------------------------------------------+


**CompassDirection**

With a CompassDirection interface, a module publish one or more SpatialSeries objects that store a floating point value for theta. The SpatialSeries::reference_frame field should indicate what direction corresponds to “0” and which is the direction of rotation (this should be “clockwise”). The si_unit for the SpatialSeries should be “radians”  or “degrees”.


**DfOverF**

dF/F information about a region of interest (ROI). Each DfOverF interface publishes one or more RoiResponseSeries. Storage hierarchy of dF/F should be the same as for segmentation (ie, same names for ROIs and for image planes). 


**EventDetection**

Detected spike events from voltage trace(s). 

+-------------------------+--------------------------------+-----------------------------------------------------+
| Name                    | API call to set                | Description                                         |
+=========================+================================+=====================================================+
| times                   | set_value("times", ...) **or** | Times of events that features correspond to (can be |
| *(double array)*        | set_value_as_link("times",...) | a link). Array structure: [# events]                |
+-------------------------+--------------------------------+-----------------------------------------------------+
| detection_method        | set_value("detection_method",  | Description of how events were detected, such as    |
| *(text)*                | ...)                           | voltage or dV/dT threshold, plus relevant values    |
+-------------------------+--------------------------------+-----------------------------------------------------+
| source_electricalseries | set_value_as_link("            | HDF5 link to TimeSeries that this data was          |
| *(TimeSeries object or  | source_electricalseries", ...) | calculated from. Metadata about electrodes and      |
| text path)*             |                                | their position can be read from that TimeSeries so  |
|                         |                                | necessary to store that information here            |
+-------------------------+--------------------------------+-----------------------------------------------------+

**EventWaveform**

Represents either the waveforms of detected events, as extracted from a raw data trace in /acquisition, or the event waveforms that were stored during experiment acquisition. Each EventWaveform interface publishes one or more SpikeEventSeries.


**EyeTracking**

Eye-tracking data. Each interface publishes one or more SpatialSeries that store direction of gaze.


**FeatureExtraction**
Features, such as PC1 and PC2, that are extracted from signals stored in a SpikeEvent TimeSeries or other source. 

+------------------------+--------------------------------+------------------------------------------------------+
| Name                   | API call to set                | Description                                          |
+========================+================================+======================================================+
| features               | set_value("features", ...)     | Array of features extracted for each event           |
| *(float array)*        |                                | Array structure: [# events][# channels] [# features] |
+------------------------+--------------------------------+------------------------------------------------------+
| times                  | set_value("times", ...) **or** | Times of events that features correspond to (can be  |
| *(double array)*       | set_value_as_link("times",...) | a link). Array structure: [# events]                 |
+------------------------+--------------------------------+------------------------------------------------------+
| description            | set_value("description", ...)  | Description of features (eg, “PC1”) for each of the  |
| *(text array)*         |                                | extracted features. Array structure: [# features]    |
+------------------------+--------------------------------+------------------------------------------------------+
| electrode_idx          | set_value("electrode_idx",     | Indices to electrodes described in the experiment's  |
| *(int array)*          | ...)                           | electrode map array in general/extracellular_ephys.  |
|                        |                                | Array structure: [# channels]                        |
+------------------------+--------------------------------+------------------------------------------------------+


**FilteredEphys**

Ephys data from one or more channels that has been subjected to filtering. Examples of filtered data include Theta and Gamma (LFP has its own interface). FilteredEphys modules publish an ElectricalSeries for each filtered channel or set of channels. The name of each ElectricalSeries is arbitrary but should be informative. The source of the filtered data, whether this is from analysis of another time series or as acquired by hardware, should be noted in each's TimeSeries::description field. There is no assumed 1::1 correspondence between filtered ephys signals and electrodes, as a single signal can apply to many nearby electrodes, and one electrode may have different filtered (e.g., theta and/or gamma) signals represented. Each interface hase one or more ElectricalSeries.

**Fluorescence**

Fluorescence information about a region of interest (ROI). Each Fluorescence interface has one or more RoiResponseSeries. Storage hierarchy of fluorescence should be the same as for segmentation (ie, same names for ROIs and for image planes). 


**ImageSegmentation**

Stores pixels in an image that represent different regions of interest (ROIs). Pixels are stored in both lists and 2D maps representing image intensity. All segmentation data is stored in a “segmentation” subfolder. Each ROI is stored in its own subfolder within ImageSegmentation, with the ROI folder containing both a 2D mask and a list of pixels that make up this mask. Also for masking neuropil. If segmentation is allowed to change with time, a new interface is required (e.g., use the former version of this one, with img_mask_0 and start_time_0).


+------------------------+-------------------------------+-------------------------------------------------------+
| Name                   | API call to set               | Description                                           |
+========================+===============================+=======================================================+
| img_mask, pix_mask,    | add_roi_mask_img() **or**     | Creates the definition of a region of interest        |
| roi_description        | add_roi_mask_pixels()         |                                                       |
+------------------------+-------------------------------+-------------------------------------------------------+
| reference_image        | add_reference_image() **or**  | Adds a reference image that ROIs are based on         |
|                        | add_reference_image_as_link() |                                                       |
+------------------------+-------------------------------+-------------------------------------------------------+
| imaging_plane          | create_imaging_plane()        | Creates space to store data from one imaging plane    |
+------------------------+-------------------------------+-------------------------------------------------------+


**LFP**

LFP data from one or more channels. Each LFP interface has one or more ElectricalSeries. The electrode map in each published ElectricalSeries will identify which channels are providing LFP data. Filter properties should be noted in the ElectricalSeries description or comments field. 


**MotionCorrection**

Publishes an image stack where all frames are shifted (registered) to a common coordinate system, to account for movement and drift between frames.

+------------------------+-------------------------------+-------------------------------------------------------+
| Name                   | API call to set               | Description                                           |
+========================+===============================+=======================================================+
| original, corrected    | add_corrected_image()         | Adds a motion-corrected image to the interface        |
| images; xy_translation |                               |                                                       |
+------------------------+-------------------------------+-------------------------------------------------------+


**Position**

Position data, whether along the x, x/y or x/y/z axis. Each interface stores one or more SpatialSeries storing position.


**PupilTracking**

Eye-tracking data. Each PupilTracking interface has one or more TimeSeries storing pupil size.


**UnitTimes**

Event times in observed units (eg, cell, synapse, etc). The UnitTimes folder contains a folder for each unit. Name of the folder should match value in source module, if that is possible/relevant (e.g., name of ROIs from Segmentation module).

+------------------------+-------------------------------+-------------------------------------------------------+
| Name                   | API call to set               | Description                                           |
+========================+===============================+=======================================================+
| times, description     | add_unit()                    | Defines a unit, including event times and description |
| and source             |                               |                                                       |
+------------------------+-------------------------------+-------------------------------------------------------+


**Module**
----------

.. autoclass:: nwbmo.Module
   :members:

**root Interface class**
------------------------

.. autoclass:: nwbmo.Interface
   :members:

**Clustering interface**
------------------------
.. autoclass:: nwbmo.Clustering
   :members:

**ImageSegmentation interface**
-------------------------------
.. autoclass:: nwbmo.ImageSegmentation
   :members:

**MotionCorrection interface**
------------------------------
.. autoclass:: nwbmo.MotionCorrection
   :members:

**UnitTimes interface**
-----------------------
.. autoclass:: nwbmo.UnitTimes
   :members:


