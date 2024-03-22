import PyOS.Filesystem as fs;
import PyOS.LinuxUtils as linux;
import PyOS.programs.Clock as clk;
import PyOS.WiM as wm;
import PyOS.UI as ui;
import PyOS.Pointer as pt;

main=ui.UI_CustomWindow();
main.setAttribute('fullscreen',True);
main.setAttribute('topmost',False);
main.config(background="#333");
scr_w=main.winfo_width();
scr_h=main.winfo_height();
LoadMessage=ui.UI_Label(main,text='...',fg="#fff",bg="#333",font=('Roboto Mono',20),height=2);
LoadImg=ui.UI_Label(main,fg="#fff",bg="#333",font=('Roboto Mono',20));
LoadImg.setImg(linux.get_pwd()+'/PyOS/OS_Resources/PyOS_Logo.png');
LoadImg.place(relx=.5,rely=.5,width='128px',height='128px',anchor=ui.CENTER);
LoadMessage.pack(expand=1,fill=ui.X,anchor='s');
#Gets around race conditions like the import speed or loading of libs.

def loadScr():
    global main;
    count=0;
    for i in range(0,30):
        count=count+1;
        if (count>3):
            count=1;
        ##endif
        ct="."*count;
        LoadMessage.setText(f'{ct}Loading{ct}');
        linux.time.sleep(.3);
        main.update();
    ##end
##end
def init():
    global main;
    #Start the loading sequence.
    loadScr();
    #Only time the smartscan is important is on first startup, after which the filesystem takes over.
    def onprogress(percent):
        LoadMessage.setText(f'Scanning Files... {percent}%');
        main.update();
    ##end
    if (not fs.path_exists(linux.get_pwd()+'/PyOS/smartscan.log')):
        success=fs.disk_scan(onprogress);
        if (success):
            startSessionAfterInit();
        else:
            panic('Unable to complete SmartScan Disk Scan. Boot failure.');
        ##endif
    else:
        #Directly start the session.
        startSessionAfterInit();
    ##endif
##end
def load():
    pass;
##end
def startSessionAfterInit():
    global main;
    LoadMessage.destroy();
    LoadImg.destroy();
    main.update();
    #Load the main window.
    if (fs.path_exists('PyOS/cfg/main.bin')):
        #Instantly initialize the main event driven part if main.bin exists.
        initializeDesktop(False,linux.jsonDecode(linux.sys_read('PyOS/cfg/main.bin').decode('utf-8')));
        main.mainloop();
    else:
        #Otherwise, create the file and initialize the installer.
        initializeInstaller();
        main.mainloop();
    ##endif
##end
def bindFn(fn,*args,**kwargs):
    def nfn(*args2,**kwargs2):
        return fn(*args,*args2,**kwargs,**kwargs2);
    ##end
    return nfn;
##end
def interpolate_color(start_color, end_color, t):
    # Linear interpolation between start_color and end_color
    r = int((1-t) * start_color[0] + t * end_color[0]);
    g = int((1-t) * start_color[1] + t * end_color[1]);
    b = int((1-t) * start_color[2] + t * end_color[2]);
    return r,g,b;
##end
def rgbtohex(r,g,b):
    return f"#{r:02x}{g:02x}{b:02x}";
