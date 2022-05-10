# Vibration Analysis V2
### Introduction to Metal 3D Printing
Metal 3D printing has been on the rise in the recent years, with the main benefit being that it can manufacture intricate and bespoke parts that tradiitonal manufacturing techniques are unable to produce, allowing for advancement of technology in aerospace, medical inductries etc.
However, it still comes with its limitations, one of which being that not all parts can be manufactured this way. Due to the high temperatures needed to melt the metal powder, there will inevitably be distortion and warping experienced by the metal part. A common solution to this is to add
support structures to the parts, which can either hold the part in place, or act as a heatsink to reduce the stress in the area.


### How Does Metal 3D Printing Work?
A thin layer of metal powder is deposited on the print job. A laser beam is then exposed onto the layer, fusing the metal powder with the previous layers.
The following schematic shows the schematic of the interior of an EOS M290 printer.

![EOS M290 printer](<./Photos/EOS M290.jpeg>)
*Front of EOS M290 printer*

![EOS M290 printer](<./Photos/EOS M290.jpeg>)
*Front of EOS M290 printer*  

![Schematic of EOS M290 printer](<./Photos/EOSM290 schematic.png>)  
*Schematic of EOS M290 chamber*  

![Interior of EOS M290 printer](<./Photos/M290 interior.png>)  
*Picture of EOS M290 chamber*  

### Project Introduction
Without the proper support structures in place, the printed metal can experience stress, causing the print to warp. When the recoater arm sweeps across the build plate to apply the next layer of metal powder, it may scrape against these warped parts that jut out of the layer, causing streaking in the newly applied layer (the new layer will not be applied evenly).
As such, there will be many problems with the print. In the worst case, the protrusions in the layers may even jam the recoater arm, causing the print to stop.

Therefore, we can tell how successful a print is by the amount of warping the parts experience, which leads to the vibration experienced by the recoater arm.

In the project, I attempted to use the vibrations experienced by the recoater arm as a metric to map out the parts of the print that has experienced warping visually.

### Set-up of Print Chamber 

To record the vibrations that the recoater arm experiences, I planned to attach an accelerometer to the recoater arm and allowed it to record while the print was ongoing. However, due to the space constrains within the print chamber, the power and data storage must be wired in externally.
As the chamber needed to be filled with Nitrogen gas for the print (to prevent any combustion), the chamber must be airtight, so I had to think of a solution to feed power toand data out of the accelerator during the print.
To tackle this problem statement, I replaced one of the plugs that was situated on the top of the print chamber with a Printed Ciruit Board (PCB) mounted on a custom-made metal mount, which allowed electrical signals to go through, but not any exchanges of gas.

![Plug in print chamber](<./Photos/Plug.png>)  
*Plug in the print chamber*  

![PCB in print chamber](<./Photos/PCB.png>)  
*Plug in the print chamber was replaced by a PCB mounted on a custom metal holder*  

To mount the accelerometer on the recoater arm, I designed a plastic mount which was then 3D printed. It could clamp on a ledge of the recoater arm, and allowed me to mount sensors within a hole in the recoater arm.

![Mount](<./Photos/Mount.png>)  
*Mount was specially designed and printed within the allowable limits in the print chamber. There were some issues when printing the mount which led to its uneven surface. Despite that, the mount worked fine so there was no need to reprint one.*  

The sensors in the chamber could thus be fed to the PCB using a coiled cable. The parts in the print chamber were then secured in place and that they were not blocking the laser. A laptop was connected to the PCB from the outside, which allowed for supply of power and data storage. The whole set-up is then allowed to run while the print was ongoing.

![Recoater arm on the extreme left of the chamber](<./Photos/Arm on left.png>)  
*Recoater arm on the extreme left of the chamber. The components were secured so that they would not drop out in the middle of the print or are obstructing the laser.*  

![Recoater arm on the extreme right of the chamber](<./Photos/Arm on right.png>)  
*Recoater arm on extreme right of the chamber*  

### Results

The .stl file of the print job can b e viewed at [Overhang.stl](<./Photos/Overhang.stl>).

