
# Project Aries Controls Team - Hybrid Rocket Engine Control System Ground Station Software
# Under Operations Flow Chart - Rev DEC.17.2017
# Property of The Project Aries Controls Teams and their Affiliates
import tkinter
import tkinter.messagebox
import matplotlib.pyplot as plt
from tkinter import *
from PIL import Image, ImageTk
from threading import Thread
import threading
import time
import os
import serial
import csv
import numpy
from drawnow import *

# Creating empty arrays used for plotting data in MATLAB plots
mission_time=[]
pressurant_pressure=[]
pressurant_temp=[]
oxidizer_pressure=[]
oxidizer_temp=[]
combustion_pressure=[]
filter_data ='' # Holds parsed telemetry array
serial_object = None # Used as handler to serial port
x= 0 # Creating x as a global variable, used to control the infinte loop when disconnect is pressed
plt.ion() # Tells MATLAB to plot live stream

# Create a File in excel with Headers that describe the telemetry
RESULT = ['Mission_time','Temp1', 'Redundant Temp1','Pressure1', 
          'Redundant Pressure1', 'Temp2','Redundant Temp2','Pressure2', 
          'Redundant Pressure2','Temp3','Redundant Temp3', 'Pressure3', 
          'Redundant Pressure3', 'Pressurant_Fill_Indicator', 'Pressurant_Oxidizer_Indicator',
          'Oxidizer_Fill_Indicator','Oxidizer_Combustion_Indicator']

with open("output.csv",'w') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerow(RESULT)

# This function takes the baud rate and comport # that was typed by the user in the entry box on
# the GUI screen and opens a serial port connection.
# The code tries to open the connection, for any reason that the comport can't be open, then this
# function prints an error.
# The error happens during run time for any reason. The person forgets to plug in the
# microntroller for debuggng purposes. Another issues would be the micro controller isn't on
def connect():
    global serial_object
    port = port_entry.get()
    print(port)
    buad = buad_rate.get()
    print(buad)
    try:
        serial_object=serial.Serial('COM' + str(port), buad,timeout=0)

    except ValueError:
        print("Enter Baud and Port")
        return

    get_data()

def makefig():
    plt.subplot(311)
    plt.plot(mission_time,pressurant_pressure,'ro-', label='Pressure (Psi)')
    plt.ticklabel_format(useoffset=False)
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.title('Pressurant Pressure & Temperature')
    plt.xlabel('Mission Time (S)')
    plt.ylabel('Pressure (Psi)')
    plt.legend(loc='upper center')
    plt.grid(True)
    plt2=plt.twinx()
    plt2.plot(mission_time,pressurant_temp,'gx-', label='Temperature (C)')
    plt2.ticklabel_format(useoffset=False)
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.xlabel('Mission Time (s)')
    plt.ylabel('Temperature (C)')
    plt.legend(loc='upper right')

    plt.subplot(312)
    plt.plot(mission_time,oxidizer_pressure,'ro-',label='Pressure (Psi)')
    plt.ticklabel_format(useoffset=False)
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.legend(loc='upper center')
    plt.grid(True)
    plt.title('Oxidizer Pressure & Temperature')
    plt.xlabel('Mission Time (s)')
    plt.ylabel('Pressure (Psi)')

    plt3=plt.twinx()
    plt3.plot(mission_time,oxidizer_temp,'bx-',label='Temperature (C)')
    plt3.ticklabel_format(useoffset=False)
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.legend(loc='upper right')
    plt.xlabel('Mission Time (s)')
    plt.ylabel('Temperature (C)')

    plt.subplot(313)
    plt.plot(mission_time,combustion_pressure,'ro-',label='Pressure (Psi)')
    plt.ticklabel_format(useoffset=False)
    ax = plt.gca()
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.title('Combustion Pressure')
    plt.xlabel('Mission Time (s)')
    plt.ylabel('Pressure (Psi)')
    plt.tight_layout()