##end
def initializeInstaller():
    global main;
    #Create the installer window.
    cfg={};
    cfg['users']=[];
    inst_win=ui.UI_Frame(main,bg="#eee");
    inst_win.place(relx=.5,rely=.5,relheight=.7,relwidth=.4,anchor=ui.CENTER);
    if (main.winfo_screenwidth()<800):
        inst_win.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
    ##endif
    def on_inst_win_configure(ev):
        if (main.winfo_screenwidth()<800):
            inst_win.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
        else:
            inst_win.place(relx=.5,rely=.5,relheight=.7,relwidth=.4,anchor=ui.CENTER);
        ##endif
    ##end
    main.bind('<Configure>',on_inst_win_configure);
    inst_win_p1=ui.UI_Frame(inst_win,bg="#eee");
    inst_win_p1.place(rely=0,relheight=1,relwidth=1);
    inst_win_p2=ui.UI_Frame(inst_win,bg="#eee");
    inst_win1_title=ui.UI_Label(inst_win_p1,text='PyOS Installer',bg="#eee",font=('Roboto Mono',10));
    inst_win1_title.place(rely=0,relheight=.1,relwidth=1);
    inst_win2_title=ui.UI_Label(inst_win_p2,text='PyOS Installer',bg="#eee",font=('Roboto Mono',10));
    inst_win2_title.place(rely=0,relheight=.1,relwidth=1);
    var1=ui.tk.IntVar(inst_win,0);
    var2=ui.tk.IntVar(inst_win,0);
    var3=ui.tk.IntVar(inst_win,1);
    var4=ui.tk.IntVar(inst_win,0);
    var5=ui.tk.IntVar(inst_win,0);
    var6=ui.tk.IntVar(inst_win,0);
    var7=ui.tk.IntVar(inst_win,0);
    var8=ui.tk.StringVar(inst_win,'');
    var9=ui.tk.StringVar(inst_win,'');
    var10=ui.tk.IntVar(inst_win,0);
    chk_pnp=ui.UI_Checkbutton(inst_win_p1,text='Auto Detect Plug \'n play devices (Not Recommended)',font=('Roboto Mono',10),bg="#eee",variable=var1);
    chk_pnp.place(rely=.1,relheight=.1,relwidth=1);
    smartscan_cb=ui.UI_Checkbutton(inst_win_p1,text='Automatically Scan with SmartScan after install.',font=('Roboto Mono',10),bg="#eee",variable=var2);
    smartscan_cb.place(rely=.2,relheight=.1,relwidth=1);
    try_pyos_button=ui.UI_Button(inst_win_p1,text='Try PyOS (will ask to install again after reboot)',font=('Roboto Mono',10));
    try_pyos_button.place(relx=0,rely=.3,relheight=.7,relwidth=.5);
    inst_pyos_button=ui.UI_Button(inst_win_p1,text='Install PyOS to local disk',font=('Roboto Mono',10));
    inst_pyos_button.place(relx=0.5,rely=.3,relheight=.7,relwidth=.5);
    def on_try_pyos_button_click():
        try_pyos_button.config(bg='#eee');
        inst_pyos_button.config(bg='#aaa');
        main.update();
        var3.set(0);
    ##end
    def on_inst_pyos_button_click():
        try_pyos_button.config(bg='#aaa');
        inst_pyos_button.config(bg='#eee');
        main.update();
        var3.set(1);
    ##end
    try_pyos_button.setCommand(bindFn(on_try_pyos_button_click));
    inst_pyos_button.setCommand(bindFn(on_inst_pyos_button_click));
    inst_root_cb=ui.UI_Checkbutton(inst_win_p2,text='Install to root directory. (Recommended)' if linux.os.access('/',linux.os.R_OK) else 'Install to root directory. (Not Recommended)',font=('Roboto Mono',10),bg="#eee",variable=var4);
    inst_root_cb.place(rely=.1,relheight=.1,relwidth=1);
    inst_dir_ent=ui.UI_Entry(inst_win_p2,font=('Roboto Mono',10),bg="#eee");
    en_root_user_cb=ui.UI_Checkbutton(inst_win_p2,text='Enable root user. (Recommended)',font=('Roboto Mono',10),bg="#eee",variable=var5);
    en_root_user_cb.place(rely=.3,relheight=.1,relwidth=1);
    inst_py_int=ui.UI_Checkbutton(inst_win_p2,text='Install python interpreter.',font=('Roboto Mono',10),bg="#eee",variable=var6);
    inst_py_int.place(rely=.4,relheight=.1,relwidth=1);
    cont_button=ui.UI_Button(inst_win_p1,text='Continue',font=('Roboto Mono',20));
    cont_button.place(rely=.9,relheight=.1,relwidth=1);
    def cont_button_cmd():
        print('user clicked next');
        inst_win_p2.place(rely=0,relheight=1,relwidth=1);
        inst_win_p1.place_forget();
        if (var3.get()==0):
            return initializeDesktop(True);
        ##endif
    ##end
    cont_button.setCommand(bindFn(cont_button_cmd));
    auto_register_cb=ui.UI_Checkbutton(inst_win_p2,text="Automatically register home user.",font=('Roboto Mono',10),bg="#eee",variable=var7);
    auto_register_cb.place(rely=.5,relheight=.1,relwidth=1);
    home_usr_name_ent=ui.tk.Entry(inst_win_p2,font=('Roboto Mono',10),bg="#eee",textvariable=var8,show='*');
    home_usr_name_ent.place(rely=.6,relheight=.2,relwidth=1);
    home_usr_pw_ent=ui.tk.Entry(inst_win_p2,font=('Roboto Mono',10),bg="#eee",textvariable=var9,show='*');
    home_usr_pw_ent.place(rely=.7,relheight=.2,relwidth=1);
    log_all_cb=ui.UI_Checkbutton(inst_win_p2,text="Log boot record. (Not Recommended for low SSD/HDD sizes)",font=('Roboto Mono',10),bg="#eee",variable=var10);
    log_all_cb.place(rely=.8,relheight=.1,relwidth=1);
    no_match_err=ui.UI_Label(inst_win_p2,text='Passwords do not match.',fg="#f00",bg="#eee",font=('Roboto Mono',10));
    inst_button=ui.UI_Button(inst_win_p2,text='Install',font=('Roboto Mono',20));
    inst_button.place(rely=.9,relheight=.1,relwidth=0.5);
    sd_button=ui.UI_Button(inst_win_p2,text='Cancel',font=('Roboto Mono',20));
    sd_button.place(relx=.5,rely=.9,relheight=.1,relwidth=0.5);
    def inst_dir_ent_cb(s):
        global inst_win;
        if (var4.get()==0):
            s.place(rely=.2,relheight=.1,relwidth=1);
            en_root_user_cb.place(rely=.3,relheight=.1,relwidth=1);
            inst_py_int.place(rely=.4,relheight=.1,relwidth=1);
            auto_register_cb.place(rely=.5,relheight=.1,relwidth=1);
            home_usr_name_ent.place(rely=.6,relheight=.1,relwidth=1);
            home_usr_pw_ent.place(rely=.7,relheight=.1,relwidth=1);
        else:
            s.place_forget();
            en_root_user_cb.place(rely=.2,relheight=.1,relwidth=1);
            inst_py_int.place(rely=.3,relheight=.1,relwidth=1);
            auto_register_cb.place(rely=.4,relheight=.1,relwidth=1);
            home_usr_name_ent.place(rely=.5,relheight=.15,relwidth=1);
            home_usr_pw_ent.place(rely=.65,relheight=.15,relwidth=1);
        ##endif
    ##end
    def inst_button_cmd():
        print('user clicked install');
        if (var4.get()==1):
            cfg['root_install']=True;
        else:
            cfg['root_install']=False;
            cfg['install_dir']=inst_dir_ent.get();
        ##endif
        if (var5.get()==1):
            cfg['root_user_enabled']=True;
        else:
            cfg['root_user_enabled']=False;
        ##endif
        if (var6.get()==1):
            cfg['auto_install_python']=True;
        else:
            cfg['auto_install_python']=False;
        ##endif
        if (var7.get()==1):
            cfg['register_on_boot']=True;
        else:
            cfg['register_on_boot']=False;
        ##endif
        if (var8.get()==var9.get()):
            cfg['root_user_password']=obfescate(var8.get());
        else:
            print('passwords do not match');
            no_match_err.place(rely=.9,relheight=.1,relwidth=1);
            inst_button.place_forget()
            sd_button.place_forget();
            main.update();
            linux.time.sleep(1);
            no_match_err.place_forget();
            inst_button.place(relx=0,rely=.9,relheight=.1,relwidth=1);
            sd_button.place(relx=.5,rely=.9,relheight=.1,relwidth=.5);
            main.update();
            return;
        ##endif
        if (var10.get()==1):
            cfg['log_all_boots']=True;
        else:
            cfg['log_all_boots']=False;
        ##endif
        inst_win_p2.place_forget();
        main.unbind('<Configure>');
        inst_win.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
        main.update();
        handleOSInstall(cfg,inst_win);
    ##end
    def sd_button_cmd():
        print('user clicked cancel, shutting down...');
        quit(); #for now it just calls quit.
    ##end
    inst_root_cb.config(command=bindFn(inst_dir_ent_cb,inst_dir_ent));
    inst_button.setCommand(bindFn(inst_button_cmd));
    sd_button.setCommand(bindFn(sd_button_cmd));
    main.update();
##end
def checkUsrs(usrTable,usr):
    res=None;
    for i in range(1,len(usrTable)):
        if (usrTable[i-1]['username']==usr):
            res=usrTable[i-1];
            break;
        ##endif
    ##end
    return res;
##end
def login(usrTable,usr,pw):
    res=None;
    for i in range(1,len(usrTable)):
        if (usrTable[i-1]['username']==usr and usrTable['password']==pw):
            res=usrTable[i-1];
            break;
        ##endif
    ##end
    return res;
