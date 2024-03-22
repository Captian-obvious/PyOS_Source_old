import PyOS.Filesystem as fs;
import tkinter as tk;
import customtkinter as ctk;
from .Modules.tksvg import SvgImage;
import webview as wv;
import PIL.Image as imgReader;
import PIL.ImageTk as tkImgReader;
#UI Widget Fills
X=tk.X;
Y=tk.Y;
BOTH=tk.BOTH;
#UI Widget Anchors
CENTER=tk.CENTER;
N=tk.N;
NW=tk.NW;
NE=tk.NE;
S=tk.S;
SW=tk.SW;
SE=tk.SE;
E=tk.E;
W=tk.W;
#UI Widget Other
LEFT=tk.LEFT;
RIGHT=tk.RIGHT;
TOP=tk.TOP;
BOTTOM=tk.BOTTOM;
END=tk.END;
NONE=tk.NONE;
#UI classes
class UI:
    def __init__(self):
        pass;
    ##end
##end
class UI_Window(tk.Tk):
    def __init__(self,screenName=None,title='Window',width=300,height=300):
        tk.Tk.__init__(self,screenName=screenName);
        self.geometry(f'{width}x{height}');
        self.title(title);
    ##end
    def setAttribute(self,attribute,value):
        if (attribute.lower()=='isfullscreen' or attribute.lower()=='fullscreen'):
            self.attributes('-fullscreen',value);
        elif (attribute.lower()=='ismaximized' or attribute.lower()=='maximized'):
            self.attributes('-zoomed',value);
        elif (attribute=='isresizable' or attribute=='resizable'):
            self.resizable(value,value);
        else:
            self.attributes('-'+attribute,value);
        ##endif
    ##end
    def setSize(self,width=300,height=300):
        self.geometry(f'{width}x{height}');
    ##end
    def setTitle(self,title):
        self.title(title);
    ##end
    def setIcon(self,iconpath,issvg=False):
        global img;
        if (issvg):
            img=SvgImage(file=iconpath);
        else:
            img=tk.PhotoImage(file=iconpath);
        ##endif
        self.iconphoto(True,img);
    ##end
##end
class UI_TopLevel(tk.Toplevel):
    def __init__(self,master,cnf={},title='Window',width=300,height=300,**kwargs):
        tk.Toplevel.__init__(self,master,cnf,**kwargs);
        self.geometry(f'{width}x{height}');
        self.title(title);
    ##end
    def setAttribute(self,attribute,value):
        if (attribute.lower()=='isfullscreen' or attribute.lower()=='fullscreen'):
            self.attributes('-fullscreen',value);
        elif (attribute.lower()=='ismaximized' or attribute.lower()=='maximized'):
            self.attributes('-zoomed',value);
        elif (attribute=='isresizable' or attribute=='resizable'):
            self.resizable(value,value);
        else:
            self.attributes('-'+attribute,value);
        ##endif
    ##end
    def setSize(self,width=300,height=300):
        self.geometry(f'{width}x{height}');
    ##end
    def setTitle(self,title):
        self.title(title);
    ##end
    def setIcon(self,iconpath,issvg=False):
        global img;
        if (issvg):
            img=SvgImage(file=iconpath);
        else:
            img=tk.PhotoImage(file=iconpath);
        ##endif
        self.iconphoto(True,img);
    ##end
##end
class UI_Frame(tk.Frame):
    def __init__(self,master,cnf={},**kwargs):
        tk.Frame.__init__(self,master,cnf={},**kwargs);
    ##end
##end
class UI_Label(tk.Label):
    def __init__(self,master,cnf={},**kwargs):
        tk.Label.__init__(self,master,cnf,**kwargs);
    ##end
    def setText(self,text):
        self.config(text=text);
    ##end
    def setImg(self,path,issvg=False):
        global img;
        if (issvg):
            img=SvgImage(file=path);
        else:
            img=tk.PhotoImage(file=path);
        ##endif
        self.config(image=img);
    ##end
    def setFont(self,font):
        self.config(font=font);
    ##end
##end
class UI_Button(tk.Button):
    def __init__(self,master,cnf={},**kwargs):
        tk.Button.__init__(self,master,cnf,**kwargs);
    ##end
    def setText(self,text):
        self.config(text=text);
    ##end
    def setImg(self,path,issvg=False):
        global img;
        if (issvg):
            img=SvgImage(file=path);
        else:
            img=tk.PhotoImage(file=path);
        ##endif
        self.config(image=img);
    ##end
    def setFont(self,font):
        self.config(font=font);
    ##end
    def setCommand(self,command):
        self.config(command=command);
    ##end