def get_data():

    # Update all the labels based on telemetry string
    # 1-Pressurant Tank
    # 2=Oxidizer Tank
    # 3=Combustion Tank
    # Mission_time,Temp1,Redundant Temp1,Pressure1, Redundant Pressure1,
    # Temp2,Redundant Temp2,Pressure2, Redundant Pressure2,
    # Temp3,Redundant Temp3,Pressure3, Redundant Pressure3, ValveInd1,ValveInd2,ValveInd3
    # ValveInd4,ValveInd5,ValveInd6
    global x
    global serial_object
    global filter_data
    i=0
    j=0
    count=0

    while(x==0):
        while (serial_object.inWaiting()==0): # Wait here until there is data
            time.sleep(1)
            pass #do nothing

        try:
            serial_data=serial_object.readline().strip('\n').strip('\r')    
            filter_data = serial_data.split(',')
            print(filter_data)

            if (filter_data):

                # expand the label box to cover old repeated text in x and y directions
                # Data Label 1
                v=StringVar()
                DATALABEL1=Label(root, textvariable=v, width=10)
                DATALABEL1.place(x=175,y=340)
                v.set(filter_data[1])

                # Data Label 2 temp2
                v1=StringVar()
                DATALABEL2=Label(root, textvariable=v1, width=10)
                DATALABEL2.place(x=175,y=360)
                v1.set(filter_data[2])

                # Data Label 3 pressure1
                v2=StringVar()
                DATALABEL3=Label(root, textvariable=v2, width=10)
                DATALABEL3.place(x=175,y=380)
                v2.set(filter_data[3])

                # Data Label 4 pressure2
                v3=StringVar()
                DATALABEL4=Label(root, textvariable=v3, width=10)
                DATALABEL4.place(x=175,y=400)
                v3.set(filter_data[4])

                # Column 2 from the left
                # Data Label 5 temp3
                v4=StringVar()
                DATALABEL5=Label(root, textvariable=v4, width=10)
                DATALABEL5.place(x=275,y=340)
                v4.set(filter_data[5])

                # Data Label 6 temp4
                v5=StringVar()
                DATALABEL6=Label(root, textvariable=v5, width=10)
                DATALABEL6.place(x=275,y=360)
                v5.set(filter_data[6])

                # Data Label 7 pressure3
                v6=StringVar()
                DATALABEL7=Label(root, textvariable=v6, width=10)
                DATALABEL7.place(x=275,y=380)
                v6.set(filter_data[7])

                # Data Label 8 pressure4
                v7=StringVar()
                DATALABEL8=Label(root, textvariable=v7, width=10)
                DATALABEL8.place(x=275,y=400)
                v7.set(filter_data[8])

                #Column 3 from the left
                # Data Label 9 temp5
                v8=StringVar()
                DATALABEL9=Label(root, textvariable=v8, width=10)
                DATALABEL9.place(x=375,y=340)
                v8.set(filter_data[9])

                # Data Label 10 temp6
                v9=StringVar()
                DATALABEL10=Label(root, textvariable=v9, width=10)
                DATALABEL10.place(x=375,y=360)
                v9.set(filter_data[10])

                # Data Label 11 pressure5
                v10=StringVar()
                DATALABEL11=Label(root, textvariable=v10, width=10)
                DATALABEL11.place(x=375,y=380)
                v10.set(filter_data[11])

                # Data Label 12 pressure6
                v11=StringVar()
                DATALABEL12=Label(root, textvariable=v11, width=10)
                DATALABEL12.place(x=375,y=400)
                v11.set(filter_data[12])

                # Column 4 Valves
                # Data Pressurant_Fill Valve Indicator Pressurant_Fill_Indicator
                v12=StringVar()
                DATALABEL13=Label(root, textvariable=v12, width=10)
                DATALABEL13.place(x=815, y=340)
                v12.set(filter_data[13])

                # Data Pressurant_Purge Valve Indicator
                # v13=StringVar()
                # DATALABEL14=Label(root, textvariable=v13)
                # DATALABEL14.place(x=815, y=360)
                # v13.set(filter_data[14])
                # Data Pressurant_Oxidizer Valve Indicator Pressurant_Oxidizer_Indicator
                v14=StringVar()
                DATALABEL15=Label(root, textvariable=v14, width=10)
                DATALABEL15.place(x=815, y=360)
                v14.set(filter_data[14])

                # Data Oxidizer_fill Valve Indicator Oxidizer_Fill_Indicator
                v15=StringVar()
                DATALABEL16=Label(root, textvariable=v15, width=10)
                DATALABEL16.place(x=815, y=380)
                v15.set(filter_data[15])

                # Data Oxidizer_Purge Valve Indicator
                # v16=StringVar()
                # DATALABEL17=Label(root, textvariable=v16)
                # DATALABEL17.place(x=815, y=420)
                # v16.set(filter_data[17])
                # Data Oxi_Combustion Valve Indicator Oxidizer_Combustion_Indicator
                v17=StringVar()
                DATALABEL18=Label(root, textvariable=v17, width=10)
                DATALABEL18.place(x=815, y=400)
                v17.set(filter_data[16])

                # Convert data into numbers
                MissionTime=float(filter_data[0])
                PressurantTemp= float(filter_data[1])
                PressurantPressure = float(filter_data[3])
                OxidizerTemp= float(filter_data[5])
                OxidizerPressure = float(filter_data[7])
                CombustionPressure=float(filter_data[11])

                # Above pressurant pressure Limit
                # Add Color Warnings
                if (PressurantPressure >= 50.0): # 100
                    DATALABEL3.config(bg='red')
                    DATALABEL3.config(fg='white')
                elif ((PressurantPressure >=30) and (PressurantPressure < 50) ):
                    DATALABEL3.config(bg='yellow')
                    DATALABEL3.config(fg='black')
                else:
                    DATALABEL3.config(bg=None)
                    DATALABEL3.config(fg='black')
                if (PressurantTemp >= 40.0):
                    DATALABEL1.config(bg='red')
                    DATALABEL1.config(fg='white')
                elif ((PressurantTemp >=30) and (PressurantTemp < 40) ):
                    DATALABEL1.config(bg='yellow')
                    DATALABEL1.config(fg='black')
                else:
                    DATALABEL1.config(bg= None)
                    DATALABEL1.config(fg='black')
                if (OxidizerPressure >= 50.0):
                    DATALABEL7.config(bg='red')
                    DATALABEL7.config(fg='white')
                elif ((OxidizerPressure >=30) and (OxidizerPressure < 50)):
                    DATALABEL7.config(bg='yellow')
                    DATALABEL7.config(fg='black')
                else:
                    DATALABEL7.config(bg=None)
                    DATALABEL7.config(fg='black')
                if (OxidizerTemp >= 40.0):
                    DATALABEL5.config(bg='red')
                    DATALABEL5.config(fg='white')
                elif ((OxidizerTemp >=30) and (OxidizerTemp < 40) ):
                    DATALABEL5.config(bg='yellow')
                    DATALABEL5.config(fg='black')
                else:
                    DATALABEL5.config(bg=None)
                    DATALABEL5.config(fg='black')

                # Place Data into their respective arrays
                if(count > 5): # Removes old data
                    mission_time.pop(0)
                    pressurant_temp.pop(0)
                    pressurant_pressure.pop(0)
                    oxidizer_temp.pop(0)
                    oxidizer_pressure.pop(0)
                    combustion_pressure.pop(0)
                    mission_time.append(MissionTime)
                    pressurant_temp.append(PressurantTemp)
                    pressurant_pressure.append(PressurantPressure)
                    oxidizer_temp.append(OxidizerTemp)
                    oxidizer_pressure.append(OxidizerPressure)
                    combustion_pressure.append(CombustionPressure)
                    drawnow(makefig)
                    # plt.pause(.5)
                    plt.pause(.0000000000000001)
                    count=count+1

                try:
                    with open("output.csv","a+") as resultFile:
                        wr = csv.writer(resultFile, dialect='excel')
                        wr.writerow(filter_data)

                except:
                    pass
        except:
            pass