##end
def initializeUserPage(win:ui.UI_CustomWindow|ui.UI_Window,cfg:dict,gdcallback=None):
    global main,usr_name_id,user,cur;
    usr_name_id=None;
    usrTable=cfg['users'];
    #print(usrTable);
    centerX=win.winfo_width()/2;
    centerY=win.winfo_height()/2;
    cur=0;
    user=usrTable[cur];
    usr_frame=ui.tk.Canvas(win,bg=cfg['noimg_background'] or '#333',height=win.winfo_height(),width=win.winfo_width());
    usr_frame.place(relheight=1,relwidth=1);
    create_bg_img(win,usr_frame,'PyOS/assets/background.png');
    prof_pic=ui.UI_CustomLabel(usr_frame,text='',fg_color='#555',corner_radius=360,height=48,width=48);
    usr_frame.create_window(centerX,centerY,window=prof_pic,anchor=ui.CENTER);
    prof_pic.place(relx=.5,rely=.35,anchor=ui.CENTER);
    def drawPage(usr):
        global usr_name_id;
        if (usr_name_id):
            usr_frame.delete(usr_name_id);
        ##endif
        prof_pic.setImg(usr['prof_pic'],True);
        usr_name_id=usr_frame.create_text(centerX,centerY,text=linux.usrndecode(usr['username']).decode('utf-8'),fill='#fff',font=('Roboto Mono',30) if win.winfo_height()>400 else ('Roboto Mono',15));
    ##end
    drawPage(user);
    pw_ent=ui.UI_Entry(usr_frame,show='*',font=('Roboto Mono',15) if win.winfo_height()>400 else ('Roboto Mono',10),justify=ui.tk.LEFT);
    usr_frame.create_window(centerX,centerY,window=pw_ent,anchor=ui.CENTER);
    pw_ent.place(relx=.4 if main.winfo_screenwidth()>600 else .35,rely=.55,relheight=.05,relwidth=.20 if main.winfo_screenwidth()>600 else .25,anchor=ui.tk.NW);
    etr_btn=ui.UI_CustomButton(usr_frame,text='>',text_color='#fff',fg_color='#555',corner_radius=360,font=('Roboto Mono',15) if win.winfo_height()>400 else ('Roboto Mono',10));
    usr_frame.create_window(centerX,centerY,window=etr_btn,anchor=ui.CENTER);
    etr_btn.place(relx=.55 if main.winfo_screenwidth()>600 else .6,rely=.55,relheight=.05,relwidth=.05,anchor=ui.tk.NW);
    nxt_btn=ui.UI_CustomButton(usr_frame,text='>',text_color='#fff',fg_color='#555',corner_radius=360,font=('Roboto Mono',15) if win.winfo_height()>400 else ('Roboto Mono',5));
    usr_frame.create_window(centerX,centerY,window=nxt_btn,anchor=ui.CENTER);
    nxt_btn.place(relx=.95,rely=.5,relheight=.1,relwidth=.05,anchor=ui.E);
    prv_btn=ui.UI_CustomButton(usr_frame,text='<',text_color='#fff',fg_color='#555',corner_radius=360,font=('Roboto Mono',15) if win.winfo_height()>400 else ('Roboto Mono',5));
    usr_frame.create_window(centerX,centerY,window=prv_btn,anchor=ui.CENTER);
    prv_btn.place(relx=.05,rely=.5,relheight=.1,relwidth=.05,anchor=ui.W);
    incorrect_cred=usr_frame.create_text(centerX,centerY+100,text='Incorrect password.',font=('Roboto Mono',10),fill='#f00');
    usr_frame.itemconfigure(incorrect_cred,state=ui.tk.HIDDEN);
    no_pw_err=usr_frame.create_text(centerX,centerY+100,text='Please type a password.',font=('Roboto Mono',10),fill='#f00');
    usr_frame.itemconfigure(no_pw_err,state=ui.tk.HIDDEN);
    def etr_btn_cmd():
        global user;
        print('user clicked enter');
        usr_frame.itemconfigure(incorrect_cred,state=ui.tk.HIDDEN);
        usr_frame.itemconfigure(no_pw_err,state=ui.tk.HIDDEN);
        if (pw_ent.get()==''):
            usr_frame.itemconfigure(no_pw_err,state=ui.tk.NORMAL);
            return;
        elif (obfescate(pw_ent.get())!=user['password']):
            usr_frame.itemconfigure(incorrect_cred,state=ui.tk.NORMAL);
            return;
        ##endif
        print('user entered correct password');
        usr_frame.place_forget();
        if (gdcallback):gdcallback();
        ##endif
        return;
    ##end
    def nxt_btn_cmd():
        global user,cur;
        print('user clicked next user');
        if (cur+1>len(usrTable)):
            print('user is last user')
            return;
        ##endif
        print('switching users');
        user=usrTable[cur+1];
        drawPage(user);
        cur+=1;
        return;
    ##end
    def prv_btn_cmd():
        global user,cur;
        print('user clicked previous user');
        if (cur-1<0):
            print('user is first user');
            return;
        ##endif
        print('switching users');
        user=usrTable[cur-1];
        drawPage(user);
        cur-=1;
        return;
    ##end
    etr_btn.setCommand(bindFn(etr_btn_cmd));
    nxt_btn.setCommand(bindFn(nxt_btn_cmd));
    prv_btn.setCommand(bindFn(prv_btn_cmd));
    #Add Person button.
    add_person_btn=ui.UI_CustomButton(usr_frame,text='Add Person',text_color='#fff',corner_radius=360,fg_color='#555',font=('Roboto Mono',10) if win.winfo_height()>400 else ('Roboto Mono',6));
    def add_person(cfg):
        print('user clicked add person');
        ap_win=ui.UI_CustomFrame(usr_frame,fg_color=cfg['noimg_background'] or '#333',width=300,height=300,corner_radius=20);
        var1=ui.tk.StringVar(ap_win,value='');
        var2=ui.tk.StringVar(ap_win,value='');
        var3=ui.tk.StringVar(ap_win,value='');
        var4=ui.tk.IntVar(ap_win,value=0);
        var5=ui.tk.IntVar(ap_win,value=0);
        var6=ui.tk.IntVar(ap_win,value=0);
        usr_frame.create_window(centerX,centerY,window=ap_win,anchor=ui.CENTER);
        ap_win.place(relx=.5,rely=.5,anchor=ui.CENTER);
        ap_win_p1=ui.UI_CustomFrame(ap_win,fg_color=cfg['noimg_background'] or '#333',corner_radius=20);
        ap_win_p1.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
        ap_win_p2=ui.UI_CustomFrame(ap_win,fg_color=cfg['noimg_background'] or '#333',corner_radius=20);
        ap_win_p1_title=ui.UI_CustomLabel(ap_win_p1,text='Add Person',font=('Roboto Mono',8),corner_radius=20,fg_color=cfg['noimg_background'] or '#333',text_color='#fff',justify=ui.tk.LEFT);
        ap_win_p1_title.place(relx=.5,relheight=.05,relwidth=1,anchor=ui.N);
        ap_win_p2_title=ui.UI_CustomLabel(ap_win_p1,text='Add Person',font=('Roboto Mono',8),corner_radius=20,fg_color=cfg['noimg_background'] or '#333',text_color='#fff',justify=ui.tk.LEFT);
        ap_win_p2_title.place(relx=.5,relheight=.05,relwidth=1,anchor=ui.N);
        ap_msg=ui.UI_CustomLabel(ap_win_p1,text='To continue, authorization is required. Please enter your credentials',font=('Roboto Mono',8),corner_radius=20,fg_color=cfg['noimg_background'] or '#333',text_color='#fff',justify=ui.tk.LEFT);
        ap_msg.place(relx=.5,rely=.05,relheight=.1,relwidth=1,anchor=ui.N)
        ap_name=ui.UI_CustomLabel(ap_win_p1,text='Username:',font=('Roboto Mono',8),fg_color=cfg['noimg_background'] or '#333',text_color='#fff',justify=ui.tk.LEFT);
        ap_name.place(relx=.5,rely=.15,relheight=.05,relwidth=.8,anchor=ui.N);
        ap_name_ent=ui.UI_CustomEntry(ap_win_p1,font=('Roboto Mono',10),textvariable=var1,fg_color=cfg['noimg_background'] or '#333',text_color='#fff',corner_radius=20);
        ap_name_ent.place(relx=.5,rely=.25,relheight=.1,relwidth=.8,anchor=ui.N);
        ap_pw=ui.UI_CustomLabel(ap_win_p1,text='Password:',font=('Roboto Mono',8),fg_color=cfg['noimg_background'] or '#333',text_color='#fff',justify=ui.tk.LEFT);
        ap_pw.place(relx=.5,rely=.35,relheight=.05,relwidth=.8,anchor=ui.N);
        ap_pw_ent=ui.UI_CustomEntry(ap_win_p1,font=('Roboto Mono',10),textvariable=var2,fg_color=cfg['noimg_background'] or '#333',text_color='#fff',corner_radius=20,show="*");
        ap_name_ent.bind('<Return>',lambda e: ap_pw_ent.focus_set());
        ap_pw_ent.place(relx=.5,rely=.45,relheight=.1,relwidth=.8,anchor=ui.N);
        ap_pw2=ui.UI_CustomLabel(ap_win_p1,text='Confirm Password:',font=('Roboto Mono',8),fg_color=cfg['noimg_background'] or '#333',text_color='#fff',justify=ui.tk.LEFT);
        ap_pw2.place(relx=.5,rely=.55,relheight=.05,relwidth=.8,anchor=ui.N);
        ap_pw2_ent=ui.UI_CustomEntry(ap_win_p1,font=('Roboto Mono',10),textvariable=var3,fg_color=cfg['noimg_background'] or '#333',text_color='#fff',corner_radius=20,show="*");
        ap_pw2_ent.place(relx=.5,rely=.65,relheight=.1,relwidth=.8,anchor=ui.N);
        ap_pw_ent.bind('<Return>',lambda e: ap_pw2_ent.focus_set());
        ap_use=ui.UI_Checkbutton(ap_win_p1,text='Allow other users of this device to use this account?',variable=var4,bg=cfg['noimg_background'] or '#333',fg='#fff',font=('Roboto Mono',6),justify=ui.tk.LEFT);
        ap_use.place(relx=.5,rely=.75,relheight=.1,relwidth=.8,anchor=ui.N);
        ap_nxt_btn=ui.UI_CustomButton(ap_win_p1,text='Next',text_color='#fff',corner_radius=20,fg_color=cfg['noimg_background'] or '#333',font=('Roboto Mono',8));
        ap_nxt_btn.place(relx=.5,rely=.85,relheight=.15,relwidth=.5);
        ap_cancel_btn=ui.UI_CustomButton(ap_win_p1,text='Cancel',text_color='#fff',corner_radius=20,fg_color=cfg['noimg_background'] or '#333',font=('Roboto Mono',8));
        ap_cancel_btn.place(relx=0,rely=.85,relheight=.15,relwidth=.5);
        ap_msg2=ui.UI_CustomLabel(ap_win_p2,text='To create an account, agree to the PyOS Privacy Policy.',text_color="#fff",fg_color=cfg['noimg_background'] or "#333",font=('Roboto Mono',8));
        ap_msg2.place(relx=.5,rely=.05,relheight=.2,relwidth=1,anchor=ui.N);
        ap_privacy_cb=ui.UI_Checkbutton(ap_win_p2,text='I have read and agree to the Privacy Policy.',variable=var5,fg="#fff",bg=cfg['noimg_background'] or "#333",font=('Roboto Mono',8));
        ap_privacy_cb.place(relx=.5,rely=.25,relheight=.3,relwidth=.8,anchor=ui.N);
        ap_isActivated=ui.UI_Checkbutton(ap_win_p2,text='Enable debugging features?',variable=var6,fg="#fff",bg=cfg['noimg_background'] or "#333",font=('Roboto Mono',8));
        ap_isActivated.place(relx=.5,rely=.55,relheight=.3,relwidth=.8,anchor=ui.N);
        ap_create_btn=ui.UI_CustomButton(ap_win_p2,text='Create Account',text_color='#fff',corner_radius=20,fg_color=cfg['noimg_background'] or '#333',font=('Roboto Mono',8));
        ap_create_btn.place(relx=.5,rely=.85,relheight=.15,relwidth=.4);
        ap_cancel_btn2=ui.UI_CustomButton(ap_win_p2,text='Cancel',text_color='#fff',corner_radius=20,fg_color=cfg['noimg_background'] or '#333',font=('Roboto Mono',8));
        ap_cancel_btn2.place(relx=.1,rely=.85,relheight=.15,relwidth=.4);
        ap_usrn_err=ui.UI_CustomLabel(ap_win_p1,text='Please enter a username.',font=('Roboto Mono',8),fg_color=cfg['noimg_background'] or '#333',text_color='#f00',justify=ui.tk.LEFT);
        ap_nopw_err=ui.UI_CustomLabel(ap_win_p1,text='Please enter a password.',font=('Roboto Mono',8),fg_color=cfg['noimg_background'] or '#333',text_color='#f00',justify=ui.tk.LEFT);
        ap_pw_err=ui.UI_CustomLabel(ap_win_p1,text='Passwords do not match.',font=('Roboto Mono',8),fg_color=cfg['noimg_background'] or '#333',text_color='#f00',justify=ui.tk.LEFT);
        ap_ag_err=ui.UI_CustomLabel(ap_win_p1,text='Please agree to the Privacy Policy.',font=('Roboto Mono',8),fg_color=cfg['noimg_background'] or '#333',text_color='#f00',justify=ui.tk.LEFT);

        def ap_nxt_btn_cmd():
            print('user clicked next');
            if (var1.get()==''):
                ap_usrn_err.place(relx=.5,rely=.85,relheight=.15,relwidth=1,anchor=ui.N);
                ap_nxt_btn.place_forget();
                ap_cancel_btn.place_forget();
                main.update();
                linux.time.sleep(1);
                ap_nxt_btn.place(relx=.5,rely=.85,relheight=.15,relwidth=.5);
                ap_cancel_btn.place(relx=0,rely=.85,relheight=.15,relwidth=.5);
                ap_usrn_err.place_forget();
                main.update();
                return;
            ##endif
            if (var2.get()==''):
                ap_nopw_err.place(relx=.5,rely=.85,relheight=.15,relwidth=1,anchor=ui.N);
                ap_nxt_btn.place_forget();
                ap_cancel_btn.place_forget();
                main.update();
                linux.time.sleep(1);
                ap_nxt_btn.place(relx=.5,rely=.85,relheight=.15,relwidth=.5);
                ap_cancel_btn.place(relx=0,rely=.85,relheight=.15,relwidth=.5);
                ap_nopw_err.place_forget();
                ap_nxt_btn.place(relx=.5,rely=.85,relheight=.15,relwidth=.5);
                ap_cancel_btn.place(relx=0,rely=.85,relheight=.15,relwidth=.5);
                main.update();
                return;
            ##endif
            if (var2.get()!=var3.get()):
                ap_pw_err.place(relx=.5,rely=.85,relheight=.15,relwidth=1,anchor=ui.N);
                ap_nxt_btn.place_forget();
                ap_cancel_btn.place_forget();
                main.update();
                linux.time.sleep(1);
                ap_nxt_btn.place(relx=.5,rely=.85,relheight=.15,relwidth=.5);
                ap_cancel_btn.place(relx=0,rely=.85,relheight=.15,relwidth=.5);
                ap_pw_err.place_forget();
                main.update();
                return;
            ##endif
            if (var4.get()==0):
                print('user will not be created');
                ap_win.place_forget();
                return;
            ##endif
            print('user will be created');
            ap_win_p2.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
            ap_win_p1.place_forget();
        ##end
        def ap_create_cmd():
            print('user clicked create');
            if (var5.get()==0):
                ap_ag_err.place(relx=.5,rely=.85,relheight=.15,relwidth=1,anchor=ui.N);
                ap_create_btn.place_forget();
                ap_cancel_btn2.place_forget();
                main.update();
                linux.time.sleep(1);
                ap_ag_err.place_forget();
                ap_create_btn.place(relx=.5,rely=.85,relheight=.15,relwidth=.4);
                ap_cancel_btn2.place(relx=.1,rely=.85,relheight=.15,relwidth=.4);
                main.update();
            ##endif
            print('user is being created');
            agree=False;
            isDebug=False;
            if (var5.get()==1):
                agree=True;
            ##endif
            if (var6.get()==1):
                isDebug=True;
            ##endif
            usr={
                "username":obfescate(var1.get(),'un'),
                "password":obfescate(var2.get()),
                "root_user":False,
                "prof_pic":"PyOS/OS_Resources/default_person.svg",
                "agreed":agree,
                "privs": {
                    "debug":isDebug,
                    "root":False,
                },
            };
            cfg['users'].append(usr);
            setf=open('PyOS/cfg/main.bin','wb');
            mainStr=linux.jsonEncode(cfg);
            setf.write(mainStr.encode('utf-8'));
            setf.close();
            print('user created');
            ap_win.place_forget();
            if (gdcallback):gdcallback(usr);
            ##endif
        ##end
        def cancel_call():
            print('user clicked cancel');
            ap_win.place_forget();
        ##end
        ap_nxt_btn.setCommand(bindFn(ap_nxt_btn_cmd));
        ap_create_btn.setCommand(bindFn(ap_create_cmd));
        ap_cancel_btn.setCommand(bindFn(cancel_call));
        ap_cancel_btn2.setCommand(bindFn(cancel_call));
        main.update();
    ##end
    usr_frame.create_window(centerX,centerY+100,window=add_person_btn,anchor=ui.CENTER);
    add_person_btn.setCommand(bindFn(add_person,cfg));
    add_person_btn.place(relx=.02,rely=.98,relheight=.05,relwidth=.15,anchor=ui.tk.SW);
    main.update();
