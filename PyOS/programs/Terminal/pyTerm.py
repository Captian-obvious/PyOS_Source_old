from PIL.Image import DEFAULT_STRATEGY
import PyOS.LinuxUtils as linux;
import PyOS.UI as ui;
import re;

class sh_cmds:
    def __init__(self):
        self.cmd_literals=[
            {'cmd':'clear','desc':'clears the terminal','valid':['clear','clr','cls'],'arguments':'None'},
            {'cmd':'help','desc':'shows all commands','valid':['help'],'arguments':'(opt)<command>'},
            {'cmd':'exit','desc':'exits the terminal','valid':['exit','quit','q'],'arguments':'None'},
            {'cmd':'mkdir','desc':'creates a directory in the working path.','valid':['makedir','mkdir','md'],'arguments':'<dir_name>'},
            {'cmd':'cdir','desc':'changes the working directory.','valid':['chdir','cdir','cd'],'arguments':'<path>'},
            {'cmd':'remove','desc':'removes a file or directory.','valid':['remove','rm','rmdir'],'arguments':'[-rf|-r|-f] <path or file>'},
            {'cmd':'move','desc':'moves a file or directory.','valid':['move','mv'],'arguments':'<source> <destination>'},
            {'cmd':'copy', 'desc':'copies a file or directory.','valid':['copy','cp'],'arguments':'[-rf|-r|-f] <source> <destination>'},
            {'cmd':'python','desc':'Python Interpreter (if installed)','valid':['py','>>>'],'arguments':'<code or path>'},
            {'cmd':'battery_firmware','desc':'Access various parts of battery firmware','valid':['battery_firmware','battery_fw','batt_fw'],'arguments':'[-get|-set] <name> (opt)<value>'},
            {'cmd':'battery_status','desc':'Shows the status of the battery','valid':['battery_status','battery_stat','batt_stat'],'arguments':'(opt)<stat>'},
            {'cmd':'wifi_scan','desc':'Scans for available wifi networks','valid':['wifiscan','wifi_scan'],'arguments':'None'},
            {'cmd':'wifi_connect','desc':'Connects to a wifi network','valid':['wifi_connect','wifi_conn','wifi_c'],'arguments':'<ssid> (opt)<password>',},
        ]
    ##end
    def get_cmd(self,cmdstr):
        cmd_ran=None;
        cmdstr=cmdstr.lower();
        cmd_args=cmdstr.split(' ');
        cmd=cmd_args[0];
        cmd_args.pop(0);
        for cmd_literal in self.cmd_literals:
            if cmd in cmd_literal['valid']:
                cmd_ran={'name':cmd_literal['cmd'],'args':cmd_args};
                break;
            ##endif
        ##end
        if (cmd_ran==None):
            cmd_ran={'name':cmd,'args':cmd_args};
        ##endif
        return cmd_ran;
    ##end
    def run_builtin(self,cmd_ran,*args):
        if cmd_ran['name']=='clear':
            args[0].clear_text();
        elif cmd_ran['name']=='help':
            args[0].type_str('Available Commands:');
            for cmd_literal in self.cmd_literals:
                args[0].type_str(cmd_literal['cmd']+' - '+cmd_literal['desc']);
                args[0].type_str('  Arguments: '+str(cmd_literal['arguments']));
                args[0].type_str(''); # Buffer
            ##end
            return {"ran":True,"cmd":cmd_ran};
        else:
            return {"ran":False,"cmd":cmd_ran};
        ##endif
    ##end
##end

