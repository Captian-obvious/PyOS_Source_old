import PyOS.UI as ui;
import PyOS.LinuxUtils as linux;
from .pyTerm import TerminalFrame;

root=ui.UI_Window();
root.setTitle('Terminal');
root.setSize(400,300);
root.focus_force();
root.iconphoto(True,ui.tk.PhotoImage(file='PyOS/programs/Terminal/favicon.png'));
terminalFrame=TerminalFrame(root,bg='#434343');
terminalFrame.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
terminalFrame.initialize();
root.mainloop();