##end
def handleFirstAuth(win:ui.UI_CustomWindow|ui.UI_Window,cfg:dict,gdcallback=None):
    global finished;
    finished=False;
    auth_win=ui.UI_Frame(win,bg="#eee");
    auth_win.place(relx=.5,rely=.5,relheight=.7,relwidth=.4,anchor=ui.CENTER);
    if (win.winfo_screenwidth()<800):
        auth_win.place(relx=.5,rely=.5,relheight=.8,relwidth=.8,anchor=ui.CENTER);
    ##endif
    def on_win_configure(ev):
        if (win.winfo_screenwidth()<800):
            auth_win.place(relx=.5,rely=0.5,relheight=.8,relwidth=.8,anchor=ui.CENTER);
        else:
            auth_win.place(relx=.5,rely=.5,relheight=.8,relwidth=.8,anchor=ui.CENTER);
        ##endif
    ##end
    win.bind('<Configure>',on_win_configure);
    auth_win_p1=ui.UI_Frame(auth_win,bg="#eee");
    auth_win_p1.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER)
    auth_win_p2=ui.UI_Frame(auth_win,bg="#eee");
    auth_win_p3=ui.UI_Frame(auth_win,bg="#eee");
    auth_win_title1=ui.UI_Label(auth_win_p1,text='Authentication',bg="#eee",font=('Roboto Mono',20),justify='left');
    auth_win_title1.place(relx=0,rely=0,relheight=.1,relwidth=.9);
    auth_win_title2=ui.UI_Label(auth_win_p2,text='Authentication',bg="#eee",font=('Roboto Mono',20),justify='left');
    auth_win_title2.place(relx=0,rely=0,relheight=.1,relwidth=.9);
    auth_win_title3=ui.UI_Label(auth_win_p3,text='Authentication',bg="#eee",font=('Roboto Mono',20),justify='left');
    auth_win_title3.place(relx=0,rely=0,relheight=.1,relwidth=.9);
    auth_win_welcome_msg=ui.UI_Label(auth_win_p1,text='Welcome to PyOS.\n To Continue authorization is required.',bg='#eee',font=('Roboto Mono',10),justify='left');
    auth_win_welcome_msg.place(relx=0,rely=.1,relheight=.1,relwidth=1);
    uname_label=ui.UI_Label(auth_win_p1,text='Username:',bg='#eee',font=('Roboto Mono', 10),justify='left');
    uname_label.place(relx=.5,rely=.3,relheight=.1,relwidth=.8,anchor=ui.CENTER);
    uname_entry=ui.UI_Entry(auth_win_p1,font=('Roboto Mono',10),bg="#eee");
    uname_entry.place(relx=.5,rely=.4,relheight=.1,relwidth=.8,anchor=ui.CENTER);
    pw_label=ui.UI_Label(auth_win_p1,text='Password:',bg='#eee',font=('Roboto Mono',10),justify='left');
    pw_label.place(relx=.5,rely=.5,relheight=.1,relwidth=.8,anchor=ui.CENTER);
    pw_entry=ui.UI_Entry(auth_win_p1,font=('Roboto Mono',10),bg="#eee",show='*');
    pw_entry.place(relx=.5,rely=.6,relheight=.1,relwidth=.8,anchor=ui.CENTER);
    pw_label2=ui.UI_Label(auth_win_p1,text='Confirm Password:',bg='#eee',font=('Roboto Mono',10),justify='left');
    pw_label2.place(relx=.5,rely=.7,relheight=.1,relwidth=.8,anchor=ui.CENTER);
    pw_entry2=ui.tk.Entry(auth_win_p1,font=('Roboto Mono',10),bg="#eee",show='*');
    pw_entry2.place(relx=.5,rely=.8,relheight=.1,relwidth=.8,anchor=ui.CENTER);
    no_uname_err=ui.UI_Label(auth_win_p1,text='Username is required.',fg="#f00",bg="#eee",font=('Roboto Mono',10));
    no_pw_err=ui.UI_Label(auth_win_p1,text='Password is required.',fg="#f00",bg="#eee",font=('Roboto Mono',10));
    pw_no_match_err=ui.UI_Label(auth_win_p1,text='Passwords do not match.',fg="#f00",bg="#eee",font=('Roboto Mono',10));
    var1=ui.tk.IntVar(auth_win,0);
    var2=ui.tk.IntVar(auth_win,0);
    all_set_up_msg=ui.UI_Label(auth_win_p3,text='All set up! You can now login',bg="#eee",font=('Roboto Mono',10),justify='left');
    all_set_up_msg.place(relx=0,rely=.1,relheight=.2,relwidth=1);
    allow_discoverable=ui.UI_Label(auth_win_p2,text='Allow this device to be discoverable on the network?',bg="#eee",font=('Roboto Mono',10));
    allow_discoverable.place(rely=.2,relheight=.1,relwidth=1);
    allow_discoverable_cb=ui.UI_Checkbutton(auth_win_p2,text='Allow',font=('Roboto Mono',10),bg="#eee",variable=var1);
    allow_discoverable_cb.place(rely=.3,relheight=.2,relwidth=1);
    agree_to_tos=ui.UI_Label(auth_win_p2,text='By creating a user you agree to the PyOS Privacy Policy.',bg="#eee",font=('Roboto Mono',10));
    agree_to_tos.place(rely=.5,relheight=.1,relwidth=1);
    agree_to_tos_cb=ui.UI_Checkbutton(auth_win_p2,text='I Agree',font=('Roboto Mono',10),bg="#eee",variable=var2);
    agree_to_tos_cb.place(rely=.6,relheight=.2,relwidth=1);
    auth_button=ui.UI_Button(auth_win_p1,text='Next',font=('Roboto Mono',20));
    auth_button.place(relx=.1,rely=.9,relheight=.1,relwidth=.4);
    cancel_button=ui.UI_Button(auth_win_p1,text='Cancel',font=('Roboto Mono',20));
    cancel_button.place(relx=.5,rely=.9,relheight=.1,relwidth=.4);
    finish_btn=ui.UI_Button(auth_win_p2,text='Next',font=('Roboto Mono',20));
    finish_btn.place(relx=.1,rely=.9,relheight=.1,relwidth=.4);
    cancel_btn=ui.UI_Button(auth_win_p2,text='Cancel',font=('Roboto Mono',20));
    cancel_btn.place(relx=.5,rely=.9,relheight=.1,relwidth=.4);
    goto_desktop_btn=ui.UI_Button(auth_win_p3,text='Go to desktop',font=('Roboto Mono',20));
    goto_desktop_btn.place(rely=.3,relheight=.7,relwidth=.5);
    signout_btn=ui.UI_Button(auth_win_p3,text='Sign Out and Shutdown.',font=('Roboto Mono',20));
    signout_btn.place(relx=.5,rely=.3,relheight=.7,relwidth=.5);
    def on_auth_button_click():
        print('user clicked authorize');
        if (uname_entry.get()==''):
            no_uname_err.place(rely=.9,relheight=.1,relwidth=1);
            auth_button.place_forget();
            cancel_button.place_forget();
            uname_entry.focus();
            main.update();
            linux.time.sleep(1);
            no_uname_err.place_forget();
            auth_button.place(relx=.1,rely=.9,relheight=.1,relwidth=.4);
            cancel_button.place(relx=.5,rely=.9,relheight=.1,relwidth=.4);
            main.update();
            return;
        ##endif
        if (pw_entry.get()=='' or pw_entry2.get()==''):
            no_pw_err.place(rely=.9,relheight=.1,relwidth=1);
            auth_button.place_forget();
            cancel_button.place_forget();
            pw_entry.focus();
            main.update();
            linux.time.sleep(1);
            no_pw_err.place_forget();
            auth_button.place(relx=.1,rely=.9,relheight=.1,relwidth=.4);
            cancel_button.place(relx=.5,rely=.9,relheight=.1,relwidth=.4);
            main.update();
            return;
        ##endif
        if (pw_entry.get()!=pw_entry2.get()):
            pw_no_match_err.place(rely=.9,relheight=.1,relwidth=1);
            auth_button.place_forget();
            cancel_button.place_forget();
            pw_entry.focus();
            main.update();
            linux.time.sleep(1);
            pw_no_match_err.place_forget();
            auth_button.place(relx=.1,rely=.9,relheight=.1,relwidth=.4);
            cancel_button.place(relx=.5,rely=.9,relheight=.1,relwidth=.4);
            main.update();
            return;
        ##endif
        if(checkUsrs(cfg['users'],obfescate(uname_entry.get(),'un'))==None):
            cfg['users'].append({
                'username':obfescate(uname_entry.get(),'un'),
                'password':obfescate(pw_entry.get()),
                'root_user':False,
                'prof_pic':'PyOS/OS_Resources/default_person.svg',
                'agreed':True,
                'privs':{
                    "debug":True,
                    "root":False,
                },
            });
        else:
            print('user already exists,logging in.');
            if (login(cfg,obfescate(uname_entry.get(),'un'),obfescate(pw_entry.get()))==None):
                print('incorrect credentials, retry.');
                pw_no_match_err.place(rely=.9,relheight=.1,relwidth=1);
                auth_button.place_forget();
                cancel_button.place_forget();
                pw_entry.focus();
                main.update();
                linux.time.sleep(1);
                pw_no_match_err.place_forget();
                auth_button.place(relx=.1,rely=.9,relheight=.1,relwidth=.4);
                cancel_button.place(relx=.5,rely=.9,relheight=.1,relwidth=.4);
                main.update();
                return;
            ##endif
        ##endif
        auth_win_p1.place_forget();
        auth_win_p2.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
        content=linux.jsonEncode(cfg);
        linux.sys_write(linux.get_pwd()+'/PyOS/cfg/main.bin',content.encode('utf-8'));
        main.update();
    ##end
    def on_finish_btn_click():
        print('user clicked finish');
        auth_win_p2.place_forget();
        auth_win_p3.place(relx=.5,rely=.5,relheight=1,relwidth=1,anchor=ui.CENTER);
        main.update();
        cfg['network_discoverable']=var1.get();
        cfg['agree_to_tos']=var2.get();
    ##end
    def on_cancel_button_click():
        print('user clicked cancel, setup cancelled. Shutting down...');
        quit(); #just calls quit for now.
    ##end
    def on_goto_desktop_click():
        global finished;
        print('user clicked go to desktop, starting environment.');
        finished=True;
        main.update();
        if gdcallback:gdcallback();
        ##endif
    ##end
    def on_signout_click():
        print('user clicked sign out, shutting down...');
        quit(); #just calls quit for now.
    ##end
    auth_button.config(command=bindFn(on_auth_button_click));
    cancel_button.config(command=bindFn(on_cancel_button_click));
    finish_btn.config(command=bindFn(on_finish_btn_click));
    cancel_btn.config(command=bindFn(on_cancel_button_click));
    goto_desktop_btn.config(command=bindFn(on_goto_desktop_click));
    signout_btn.config(command=bindFn(on_signout_click));
    main.update();