class TerminalFrame(ui.UI_Frame):
    def __init__(self,master,cnf={},**kwargs):
        if ('exec_path' in kwargs):
            self.exec_path=kwargs['exec_path'];
            self.path=self.parse_path(self.exec_path);
            kwargs.pop('exec_path');
        elif ('privs' in kwargs and 'root' in kwargs['privs'] and kwargs['privs']['root']==True):
            self.exec_path=linux.root_exec_path();
            self.path=self.parse_path(self.exec_path);
            kwargs.pop('privs');
        else:
            self.exec_path=linux.get_pwd();
            self.path=self.parse_path(self.exec_path);
        ##endif
        ui.UI_Frame.__init__(self,master,cnf,**kwargs);
        self.isInitialized=False;
        self.cmdToRun=None;
        self.curr_text='';
        self.mainTextArea=ui.tk.Listbox(self,bg='#434343',fg='#f90',font=('Courier New',8),highlightcolor='#434343', highlightthickness=0,selectbackground='#434343',selectforeground="#f90",activestyle=ui.tk.NONE);
        self.scrollbar=ui.tk.Scrollbar(self);
        self.copyrightStr='Copyright (c) 2024, PyOS Developers\n';
        self.versionStr='Version: 1.11.0\n';
        self.Keybinds={'<Return>':lambda x :self.enter_key_callback(),'<BackSpace>':lambda x :self.backspace_callback(),'<KeyPress>':lambda x :self.keypress_callback(x.char),'<KeyRelease>':lambda x :self.keyrelease_callback(x.char)};
        self.mainTextArea.pack(expand=1,fill=ui.BOTH);
        self.scrollbar.pack(side=ui.RIGHT,fill=ui.Y);
        self.log='';
    ##end
    def endsWith(self,s1,s2):
        return s1.endswith(s2);
    ##end
    def startsWith(self,s1, s2):
        return s1.startswith(s2);
    ##end
    def stringContains(self,s, s2):
        return s2 in s;
    ##end
    def execLater(self,func,func2,ti):
        def run():
            t=__import__('time');
            t.sleep(ti);
            if func:func();
            ##endif
            if func2:func2();
            ##endif
        ##end
        runner=linux.task.Thread(target=run);
        runner.start();
    ##end
    def parse_path(self,path):
        home_path_regex=r'(\/home\/[A-Za-z0-9_]+)\/(?:.*)';
        home_path_regex_match=re.match(home_path_regex,path);
        if (home_path_regex_match):
            mstr=home_path_regex_match.group(1);
            print(mstr);
            newpath=path.replace(mstr,'~');
            return newpath;
        else:
            return path;
        ##endif
    ##end
    def run_cmd(self,cmd,lastLI):
        command_summary=cmd.split(' ');
        linux.os.environ["PYTHONUNBUFFERED"]="1";
        result=linux.runner.run(command_summary,stdout=linux.runner.PIPE,stderr=linux.runner.STDOUT,shell=True,env=linux.os.environ);
        output=result.stdout;
        output_lines = output.splitlines();
        for k in output_lines:
            self.mainTextArea.insert(lastLI, k);
            lastLI+=1;
            self.master.update();
        ##end
        return;
    ##end
    def refresh(self,backspace=False):
        if (self.curr_text!=f'{self.path}> ' or backspace):
            self.mainTextArea.delete(ui.END);
        ##endif
        self.mainTextArea.insert(ui.END,self.curr_text);
        self.master.update();
        return;
    ##end
    def append_to_text(self,text,ymoveoverride=True):
        self.mainTextArea.delete(ui.END);
        self.curr_text=self.curr_text+text;
        self.mainTextArea.insert(ui.END,self.curr_text);
        if (ymoveoverride!=True):
            self.mainTextArea.yview_moveto(1);
        ##endif
    ##end
    def type_str(self,string):
        # types a given string automatically to the terminal.
        for k in string:
            self.append_to_text(k);
        ##end
        self.mainTextArea.yview_scroll(1, ui.tk.UNITS);
        self.master.update();
        return;
    ##end
    def enter_key_callback(self):
        compiler_thread=linux.task.Thread(target=self.run_cmd,args=(self.curr_text[len(self.path)+2 : ],self.mainTextArea.size()));
        compiler_thread.daemon=True;
        compiler_thread.start();
        self.curr_text=f'{self.path}> ';
        self.mainTextArea.insert(ui.END, self.curr_text);
        self.mainTextArea.yview_moveto(1);
        self.master.update();
        return;
    ##end
    def keypress_callback(self,key=''):
        if (key!=''):
            self.log+=f' (keydown - {key})';
            self.append_to_text(key);
            self.master.update();
        ##endif
    ##end
    def keyrelease_callback(self,key=''):
        if (key!=' '):
            self.log+=f' (keyup - {key})';
        ##endif
    ##end
    def backspace_callback(self):
        # callback for backspace key erases the last character.
        if (len(self.curr_text)>3):
            self.curr_text=self.curr_text[ : -1];
            self.refresh(True);
            self.master.update();
        ##endif
        return;
    ##end
    def initialize(self,startCmd=''):
        if (not self.isInitialized):
            print('I am initial');
            self.mainTextArea.insert(ui.END,"Welcome to the PyOS Terminal!");
            self.mainTextArea.insert(ui.END,"Type 'help' for a list of commands.");
            self.mainTextArea.insert(ui.END,self.copyrightStr);
            self.mainTextArea.insert(ui.END,self.versionStr);
            self.mainTextArea.insert(ui.END, '');
            self.mainTextArea.insert(ui.END, '');
            self.append_to_text(''); # Buffer.
            self.isInitialized=True;
            self.refresh();
            self.startSession(startCmd);
            self.addEventListeners();
            self.master.update();
        ##endif
    ##end
    def startSession(self,startCmd=''):
        print('I am session');
        if (startCmd!='' and startCmd!=' '):
            self.type_str(startCmd);
            self.run_cmd(startCmd,self.mainTextArea.size());
        ##endif
        self.curr_text=f'{self.path}> '; #Initialize the terminal with the correct string.
        self.type_str(self.curr_text);
        self.master.update();
    ##end
    def addEventListeners(self):
        self.scrollbar.config(command=self.mainTextArea.yview);
        self.mainTextArea.config(yscrollcommand=self.scrollbar.set);
        self.addKeypressListeners();
        self.master.update();
    ##end
    def addKeypressListeners(self):
        global terminal_listbox;
        terminal_listbox=self.mainTextArea;
        for key,func in self.Keybinds.items():
            if (key!=None and func!=None):
                terminal_listbox.bind(key, func);
            ##endif
        ##end
        self.master.update();
    ##end
    def clear_text(self):
        self.mainTextArea.delete(0,ui.END);
    ##end
##end