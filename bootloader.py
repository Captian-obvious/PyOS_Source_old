import PyOS.MainExe as main;
import os,sys;
sys.path.append('PyOS');
sys.path.append('PyOS/Modules');
#check for conflicts

#Check configuration and if not found create it.
if (not os.path.exists('PyOS')):
    os.mkdir('PyOS');
    if (not os.path.exists('PyOS/Modules')):
        os.mkdir('PyOS/Modules');
    ##endif
    if (not os.path.exists('PyOS/cfg')):
        os.mkdir('PyOS/cfg');
    ##endif
    if (not os.path.exists('PyOS/.lib')):
        os.mkdir('PyOS/.lib');
    ##endif
##endif

if (__name__=="__main__"):
    #Initialize and load the main executable.
    main.init();
    main.load();
##endif
