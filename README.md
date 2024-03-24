# sensor-reliability
This repo dedicates to codes for assessing the reliability of air quality sensor network


### Dempster-Shafer algorithm

The file `DS.py` contains implementation of Dempster-Shafer algorithm. It is used to derive the probability of events, scenarios based on the given sampling matrix and feature matrix. The constructor of class `DempsterShafer` is initiated by passing the sampling and feature matrices with the type `numpy.array`. The method `result` of the class abstracts the Dempster-Shafer combination rule and **returns** the probability of the hypotheses in the feature matrix.

### Plotting results
The plots illustrating results from the reliability assessment of Dempster-Shafer are encoded in ``.

#### Reliability
The probability assigned to each hypothesis is plotted as 100% stacked graph.

#### Highest reliability
Probability of the normal operation is plotted for comparison.

#### Switching
Switching is performed based on the highest probability of normal operation within all sensors of the dependable system. A form of Gantt chart is plotted to visualize the time interval when a sensor is selected.

#### Continuous data flow
In this graph, a continuous data flow of measured parameters is established through the switching mechanism. A continuous flow is constructed by stitching intervals of data from different sensors in the dependable system.

