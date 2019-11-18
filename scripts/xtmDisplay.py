import numpy
from matplotlib import pyplot
from matplotlib.widgets import Slider, Button, RadioButtons

class xtmDisplay():
    """
    DESCRIPTION:
        Class to plot xtm images.
    PARAMETERS:
        imageList=<list>
            List of images. May be just on eimage, but must be a list 
    """
    def __init__(self):
        
        self.imageList=[]
        self.titleList=[]
        self.ROI=None  # needed if a ROI is given. List with [x1y2,x1,y2] values for displaying the correct CCD area
        self.coords=[]

        self.__noi=0
        self.__imageBoxList=[]
        self.__sliderVminBoxList=[]
        self.__sliderVmaxBoxList=[]
        self.__histBoxList=[]
        
    def Display(self):
        """
        DESCRIPTION:
            Create image window
        """
        self.__noi=len(self.imageList)
        self.coords=numpy.zeros((self.__noi,4))

        self.fig=pyplot.figure(figsize=[self.__noi*6,8]);
        self.fig.set_size_inches(self.__noi*6,8)
        histAxList,sliderVminAxList,sliderVmaxAxList,imageAxList=[],[],[],[]
        self.__imageBoxList=[]
        self.__sliderVminBoxList=[]
        self.__sliderVmaxBoxList=[]
        self.__histBoxList=[]
        i=0
        cid=self.fig.canvas.mpl_connect('button_press_event',self.__onclick)
        for image in self.imageList:
            # axes definitions:
            padding = 0.05
            width = (0.8-(self.__noi-1)*padding)/self.__noi

            bottomHist, heightHist = padding, 0.12
            boxHeight=2*padding+bottomHist+heightHist
            #bottomSliderVmin, heightSliderVmin = boxHeight, 0.01
            #boxHeight+=padding/2+heightSliderVmin
            #bottomSliderVmax, heightSliderVmax = boxHeight, 0.01
            #boxHeight+=padding+heightSliderVmax
            bottomImage, heightImage = boxHeight, 1-(boxHeight+padding)
            
            histAxList.append([padding+i*(width+padding),bottomHist,width,heightHist])
            #TODO add vmin vmax sliders
            #sliderVminAxList.append([padding+i*(width+padding),bottomSliderVmin,width,heightSliderVmin])
            #sliderVmaxAxList.append([padding+i*(width+padding),bottomSliderVmax,width,heightSliderVmax])
            imageAxList.append([padding+i*(width+padding),bottomImage,width,heightImage])

            self.__histBoxList.append(pyplot.axes(histAxList[i]))
            #self.__sliderVminBoxList.append(pyplot.axes(sliderVminAxList[i]))
            #self.__sliderVmaxBoxList.append(pyplot.axes(sliderVmaxAxList[i]))
            self.__imageBoxList.append(pyplot.axes(imageAxList[i]))
            
            #sVmin = Slider(self.__sliderVminBoxList[i], 'vmin', 0, 1, valinit=0)
            #sVmax = Slider(self.__sliderVmaxBoxList[i], 'vmax', 0, 1, valinit=1)

            #sVmin.on_changed(self.__updateColors)
            #sVmax.on_changed(self.__updateColors)
                    
            if self.ROI==None:
                self.__imageBoxList[i].imshow(image,interpolation='nearest',vmin=0,cmap='hot')
                self.__imageBoxList[i].set_title(self.titleList[i])
            else:
                xmin,xmax,ymin,ymax=min(self.ROI[0],self.ROI[2]),\
                        max(self.ROI[0],self.ROI[2]),\
                        min(self.ROI[1],self.ROI[3]),\
                        max(self.ROI[1],self.ROI[3])
                self.__imageBoxList[i].imshow(image,extent=[xmin,xmax,ymax,ymin],interpolation='nearest',vmin=0,cmap='hot')
                self.__imageBoxList[i].set_title(self.titleList[i])
            flat=image.flatten()
            self.__histBoxList[i].hist(flat,bins=255, histtype='stepfilled')
            i+=1
        pyplot.show();
        return None

    def __onclick(self,event):
        if event.inaxes in self.__imageBoxList:
            if event.button==2:
                print('red x=%d, z=%d'%(event.xdata, event.ydata))
                if len(event.inaxes.lines)==4:
                    del(event.inaxes.lines[:])
                self.coords[self.__imageBoxList.index(event.inaxes),0]=int(event.xdata)
                self.coords[self.__imageBoxList.index(event.inaxes),1]=int(event.ydata)
                event.inaxes.axhline(y=event.ydata,color='r')
                event.inaxes.axvline(x=event.xdata,color='r')
                pyplot.draw()
            if event.button==3:
                print('green x=%d, z=%d'%(event.xdata, event.ydata))
                if len(event.inaxes.lines)==4:
                    del(event.inaxes.lines[:])
                self.coords[self.__imageBoxList.index(event.inaxes),2]=int(event.xdata)
                self.coords[self.__imageBoxList.index(event.inaxes),3]=int(event.ydata)
                event.inaxes.axhline(y=event.ydata,color='g')
                event.inaxes.axvline(x=event.xdata,color='g')
                pyplot.draw()

    def __updateColors(self):
        pass
