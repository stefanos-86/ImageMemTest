# ImageMemoryTest

This software is a low-cost tool to create simple experiments that test memory recall.

The essence of such experiments is to show a participant several images. The participant must learn and remember their position.
There can be several "variations" on this basic idea: show the images one at a time or in a group, for a different time, on 
different positions on the screen, as well as using different sets of images.

After watching the images, the participant is asked to recall the positions of the images that he or she can remember.
The experimenter wants to measure the accuracy of the answer (distance between the real position and the remembered positions).
Coarse measurment in terms of screen pixels are enough to compare images, to see what can be "remembered closer".

This tool was created as a low cost replacement for commercially available software (like [Superlab](https://www.noldus.com/)) that
could not be procured for the planned experimental campaign, as well as to improve over other "expedient" methods of implementing the 
tests (e. g. animated Power Point decks).

The software was made for just that series of experiments.
It was developed, at no cost, to answer a personal request from one of the experimenters.
There are no plans to continue developing this tool or to use it again in the future.

Neither I nor the experimenters planned to share the code. It was deemed uninteresting and not needed for the scientific work we were trying to accomplish.
Years later we created the repository mostly as our own archive... if a bit too late.
Nevertheless, it may be of interest to other experimenters - thus we leave the repository public for everyone who may be curious.

### Usage
Please refer to [the user guide](https://github.com/stefanos-86/ImageMemTest/blob/main/Instructions.odt).

*Be sure that the test files are trusted. The experiment files can contain arbitrary code.*
This was, at the time, an acceptable risk. The software was to be used under controlled conditions
(e. g. no sharing of experiment files, host computer kept under supervision of the experimenter...).

_Be aware that the software may not correctly calculate the distance between the original image position and the test marker
if the subject places the markers too far away from the expected position._ In practice this turned out not to be a problem:
"normal" paticipants can usually reconstruct the test configuration with sufficient accuracy. [See here](https://github.com/stefanos-86/ImageMemTest/blob/main/Casi%20Patologici.odt) for more details (in Italian).


### Techincal Details

This is old (as of 2023) code, based on Python 2.7.

It is a low cost effort, which required some compromises, like keeping the dependencies to a minimum
and "forcing" the built-in Tkinter Python UI framework to display images as if they were movable sprites rather than elements of a GUI.

The tool is targeted to "novice" users (not to other developers or technicians). Nevertheless it must be programmable (within limits)
to let them implement different kind of experiments or to vary the experiments parameters. A GUI would be too costly to implement,
a whole domain language too complex to use.

The compromise is to allow writing simple commands in text file.
To further keep the implementation simple, those commands are... constructors. Each command corresponds to a class, it can be "fed" to eval()
to create an instance. Then it is just a matter of running trough the list of commands - no parsing or other decoding required (other than
what comes "free" from the Python interpreter).

On the downside, this leaves the tool wide open for arbitrary code injections. The risk was (hopefully) minimal on the intended use case: single installation
on a PC under complete control of the experimenter, no sharing of files, making the compromise acceptable.

Other than that, there are classes to handle the test images, the markers, load files... They are "plain code", there are no "special tricks". There are unit tests
in the test folders but they were not run when uploading the code to GitHub. The main program was simply "smoke tested" but should still be functional.

The Release script is not part of the tool. It quikly packages a zip file with all the code, than can then be sent to an experimenter.

### Published Works
The software, in spite of its basic nature, could be successfully used "in the field".

The work that includes the experiments done with this software is published in the
[Frontiers in Psychology](https://www.frontiersin.org/articles/10.3389/fpsyg.2019.02587/full) journal.