##end
#Irreversible obfescation happens here.
def obfescate(s,mode='pw'):
    if mode=='pw':
        bytes=s.encode('utf-8');
        b64bytes=linux.pwencode(bytes);
        b64str=b64bytes.decode('ascii');
        return b64str;
    elif mode=='un':
        bytes=s.encode('utf-8');
        b64bytes=linux.usrnencode(bytes);
        b64str=b64bytes.decode('ascii');
        return b64str;
    ##end
##end
def handleOSInstall(cfg,win:ui.UI_Frame):
    global main,finished;
    finished=False;
    #Initialize the installer window.
    linux.time.sleep(.5);
    win.config(bg="#aaa");
    InstallImage=ui.UI_Label(win,fg="#fff",bg="#aaa",font=('Roboto Mono',20),height=3);
    InstallImage.setImg(linux.get_pwd()+'/PyOS/OS_Resources/PyOS_Logo.png');
    InstallImage.place(relx=.5,rely=.5,height='128px',width='128px',anchor=ui.CENTER);
    InstallMessage=ui.UI_Label(win,text='...',fg='#fff',bg='#aaa',font=('Roboto Mono',20),height=2);
    InstallMessage.pack(expand=1,fill=ui.X,anchor='s');
    def tween():
        start_c=(170,170,170);
        end_c=(51,51,51);
        for i in range(1,30):
            linux.time.sleep(.001);
            t=i/(30)  # Normalize t to [0, 1]
            r,g,b=interpolate_color(start_c,end_c,t);
            hxd=rgbtohex(r,g,b);
            win.config(bg=hxd);
            InstallImage.config(bg=hxd);
            InstallMessage.config(bg=hxd);
            main.update();
        ##end
    ##end
    t1=linux.task.Thread(target=tween);
    t1.start();
    #Begin the install process
    global msgOverride,msgText;
    msgOverride=False;
    msgText='Installing';
    linux.time.sleep(1);
    def installerLoop():
        #installer loop is so user knows that the installer is running.
        global main,finished,msgOverride,msgText;
        count=0;
        while (not finished):
            linux.time.sleep(.3);
            count+=1
            if (count>3):
                count=1;
            ##endif
            ct="."*count;
            newmsg=msgText.replace('...',str(ct));
            if (not msgOverride):
                InstallMessage.setText(f'{ct}Installing{ct}');
            else:
                InstallMessage.setText(newmsg);
            ##endif
            main.update();
        ##end
    ##end
    def install_py_int():
        global main,msgOverride;
        #install python
        msgOverride=True;
        count=0;
        for i in range(1,230):
            linux.time.sleep(.3);
            hxd=linux.math.floor((i/200)*100);
            count+=1;
            if (count>3):
                count=1;
            ##endif
            if (hxd>100):
                hxd=100;
            ##endif
            ct='.'*count;
            InstallMessage.setText(f'Installing Python Interpreter{ct} {hxd}%');
            main.update();
        ##end
        msgOverride=False;
    ##end
    def install_root_setup():
        global main,msgOverride,msgText;
        msgOverride=True;
        #This is essentially an update menu, automatically updates root env.
        #first step of install
        updAvailable=True;
        #gets around command race conditions
        count=0;
        def cmdFunc():
            linux.sys_run('mkdir -p $0/PyOS/.lib/bin');
            linux.sys_run('mkdir -p $0/PyOS/.lib/bin/.boot');
            linux.sys_run('mkdir -p $0/PyOS/.lib/.os');
            linux.sys_run('mkdir -p $0/PyOS/.lib/.os/boot');
            linux.sys_run('cd $0/PyOS/.lib/.os/boot');
            linux.sys_run('mkdir .cache');
        ##end
        cmdThread=linux.task.Thread(target=cmdFunc);
        cmdThread.start();
        for i in range(1,330):
            linux.time.sleep(.3);
            hxd=linux.math.floor((i/300)*100);
            count+=1;
            if (count>3):
                count=1;
            ##endif
            if (hxd>100):
                hxd=100;
            ##endif
            ct='.'*count;
            InstallMessage.setText(f'Setting up root environment{ct} {hxd}%');
            main.update();
        ##end
        if (updAvailable):
            #update the environment.
            #linux.run_command('apt upgrade');
            count=0;
            for i in range(1,630):
                linux.time.sleep(.3);
                hxd=linux.math.floor((i/600)*100);
                count+=1
                if(count>3):
                    count=1;
                ##endif
                if (hxd>100):
                    hxd=100;
                ##endif
                ct='.'*count;
                InstallMessage.setText(f'Updating root environment{ct} {hxd}%');
                main.update();
            ##end
        ##endif
        msgOverride=False;
    ##end
    def install_main_settings():
        global main;
        count=0;
        for i in range(1,310):
            linux.time.sleep(.3);
            hxd=linux.math.floor((i/300)*100);
            count+=1
            if(count>3):
                count=1;
            ##endif
            if (hxd>100):
                hxd=100;
            ##endif
            ct='.'*count;
            InstallMessage.setText(f'Configuring root environment{ct} {hxd}%');
            main.update();
        ##end
        setf=open(linux.get_pwd()+'/PyOS/cfg/main.bin','wb');
        mainstr=linux.jsonEncode(cfg);
        setf.write(mainstr.encode('utf-8'));
        setf.close();
    ##end
    install_root_setup();
    if (cfg['auto_install_python']==True):
        #Probably the fastest part of the install.
        install_py_int();
    ##endif
    #installs main settings last as everything else has to finish beforehand.
    install_main_settings();
    count=0;
    for i in range(1,430):
        linux.time.sleep(.3);
        hxd=linux.math.floor((i/400)*100);
        count+=1
        if(count>3):
            count=1;
        ##endif
        if (hxd>100):
            hxd=100;
        ##endif
        ct='.'*count;
        InstallMessage.setText(f'Finalizing Install{ct} {hxd}%');
        main.update();
    ##end
    finished=True;
    InstallMessage.setText('Install Complete, Enjoy PyOS! :)');
    main.update();
    linux.time.sleep(1);
    def tween2():
        start_c=(51,51,51);
        end_c=(0,0,0);
        for i in range(1,20):
            linux.time.sleep(.001);
            t=i/(30)  # Normalize t to [0, 1]
            r,g,b=interpolate_color(start_c,end_c,t);
            hxd=rgbtohex(r,g,b);
            win.config(bg=hxd);
            InstallImage.config(bg=hxd);
            InstallMessage.config(bg=hxd);
            main.update();
        ##end
    ##end
    tween2();
    InstallMessage.destroy();
    InstallImage.destroy();
    return initializeDesktop(True,cfg);