def send():
    send_data = data_entry.get()
    if not send_data:
        print("Sent Nothing")

    serial_object.write(send_data)
    print(send_data)

def disconnect():
    global x
    x=1

    try:
        serial_object.close()

    except AttributeError:
        print("Closed without Using it -_-")

    root.destroy()

def open_Pressurant_fill():
    global serial_object
    serial_object.write(b'1')

def close_Pressurant_fill():
    global serial_object
    serial_object.write(b'2')

def open_POIV():
    global serial_object
    serial_object.write(b'3')

def close_POIV():
    global serial_object
    serial_object.write(b'4')

def open_Oxidizer_fill():
    global serial_object
    serial_object.write(b'5')

def close_Oxidizer_fill():
    global serial_object
    serial_object.write(b'6')
 
def launch():
    global serial_object
    serial_object.write(b'7')

def Abort():
    global serial_object
    serial_object.write(b'8')

root = Tk()
root.title("Aries Project")
root.geometry('{}x{}'.format(1600, 800))

# Main
if __name__ == "__main__":

    # This is the background image
    photo=ImageTk.PhotoImage(file="logo.jpg")
    label = Label(root,image = photo)
    label.pack()
    root.resizable(False, False)
    frame_2 = Frame(height = 500, width = 1600, bd = 3, relief = 'groove').place(x = 0, y = 300)
    frame_1 = Frame(height = 400, width = 600, bd = 3, relief = 'groove').place(x = 1000, y = 400)

    #Creating Widgets
    LabelOne=Label(root,text= "Tanks:",font = "Times 14 bold")
    LabelTwo=Label(root,text= "Pressurant:",font = "Times 14 bold")
    LabelThree=Label(root,text= "Oxidizer:",font = "Times 14 bold")
    LabelFour=Label(root,text = "Combustion:",font = "Times 14 bold")
    LabelFive=Label(root,text= "Temperature (C):")
    LabelSix=Label(root,text= "Temperature (C):")
    LabelSeven=Label(root,text= "Pressure (psi):")
    LabelEight=Label(root,text= "Pressure (psi):")
    LabelNine=Label(root, text= "Baud Rate:")
    LabelTen=Label(root, text= "Port:")
    LabelEleven=Label(root, text= "Numbers Only")
    LabelTwelve=Label(root, text= "Valves: ",font = "Times 14 bold")
    LabelThirteen=Label(root, text= "High/Low (1/0):",font = "Times 14 bold")
    Label_14=Label(root, text ="Pressurant_Fill: ")
    Label_15=Label(root, text ="Pressurant_Purge:")
    Label_16=Label(root, text ="Pressurant_Oxidizer:")
    Label_17=Label(root, text ="Oxidizer_fill:")
    Label_18=Label(root, text ="Oxidizer_Purge:")
    Label_19=Label(root, text ="Oxi_Combustion:")

    #Placing Widgets
    LabelOne.place(x=40, y=302)
    LabelTwo.place(x=175, y=302)
    LabelThree.place(x=275, y=302)
    LabelFour.place(x=370, y=302)
    LabelFive.place(x=40, y=340)
    LabelSix.place(x=40, y=360)
    LabelSeven.place(x=40, y=380)
    LabelEight.place(x=40, y=400)
    LabelNine.place(x=1100, y=420)
    LabelTen.place(x=1100, y=460)
    LabelEleven.place(x=1100,y=500)
    LabelTwelve.place(x=600, y=302)
    LabelThirteen.place(x=800, y=302)
    Label_14.place(x=600, y=340)
    Label_16.place(x=600, y=360)
    Label_17.place(x=600, y=380)
    Label_19.place(x=600, y=400)

    #Data Labels
    Label_data1=Label(root, text ="X")
    Label_data2=Label(root, text ="X")
    Label_data3=Label(root, text ="X")
    Label_data4=Label(root, text ="X")
    Label_data5=Label(root, text ="X")
    Label_data6=Label(root, text ="X")
    Label_data7=Label(root, text ="X")
    Label_data8=Label(root, text ="X")
    Label_data9=Label(root, text ="X")
    Label_data10=Label(root, text ="X")
    Label_data11=Label(root, text ="X")
    Label_data12=Label(root, text ="X")
    Label_Pressurant_Fill=Label(root, text ="X")
    Label_Pressurant_Oxidizer=Label(root, text ="X")
    Label_Oxidizer_fill=Label(root, text ="X")
    Label_Oxi_Combustion=Label(root, text ="X")

    # Place Data Labels
    Label_data1.place(x=175,y=340)  # Temp of Pressurant
    Label_data2.place(x=175,y=360)  # Temp Redundant of Pressurant
    Label_data3.place(x=175,y=380)  # Pressure of Pressurant
    Label_data4.place(x=175,y=400)  # Pressure Redundant of Pressurant
    Label_data5.place(x=275,y=340)  # Temp of Oxidizer
    Label_data6.place(x=275,y=360)  # Temp Redundant of Oxidizer
    Label_data7.place(x=275,y=380)  # Pressure of Oxidizer
    Label_data8.place(x=275,y=400)  # Pressure Redundant of Oxidizer
    Label_data9.place(x=375,y=340)  # Temp of Combustion Chamber
    Label_data10.place(x=375,y=360 )# Temp Redundant of Combustion Chamber
    Label_data11.place(x=375,y=380) # Pressure of Combustion Chamber
    Label_data12.place(x=375,y=400) # Pressure Redundant of Combustion Chamber
    Label_Pressurant_Fill.place(x=815, y=340)
    Label_Pressurant_Oxidizer.place(x=815, y=360)
    Label_Oxidizer_fill.place(x=815, y=380)
    Label_Oxi_Combustion.place(x=815, y=400)

    # Buttons
    button = Button(root,text = "Send", command = send, width = 6).place(x=1020, y=500) # One way to send command to Control Sys
    connect = Button(root,text = "Connect", command = connect).place(x=1020, y=420) # connect to the Control Sys
    disconnect = Button(root,text = "Disconnect", command = disconnect).place(x=1020, y=540) # Close the program
    
    # Button Commands for Control System
    button1 = Button(root,text = "Open P-Fill", command = open_Pressurant_fill, width = 12).place(x=1020, y=600)
    button2 = Button(root,text = "Close P-Fill", command = close_Pressurant_fill, width = 12).place(x=1020, y=640)
    button3 = Button(root,text = "Open POIV", command = open_POIV, width = 12).place(x=1020, y=680)
    button4 = Button(root,text = "Close POIV", command = close_POIV, width = 12).place(x=1020, y=720)
    button5 = Button(root,text = "Open Oxi-Fill", command = open_Oxidizer_fill, width = 12).place(x=1180, y=600)
    button6 = Button(root,text = "Close Oxi-Fill", command = close_Oxidizer_fill, width = 12).place(x=1180, y=640)
    button7 = Button(root,text = "Launch", command = launch, width = 12).place(x=1180, y=680)
    button8 = Button(root,text = "Abort", command = Abort, width = 12).place(x=1180, y=720)
   
    # Entry
    data_entry=Entry(width=7)
    data_entry.place(x=1200,y=500)
    buad_rate=Entry(width=7)
