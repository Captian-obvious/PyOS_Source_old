from .__init__ import task;
from .__init__ import c;
from .__init__ import lib;
#Load the decoding library
audioSys=lib.LoadLibrary('libAudio.so');

def play_sound(path):
    try:
        decodedArray=audioSys.decode(path);
        audioSys.play_sound(decodedArray);
        return True;
    except audioSys.c_decode_err as e:
        print('An error occured while decoding audio: '+str(e));
        return False;
    ##endtry
##end