##end
def initializeDesktop(fromInstall=False,cfg=None):
    if (fromInstall==True):
        #This is the first time the user has installed PyOS
        GettingReadyMsg=ui.UI_Label(main,text='We are getting everything ready.',fg='#fff',bg='#333',font=('Roboto Mono',30),height=4);
        GettingReadyMsg.place(relx=.5,rely=.5,relwidth=1,relheight=1,anchor=ui.CENTER);
        def tween():
            start_c=(153,153,153);
            end_c=(51,51,51);
            for i in range(1,200):
                linux.time.sleep(.01);
                t=i/(200)  # Normalize t to [0, 1]
                r,g,b=interpolate_color(start_c,end_c,t);
                hxd=rgbtohex(r,g,b);
                GettingReadyMsg.config(bg=hxd);
                main.update();
            ##end
            for i in range(1,200):
                linux.time.sleep(.01);
                t=i/(200)  # Normalize t to [0, 1]
                r,g,b=interpolate_color(end_c,start_c,t);
                hxd=rgbtohex(r,g,b);
                GettingReadyMsg.config(bg=hxd);
                main.update();
            ##end
        ##end
        tween();
        tween();
        GettingReadyMsg.setText('Just a few more things...')
        tween();
        tween();
        tween();
        tween();
        GettingReadyMsg.setText('PyOS is almost ready..')
        tween();
        tween();
        tween();
        tween();
        GettingReadyMsg.setText('Finishing up...')
        tween();
        tween();
        tween();
        tween();
        GettingReadyMsg.setText('Your PyOS is ready!');
        tween();
        handleFirstAuth(main,cfg,bindFn(goto_desktop,main,cfg));
        GettingReadyMsg.destroy();
        main.update();
        return;
    ##endif
    if (cfg['users']==[]):
        handleFirstAuth(main,cfg,bindFn(goto_desktop,main,cfg));
        main.update();
        return;
    ##endif
    initializeUserPage(main,cfg,bindFn(goto_desktop,main,cfg));
