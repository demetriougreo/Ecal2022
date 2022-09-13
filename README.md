# Ecal2022
The Folder Analyse contains all scripts develloped during the Summer project. It contains 5 different folders, each dedicated to each individual task. Regarding he steps 
once has to follow in order to navigate her/himself in the folders it could check the actual documentation report, as well as the Tutorial Video. 

## Amplitude Calibration ##
Amplitude Calibration contains all relative scripts and data, with regard to the charge integration of the Tofpets. Each tofpet, consists of 3 integration sub-circuits,
which can be deployed during the recording of a hit, to determine the charge of the produced signal, which in retrospect corresponds to the deposited energy of the 
traversing particel. 

## Angular Study ##
Angular study segment investigates the angular distribution of the inciding cosmic-rays/muons. There are two sub-tasks that are incorporated in the current study. 
Firstly, we look to verify the dependancy on the $cos^2\theta$ of the elevation angle, and secondary to validate the uniform azimuthal distibution of the muons. 
In the folder *Graphs* all produced data is illustrated and juxtaposed with the anticipated Monte-Carlo distribution (Implementing the Metropolis-Hastings Angorithm
for a symmetrical distribution). In the current form of the algorithm, it reproduces results that resemble the expected ones. Yet, there has been detected certain bugs
in the track reconstruction algorithm, that influence the behaviour of the results, and make them deviate in certain regions from the Metropolis-Hastings results.The problem 
appears, when the projected elevation angles, are small, correspong to consecutive SiPMs of the same Layer to be activated. 

## Print PCB ##
It is one of the intermidiary steps deployed during the illustration of the tracks and it is a heatmap, of the number of hits, per SiPM of each PCB. It can be used independantly 
of the track reconstruction algorithm, and it is usually deployed, for hardware debugging, in order to detect mulfunctioning photomultipliers , or weak board connection spots. 

## Track Reconstruction ##
Track Reconstruction folder consists of numerous scripts and intermidiary data results, which are later used in time calibration folder. The primary tasks of this section of data analysis, is the reconstruction of the tracks, which is acheived using the 

## Time Calibration ##
