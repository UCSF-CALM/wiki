---
layout: default
title: Python Scripts for TruLive
author: Herrington, Kari
---

Kari\'s notes on Scripts from Jan Frankowski **( Notes are IN
PROGRESS)**

Packages recommended to install

[spyder\
tifffile\
h5py\
opencv-python\
auto-py-to-exe]{style="color: inherit;" olk-copy-source="MessageBody"}

[[tkinter]\
[natsort]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[[Note:]]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[[Auto-py-to-exe can be used to compile into a .exe to run without any
dependencies]]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[[had trouble installing tkinter but it is only used in the old
version]]]{style="color: inherit;"
olk-copy-source="MessageBody"}

## [[Scripts from Jan:]]{style="color: inherit;" olk-copy-source="MessageBody"}

### [[OLD - Max intensity_easygui]]{style="color: inherit;" olk-copy-source="MessageBody"}

[[To create a series of MIPS for a
timelapse. ]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[Note does one color and position at a
time.]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[General idea is it is easy and
s]]{style="color: inherit;"
olk-copy-source="MessageBody"}[[cript opens up a series of windows for
prompting:]]{style="color: inherit;"
olk-copy-source="MessageBody"}

- [[Navigate to Raw
  data]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
- [[Output]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
- [[Choose long or short
  camera]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
  - [[There may be a bug (it
    was ]]{style="color: inherit;"
    olk-copy-source="MessageBody"}
- [[Name]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
- [[choose subset Z → note have to know Z planes you
  want]]{style="color: inherit;"
  olk-copy-source="MessageBody"}

[[Should write a simple set of files for each in a folder and you can
drag the folder into
ImageJ]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[This is Tedious For multicolor can multi position - but can be nice
for quick
checks]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[Reccomended to use the other two files Step 1 and step
2]]{style="color: inherit;"
olk-copy-source="MessageBody"}

\

[[[maxintensity_raw_easygui_0403224_dualcolor.py](/download/attachments/698323118/maxintensity_raw_easygui_0403224_dualcolor.py?version=1&modificationDate=1741825480000&api=v2){.confluence-embedded-file
nice-type="null"
file-src="/download/attachments/698323118/maxintensity_raw_easygui_0403224_dualcolor.py?version=1&modificationDate=1741825480000&api=v2"
linked-resource-id="698323199" linked-resource-type="attachment"
linked-resource-container-id="698323118"
linked-resource-default-alias="maxintensity_raw_easygui_0403224_dualcolor.py"
mime-type="application/octet-stream" has-thumbnail="false"
linked-resource-version="1" can-edit="true"
aria-label="maxintensity_raw_easygui_0403224_dualcolor.py"
draggable="false"}{.companion-edit-button-placeholder
.edit-button-overlay linked-resource-container-id="698323118"
linked-resource-id="698323199" template-name="companionEditIcon"
source-location="embedded-attachment"}[[[maxintensity_raw_easygui_121522.py](/download/attachments/698323118/maxintensity_raw_easygui_121522.py?version=1&modificationDate=1741825458000&api=v2){.confluence-embedded-file
nice-type="null"
file-src="/download/attachments/698323118/maxintensity_raw_easygui_121522.py?version=1&modificationDate=1741825458000&api=v2"
linked-resource-id="698323198" linked-resource-type="attachment"
linked-resource-container-id="698323118"
linked-resource-default-alias="maxintensity_raw_easygui_121522.py"
mime-type="application/octet-stream" has-thumbnail="false"
linked-resource-version="1" can-edit="true"
aria-label="maxintensity_raw_easygui_121522.py"
draggable="false"}{.companion-edit-button-placeholder
.edit-button-overlay linked-resource-container-id="698323118"
linked-resource-id="698323198" template-name="companionEditIcon"
source-location="embedded-attachment"}

\

### [[Max_intensity_raw_030525 STEP 1]]{style="color: inherit;" olk-copy-source="MessageBody"}

[[Will down sample by default and will autodetect and split
files]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[Makes a new folder for
each]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[Gives line
prompts]]{style="color: inherit;"
olk-copy-source="MessageBody"}

- [[point to raw
  data]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
- [[folder for
  output]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
- [[choose to down sample (default is
  Y)]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
- [[Allows you to assign Green, Magenta, Cyan, and
  Yellow]]{style="color: inherit;"
  olk-copy-source="MessageBody"}
- [[will autoscale/detect (or you can choose min and max for each
  channel)]]{style="color: inherit;"
  olk-copy-source="MessageBody"}

[[[step1_maxintensity_raw_030525.py](/download/attachments/698323118/step1_maxintensity_raw_030525.py?version=1&modificationDate=1741825392000&api=v2){.confluence-embedded-file
nice-type="null"
file-src="/download/attachments/698323118/step1_maxintensity_raw_030525.py?version=1&modificationDate=1741825392000&api=v2"
linked-resource-id="698323196" linked-resource-type="attachment"
linked-resource-container-id="698323118"
linked-resource-default-alias="step1_maxintensity_raw_030525.py"
mime-type="application/octet-stream" has-thumbnail="false"
linked-resource-version="1" can-edit="true"
aria-label="step1_maxintensity_raw_030525.py"
draggable="false"}{.companion-edit-button-placeholder
.edit-button-overlay linked-resource-container-id="698323118"
linked-resource-id="698323196" template-name="companionEditIcon"
source-location="embedded-attachment"}

### **[[Video_030525 Step 2]]{style="color: inherit;" olk-copy-source="MessageBody"}**

[[Runs on the Previous
MIPs ]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[will give overlay video and
montage]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[Reccomended FPS is
7]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[Auto
mirrorors]]{style="color: inherit;"
olk-copy-source="MessageBody"}

[[[step2_video_030525.py](/download/attachments/698323118/step2_video_030525.py?version=1&modificationDate=1741825403000&api=v2){.confluence-embedded-file
nice-type="null"
file-src="/download/attachments/698323118/step2_video_030525.py?version=1&modificationDate=1741825403000&api=v2"
linked-resource-id="698323197" linked-resource-type="attachment"
linked-resource-container-id="698323118"
linked-resource-default-alias="step2_video_030525.py"
mime-type="application/octet-stream" has-thumbnail="false"
linked-resource-version="1" can-edit="true"
aria-label="step2_video_030525.py"
draggable="false"}{.companion-edit-button-placeholder
.edit-button-overlay linked-resource-container-id="698323118"
linked-resource-id="698323197" template-name="companionEditIcon"
source-location="embedded-attachment"}

\

\

## Attachments:

[step1_maxintensity_raw_030525.py](attachments/698323118/698323196.py)
(application/octet-stream)\

[step2_video_030525.py](attachments/698323118/698323197.py)
(application/octet-stream)\

[maxintensity_raw_easygui_121522.py](attachments/698323118/698323198.py)
(application/octet-stream)\

[maxintensity_raw_easygui_0403224_dualcolor.py](attachments/698323118/698323199.py)
(application/octet-stream)\