##end
def goto_desktop(main:ui.UI_Window|ui.UI_CustomWindow,cfg:dict):
    print('loading desktop');
    desktop_frame=ui.tk.Canvas(main,bg='#333',height=main.winfo_height(),width=main.winfo_width());
    centerX=main.winfo_width()/2;
    centerY=main.winfo_height()/2;
    create_bg_img(main,desktop_frame,linux.get_pwd()+'/PyOS/assets/background.png');
    desktop_frame.place(relx=0,rely=0,relwidth=1,relheight=1);
    desktop_frame.update();
    taskbar=ui.tk.Canvas(desktop_frame,bg='#333',height=32);
    taskbar.place(relx=0.5,rely=1,relwidth=1,anchor=ui.S);
    #start the clock
    clk.clock.start(main,taskbar);
    #(Replit ignore the 1 request per second, its how the clock heartbeat works)
    dash_btn=ui.UI_Button(taskbar,text='-',fg='#fff',bg='#333',font=('Roboto Mono',15));
    taskbar.create_window(0,0,window=dash_btn,anchor=ui.tk.NW);
    dash_btn.config(height=taskbar.winfo_height(),width=taskbar.winfo_height());
    dash_menu=ui.UI_Frame(desktop_frame,bg='#333');
    desktop_frame.create_window(0,0,window=dash_menu,anchor=ui.tk.SW);
    sidebar=ui.UI_Frame(dash_menu,bg='#333',width=32);
    sidebar.place(relx=0,rely=0,relheight=1);
    searchbar=ui.UI_Frame(dash_menu,bg='#333');
    searchbar.place(relx=.6,rely=0,relheight=0.05 if main.winfo_screenwidth()>400 else .1,relwidth=.8,anchor=ui.N);
    search_entry=ui.UI_Entry(searchbar,fg='#fff',bg='#333',font=('Roboto Mono',10) if main.winfo_screenwidth()>400 else ('Roboto Mono',6));
    search_entry.place(relx=0.1,rely=0.1,relheight=.8,relwidth=.8,anchor=ui.tk.NW);
    def signout(par,cfg):
        print('user clicked sign out, signing out...');
    ##end
    def query(par,cfg,kword):
        print('user clicked query, searching for '+kword);
        if (kword==''):
            return;
        else:
            kword=kword.lower();
            #Firstly, query the programs folder for programs with the keyword inside its name.
            if (kword=='cmd' or kword=='term' or kword=='terminal' or kword=='shell'):
                kword='terminal';
                #display terminal icon as it is the most likely to be searched for in this case
                
            ##endif
        ##endif
        #Then, query the apps folder for apps with the keyword inside its name.
        #and if not found there, query the internet (firefox)
    ##end
    global menu_shown;
    menu_shown=False;
    def on_dash_btn_click(par,cfg,mainf,secf):
        global menu_shown;
        if menu_shown:
            menu_shown=False;
            print('user clicked dash button, hiding menu');
            dash_menu.place_forget();
        else:
            menu_shown=True;
            print('user clicked dash button, showing dash menu.');
            dash_menu.place(y=desktop_frame.winfo_height()-32,relwidth=.3,relheight=.6,anchor=ui.tk.SW);
            
            if (main.winfo_screenwidth()<800):
                dash_menu.place(y=desktop_frame.winfo_height()-32,relwidth=.4,relheight=.8,anchor=ui.tk.SW);
            ##endif
        ##endif
    ##end
    dash_btn.setCommand(bindFn(on_dash_btn_click,main,cfg,desktop_frame,taskbar));
    def create_application_icons():
        #creates the application icons in dash menu
        icon_canvas=ui.UI_Canvas(dash_menu,bg='#777');
        icon_canvas.place(relx=.6,rely=1,relwidth=.8,relheight=.95 if main.winfo_screenwidth()>400 else .9,anchor=ui.tk.S);
        gridsize=(32,32);
        #determine what apps are installed and place them based on grid size
        #(For now it places test patterns)
        for i in range(0,8):
            print('Application placed');
            main.update();
        ##end
    ##end
    create_application_icons();
    py=pt.PyOS_Utils();
    net_int=pt.Network_Utils();
    available=net_int.get_available_networks();
    
    #handle the 'Connections are available' message.
    #This is a temporary message, it will be replaced by a more user friendly message.
    if (len(available)==0):
        print('No internet connection(s) detected.');
    else:
        print('Internet connection(s) detected.');
        
    ##endif
    clk_frame=ui.UI_Frame(desktop_frame,bg='#333');
    net_ico=py.wifi_icon(taskbar,taskbar.winfo_width()-100,taskbar.winfo_height()-6,32,32);
    net_ico.draw(25);
    def on_clock_clicked():
        print('user clicked clock');
        taskbar.tag_unbind('clock','<Button-1>');
        clk.main(clk_frame);
        taskbar.tag_bind('clock','<Button-1>',lambda x: on_clock_clicked());
    ##end
    taskbar.tag_bind('clock','<Button-1>',lambda x: on_clock_clicked());
    main.update();
##end
def panic(msg):
    print(msg);
##end
def create_bg_img(win,cvs,path):
    centerX=win.winfo_width()/2;
    centerY=win.winfo_height()/2;
    width=win.winfo_width();
    cvs.ogn_img=ogn_img=ui.imgReader.open(path);
    aspect_ratio=ogn_img.width/ogn_img.height;
    new_height=int(width/aspect_ratio);
    cvs.bgimg=bgimg=ui.tkImgReader.PhotoImage(ogn_img.resize((width, new_height)));
    cvs.create_image(centerX,centerY,image=bgimg,anchor=ui.CENTER);
##end
def scale_to_width(path,max_width):
    original_image=ui.imgReader.open(path);
    aspect_ratio=original_image.width/original_image.height;
    new_height=int(max_width/aspect_ratio);
    resized_image=original_image.resize((max_width, new_height));
    return resized_image;
##end