![CAD file used for the print](<./Photos/CAD_file.png>)  
{{< caption >}}CAD file used for the print{{< /caption >}}
*CAD file used for the print*  


There were existing data from previous prints which showed that the steeper the overhang angle on the module, the more likely the overhang will warp up. Hence, I chose to print these CAD modules so that more vibrations will be experienced by the recoater arm.
The whole print took around five hours. After the print job was done, I disassembled the set-up. The data collected can be viewed at [putty_arduino.csv](<./putty_arduino.csv>).

After some processing, the raw data is saved into a .npy file for faster processing in subsequent code. As the arm moves along the x-axis, we will be using the x-axis data.

![Graph of raw x-data](<./Photos/Raw image graph.png>)  
*Raw X-axis data*  

Zooming in, we obtain the x-axis data for a single layer:

![Graph of one cycle](<./Photos/One cycle.png>)  
*Data for one layer*  

The first frame of acceleration is when the recoater moves from the left side of the machine to the right. It has a higher speed, thus we see that the acceleration is higher and the time taken is shorter. The second frame is when the recoater moves from the right side of the 
machine to the left. Through this movement, the recoater arm sweeps an even layer of metal powder on top of the build plate. This movement is slower, therefore taking a longer time.

The first step of the code is to remove all the unnecessary data and obtain the accelerations recorded when the arm is moving from right to left. I used a low-pass filter and some smoothing, to get a windowing as follows:

![Windowing](<./Photos/Windowing.png>)  
*Window for recoater arm movement*  

After some more post processing, I was able to obtain the window where the recoater arm moved from right to left. As we are only interested in the parts when the recoater arm moves over the build plate, I utilised the position of the build plate relative to the whole movement to truncate the data even more. However,
this assumes that the recoater arm moves at a constant speed, and its acceleration is infinite.

Once I obtained the regions of interest, I plotted the X, Y and Z plots. I found out that the X plot displayed the most information, so I went with only the X-plot for processing later on.

![X-plots](<./Photos/X-axis plot.png>)  
*Plot of data from all the layers superimposed on one another. We can see the sharp spikes on a few of the layers, caused by the warping of the modules. 
*  

I took this data and plot it onto a 2D heatmap. Due to the nature of the recoater arm, we can only identify vibrations in the X and Z-axes. I then rendered the X-Z view of the CAD image.

![2D CAD view](<./Photos/2D-cadview.png>)    
*2D CAD view of .stl file generated by the script*

![2D CAD view](<./Photos/2D-cadview.png>)    
*2D CAD view of .stl file generated by the script*

The 2D CAD photo was scaled accordingly, and then superimposed on the heatmap, creating our final product.

![Final image](<./Photos/Final image.png>)  
*Final image*  

### Conclusion
This project serves as a proof of concept that it is possible to see the areas affected by distortion and warping through reading the vibrations experienced by the recoater arm. During the print, it was observed that the module with the steepest overhand experienced a slight warping, which is translated into the vibration data. This shows that this method of visualising warping is sensitive and feasible.   

However, in the final image that was generated, the regions of higher vibrations did not seem to match with the exact position of the module. Reasons for this offset is discussed later.

### Challenges (yet to be solved)
1. For each layer of the truncated data, the number of data points does not seem to be the same (as seen at the ends of each layer). This leads to some of the layers in the heatmap to have an offset and is probably why the areas of high vibration does not match exactly with the .stl file.
2. The regions of interest (when recoater arm is sweeping on the build plate) is obtained by knowing the position of the build plate relative to the whole recoater movement, assuming that the recoater moves at a constant speed and acceleration is infinite. No matter how good the windowing algorithm is, there still seems to be a discrepancy in whether the build plate starts and ends. An improvement in the future could be to install a photodetector on the mount, allowing us to identify when the arm is moving over the build plate.
3. Due to the slow Serial.print() function in the Arduino, the accelerometer only samples at slightly over 500Hz despite being hooked up via SPI. The promised max frequency is 25.6KHz.