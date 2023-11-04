## THis project detect the qrcode and then scan using pyzbar libaray and open and close door
###########  Make a virtual environment and run code   is best way    
from imutils.video import VideoStream    ### for video stream 
from pyzbar import pyzbar   #    for qr code decoder
import argparse      #   for argument passa i
import datetime
import imutils  #  for image resize     
import time
import cv2
import  RPi.GPIO as GPIO   #  for gpio pins 
#######################################################
lock= 27     #   gpio pin 27 number is used     for lock   
GPIO.setmode(GPIO.BCM)       # bcm mode is used   
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)    #   button is attached in  pull up configration
GPIO.setup(lock,GPIO.OUT)   #         define lock as  output  
GPIO.output(lock,GPIO.HIGH); #   i have used optocoupler relay so it operate on LOW signal     
inputValue = GPIO.input(17);   #   sensor or button attached here 
ap = argparse.ArgumentParser()   #   argument passing  
ap.add_argument("-o", "--output", type=str, default="qrcodes.csv",
help="")   #   create the qrcodes.csv and also output type 
args = vars(ap.parse_args())                                                               
cam = VideoStream(usePiCamera=True).start() # For Pi Camera
c=0;
time.sleep(2.0)
n=2;
csv = open(args["output"], "w")    #    now open the csv file to write or store data of time,date ,qrc ode information 
found = set()          #    found is variable used below to check whether the file is empty or not
while True:
    
    if(inputValue==False):
        print("Other Mode1");# loop for taking frames continusly 
        frame = cam.read()   #    read camera and save it in variable frame 
        inputValue = GPIO.input(17);    #    raed the button   attached on pin 17
        frame = imutils.resize(frame, width=400)    #     as imutils libaray used for image resize so that it will display on screen 
        qrcodes = pyzbar.decode(frame)  #   frame ae proceeesed   using pyzbar libaray and decode the value it automatically check if its qrcode or not   
        print("Please Scan Code ...........");
        for qrcode in qrcodes:  #  now check each paramter in qrcodes variable extract by libaray 
            
            (x, y, w, h) = qrcode.rect    #   NOW LOACATE The qrcode and extract the x,y coordicnates 
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # add rectangle on it using cv2 libaray 
            qrcodeData = qrcode.data.decode("utf-8")   # using uft-8 decode data into readable text foam 
            text = "{}".format(qrcodeData)  # qrcodeData is save in text and then
            print("QR CODE Information ");
            print(text);  # print on terminal    
            ######### apply conditions on string    one is private key and other is public   
            if(text=="roger"):
                print("QR code is correct , Door is open");
                GPIO.output(lock,GPIO.LOW)
                inputValue = GPIO.input(17);
            else:
                print("Please scan correct QR code -- Door close");
                GPIO.output(lock,GPIO.HIGH)
                inputValue = GPIO.input(17);
            ###########################################put text here   colour ,font size and location is define 
            cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # if the qrcodetext is currently not in our CSV file, write
    # the timestamp + qrcodeto disk and update the set
            if qrcodeData not in found:      #   found variable which is call above check if empty or not csv file 
                csv.write("{},{}\n".format(datetime.datetime.now(),
                qrcodeData))    ##  write on  qr code     
                csv.flush()    
                found.add(qrcodeData)     
                cv2.imshow("qrcodeReader", frame)
                print("Code is scanned  ...........");
            if(cv2.waitKey(1) == ord("q")):  ##  if q is pressed break the loop   
                break
    if (inputValue==True):
        print("Other Mode2");
        inputValue = GPIO.input(17);  
            
print("ended  Thankyou ...")
csv.close()
cv2.destroyAllWindows()
cam.stop()