##end
class UI_Canvas(tk.Canvas):
    def __init__(self,master,cnf={},**kwargs):
        tk.Canvas.__init__(self,master,cnf,**kwargs);
    ##end
##end
class UI_Entry(tk.Entry):
    def __init__(self,master,cnf={},**kwargs):
        tk.Entry.__init__(self,master,cnf,**kwargs);
    ##end
##end
class UI_Checkbutton(tk.Checkbutton):
    def __init__(self,master,cnf={},**kwargs):
        tk.Checkbutton.__init__(self,master,cnf,**kwargs);
    ##end
##end
class UI_Listbox(tk.Listbox):
    def __init__(self,master,cnf={},**kwargs):
        tk.Listbox.__init__(self,master,cnf,**kwargs);
    ##end
    def append_text(self,text):
        self.insert(tk.END,text);
    ##end
##end
class UI_CustomWindow(ctk.CTk):
    def __init__(self,fg_color: str | tuple[str,str] | None=None,title='Window',width=300,height=300,*a,**kwargs):
        ctk.CTk.__init__(self,fg_color,*a,**kwargs);
        self.geometry(f'{width}x{height}');
        self.title(title);
    ##end
    def setAttribute(self,attribute,value):
        if (attribute.lower()=='isfullscreen' or attribute.lower()=='fullscreen'):
            self.attributes('-fullscreen',value);
        elif (attribute.lower()=='ismaximized' or attribute.lower()=='maximized'):
            self.attributes('-zoomed',value);
        elif (attribute=='isresizeable' or attribute=='resizeable'):
            self.resizable(value,value);
        else:
            self.attributes('-'+attribute,value);
        ##endif
    ##end
    def setSize(self,width=300,height=300):
        self.geometry(f'{width}x{height}');
    ##end
    def setTitle(self,title):
        self.title(title);
    ##end
    def setIcon(self,iconpath,issvg=False):
        global img;
        if (issvg):
            img=SvgImage(file=iconpath);
        else:
            img=tk.PhotoImage(file=iconpath);
        ##endif
        self.iconphoto(True,img);
    ##end
##end
class UI_CustomFrame(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        ctk.CTkFrame.__init__(self,master,**kwargs);
    ##end
##end
class UI_CustomLabel(ctk.CTkLabel):
    def __init__(self,master,cnf={},**kwargs):
        ctk.CTkLabel.__init__(self,master,**kwargs);
    ##end
    def setText(self,text):
        self.configure(text=text);
    ##end
    def setImg(self,path,issvg=False):
        global img;
        if issvg:
            img=SvgImage(file=path);
        else:
            img=ctk.CTkImage(light_image=imgReader.open(path),dark_image=imgReader.open(path));
        ##endif
        self.configure(image=img);
    ##end
    def setFont(self,font):
        self.configure(font=font);
    ##end
##end
class UI_CustomButton(ctk.CTkButton):
    def __init__(self,master,**kwargs):
        ctk.CTkButton.__init__(self,master,**kwargs);
    ##end
    def setText(self,text):
        self.configure(text=text);
    ##end
    def setImg(self,path,issvg=False):
        global img;
        img=ctk.CTkImage(light_image=imgReader.open(path),dark_image=imgReader.open(path));
        self.configure(image=img);
    ##end
    def setFont(self,font):
        self.configure(font=font);
    ##end
    def setCommand(self,command):
        self.configure(command=command);
    ##end
##end
class UI_CustomCanvas(ctk.CTkCanvas):
    def __init__(self,master,**kwargs):
        ctk.CTkCanvas.__init__(self,master,**kwargs);
    ##end
##end
class UI_CustomEntry(ctk.CTkEntry):
    def __init__(self,master,**kwargs):
        ctk.CTkEntry.__init__(self,master,**kwargs);
    ##end
##end
class UI_CustomCheckbutton(ctk.CTkCheckBox):
    def __init__(self,master,**kwargs):
        ctk.CTkCheckBox.__init__(self,master,**kwargs);
    ##end
##end
def round_rectangle(canvas,x1,y1,x2,y2,radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True);
##end
def create_circle(canvas,x,y,radius=25,**kwargs):
    return canvas.create_oval(x-radius,y-radius,x+radius,y+radius,**kwargs);
##end