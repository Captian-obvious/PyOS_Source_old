import PyOS.LinuxUtils as linux;
import PyOS.Pointer as pt
import PyOS.UI as ui;
from datetime import datetime as dt;
##define clockModule
global menu_shown;
menu_shown=False;
class Clock:
    def __init__(self,name,showInTaskbar=True):
        self.name=name;
        self.inTaskbar=showInTaskbar;
        self.clockLabel=None;
        self.cWindow:ui.UI_Canvas|None=None;
        self.cLabel:int|None=None;
        self.curTime="0:00:00";
        self.tbTime="0:00";
        self.curHour=0;
        self.curMin=0;
        self.curSec=0;
        self.curDate="0/0/0";
        self.minStr="";
        self.secStr="";
        self.win:ui.UI_Window|ui.UI_CustomWindow|None=None;
        self.win2:ui.UI_Window|ui.UI_CustomWindow|None=None;
        self.tbCanvas:ui.UI_Canvas|None=None;
    ##end
    def getOSTime(self):
        return dt.utcnow().ctime();
    ##end
    def getOSClockTime(self):
        return dt.utcnow().strftime("%H:%M:%S");
    ##end
    def getOSDate(self):
        return dt.utcnow().strftime("%d/%m/%Y");
    ##end
    def start(self,win=None,tbCanvas=None):
        self.win=win;
        self.tbCanvas=tbCanvas;
        self.clockRunning=True;
        def doClock():
            self.curTime=self.getOSTime();
            self.curHour=int(dt.utcnow().strftime("%H"));
            self.curMin=int(dt.utcnow().strftime("%M"));
            self.curSec=int(dt.utcnow().strftime("%S"));
            self.minStr=str(self.curMin);
            self.secStr=str(self.curSec);
            while (self.clockRunning):
                linux.time.sleep(1);
                self.curSec=self.curSec+1;
                self.minStr=str(self.curMin);
                self.secStr=str(self.curSec);
                if self.curSec==60:
                    self.curMin=self.curMin+1;
                    self.curSec=0;
                    print('clock update');
                    if self.curMin==60:
                        self.curMin=0;
                        self.curHour=self.curHour+1;
                    ##endif
                ##endif
                if self.curHour==24:
                    self.curHour=0;
                ##end
                if self.curMin<10:
                    self.minStr="0"+str(self.curMin);
                ##endif
                if self.curSec<10:
                    self.secStr="0"+str(self.curSec);
                ##endif
                self.curTime=str(self.curHour)+":"+self.minStr+":"+self.secStr
                self.tbTime=str(self.curHour)+":"+self.minStr;
                if self.getOSTime()!=self.curTime:
                    curTime=self.getOSTime();
                ##endif
                self.updateClock();
            ##end
        ##end
        self.cThread=linux.task.Thread(target=doClock);
        self.cThread.start();
    ##end
    def updateClock(self):
        if (self.inTaskbar):
            if self.tbCanvas!=None:
                if (self.clockLabel==None):
                    self.clockLabel=self.tbCanvas.create_text(self.tbCanvas.winfo_width()-64,self.tbCanvas.winfo_height()/2,text='0:00',font=("Helvetica",15),width=64,fill="white",tags=("clickable","clock"));
                ##endif
                self.tbCanvas.itemconfig(self.clockLabel, text=self.tbTime);
                
            ##endif
        ##endif
        if (self.cWindow):
            self.cWindow.itemconfig(self.cLabel, text=self.curTime);
        ##endif
        if self.win:
            self.win.update();
        ##endif
        if self.win2:
            self.win2.update();
        ##endif
    ##end
    def stop(self):
        self.clockRunning=False;
    ##end
##end

# [this is a startup program!]
#create an instance of clock
clock=Clock('Primary');
def main(root:ui.UI_Frame|ui.UI_CustomFrame):
    global menu_shown;
    if menu_shown==True:
        menu_shown=False
        root.place_forget();
        on_close();
    else:
        menu_shown=True;
        root.place(relx=1,y=root.master.winfo_height()-32,relwidth=.25,relheight=.4,anchor=ui.SE);
        if (root.winfo_screenwidth()<800):
            root.place(relx=1,y=root.master.winfo_height()-32,relwidth=.3,relheight=.6,anchor=ui.SE);
        ##endif
        on_open(root);
    ##endif
##end
def on_open(root):
    global clock;
    #OS will start the clock
    #Here we instead put the clock frame config
    root.focus_force();
    canvas=ui.UI_Canvas(root,width=root.winfo_width(),height=root.winfo_height(),bg='#333');
    canvas.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
    clock.cWindow=canvas;
    centerX=canvas.winfo_width()/2;
    centerY=canvas.winfo_height()/2;
    clock.cLabel=canvas.create_text(centerX,centerY,text='0:00:00',font=("Helvetica",30),width=96,fill='white');
##end
def on_close():
    global clock;
    if clock.win2:
        clock.win2.destroy();
        clock.win2=None;
    ##endif
    clock.cLabel=None;
    if clock.cWindow:
        clock.cWindow.destroy();
        clock.cWindow=None;
    ##endif
##end