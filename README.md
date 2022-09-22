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

*METROPOLIS HASTINGS ALGORITHM* https://www.youtube.com/watch?v=0lpT-yveuIA&ab_channel=MachineLearningTV

## Print PCB ##
It is one of the intermidiary steps deployed during the illustration of the tracks and it is a heatmap, of the number of hits, per SiPM of each PCB. It can be used independantly 
of the track reconstruction algorithm, and it is usually deployed, for hardware debugging, in order to detect mulfunctioning photomultipliers , or weak board connection spots. 

## Track Reconstruction ##
Track Reconstruction folder consists of numerous scripts and intermidiary data results, which are later used in time calibration folder. The primary tasks of this section of data analysis, is the reconstruction of the tracks, which is acheived, deploying the Houhg Transform. However, there are certain limitations introduced to the system. It onlys manages to select events, which present a single particle. Nonetheless, with some slight modifications to the algorithm all possible cases may be incorporate all posible cases. 

## Time Calibration ##
Time calibration cna be acheived only in the context of relative time calibration, without the use of any laser. That stems from the fact, that all timestamps are in fact relative to the actual event seed. Therefore, any delay time can be evaluated relative to a single SiPM. This can be calculated, simply by evaluating the difference in distnace travelled, and the relative delay, according to a single activation of the reference SiPM. Then the algorithm pivots from SiPM to SiPM, calculating the realtvie delay corresponding to an activation in time. However, this method presents an intrinsic flow. The real zero is practically impossible to be evaluated. Therefore, as a final step, we plot the time residuals, of each SiPM, and follow once again the pivot sequence, determining the real zeros, of each SiPM and subsequently the real delay. 
