#!/usr/bin/python
import sys
import nwb
import test_utils as ut

# create two epochs, add different subset of tags to each
# verify main epoch folder has tag attribute that contains
#   exactly the unique tags of each epoch and that each
#   epoch contains the assigned tags
    
fname = "x" + __file__[3:-3] + ".nwb"
borg = ut.create_new_file(fname, "Epoch tags")

tags = ["tag-a", "tag-b", "tag-c"]

epoch1 = borg.create_epoch("epoch-1", 0, 3);
for i in range(len(tags)-1):
    epoch1.add_tag(tags[i+1])

epoch2 = borg.create_epoch("epoch-2", 1, 4);
for i in range(len(tags)-1):
    epoch2.add_tag(tags[i])

borg.close()

tags = ut.verify_attribute_present(fname, "epochs/epoch-1", "tags");
for i in range(len(tags)-1):
    if tags[i+1] not in tags:
        ut.error("Verifying epoch tag content", "All tags not present")

tags = ut.verify_attribute_present(fname, "epochs/epoch-2", "tags");
for i in range(len(tags)-1):
    if tags[i] not in tags:
        ut.error("Verifying epoch tag content", "All tags not present")

tags = ut.verify_attribute_present(fname, "epochs", "tags");
for i in range(len(tags)):
    if tags[i] not in tags:
        ut.error("Verifying epoch tag content", "All tags not present")


print("%s PASSED" % __file__)

