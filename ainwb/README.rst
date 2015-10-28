Project description below

Install
=======

Instructions are provided to install the NWB library to the standard
system package repository. Installation to non-standard locations
will be different.

python 2
   system requirements:
      numpy, h5py

   as root, run:
     python setup.py install

python 3
   system requirements:
      numpy, h5py, cython

   as root, run:
     python3 setup.py install



Project description
===================


Neurodata Without Borders: Neurophysiology is a project to develop a
unified data format for cellular-based neurophysiology data, focused on
the dynamics of groups of neurons measured under a large range of
experimental conditions. Participating labs provided use cases and
critical feedback to the effort. The design goals for the NWB format
included:

**Compatibility**
Cross-platform
Support for tool makers

**Usability**
Quickly develop a basic understanding of an experiment and its data
Review an experiment’s details without programming knowledge

**Flexibility**
Accommodate an experiment’s raw and processed data
Encapsulate all of an experiment’s data, or link to external data source
when necessary

**Extensibility**
Accommodate future experimental paradigms without sacrificing backwards
compatibility.  Support custom extensions when the standard is lacking

**Longevity**
Data published in the format should be accessible for decades

Hierarchical Data Format (HDF) was selected for the NWB format because
it met several of the project’s requirements. First, it is a mature data
format standard with libraries available in multiple programming
languages. Second, the format’s hierarchical structure allows data to be
grouped into logical self-documenting sections. Its structure is
analogous to a file system in which its “groups” and “datasets”
correspond to directories and files. Groups and datasets can have
attributes that provide additional details, such as authorities’
identifiers. Third, its linking feature enables data stored in one
location to be transparently accessed from multiple locations in the
hierarchy. The linked data can be external to the file. Fourth, HDFView,
a free, cross-platform application, can be used to open a file and
browse data. Finally, ensuring the ongoing accessibility of HDF-stored
data is the mission of The HDF Group, the nonprofit that is the steward
of the technology.

The NWB format standard is codified in a schema file written in a
specification language created for this project. The specification
language describes the schema, including data types and associations. A
new schema file will be published for each revision of the NWB format
standard. Tool developers are expected to take advantage of this
explicit description of the format. However, data publishers are not
expected to do so. They can add custom datasets to existing TimeSeries,
Epochs, Modules and Interfaces. 


