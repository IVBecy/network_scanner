# Modules
import time
import sys
import scan
from tkinter import *

# Main class
class Gui():
  # On every start up
  def __init__(self):
    ############################# GUI  ###########################################
    self.GREY = "#C0C0C0"
    self.labelFont = 13
    #root
    self.height = 600
    self.width = 600
    self.root = Tk()
    self.root.title("Network Scanner")
    self.root.geometry(f"{self.width}x{self.height}")
    self.root.minsize(600, 600)
    self.root.maxsize(700, 700)
    #info
    self.inst = Frame(self.root, bg=self.GREY,relief="flat",width=self.width,height=200)
    self.inst.grid(ipadx=5000)
    #target
    self.targetLabel = Label(self.inst,text="Target:",bg=self.GREY,font=("Arial",self.labelFont))
    self.targetLabel.grid(column=0,row=1,ipadx=20,ipady=20)
    self.targetEntry = Entry(self.inst,bg="white", font=("Arial", 11),borderwidth=2,relief="ridge")
    self.targetEntry.grid(column=1,row=1)
    #mode
    self.modeLabel = Label(self.inst, text="Mode:",bg=self.GREY,font=("Arial",self.labelFont))
    self.modeLabel.grid(column=2,row=1,ipadx=20)
    self.modeEntry = Entry(self.inst,bg="white",font=("Arial", 11),borderwidth=2,relief="ridge")
    self.modeEntry.grid(column=3,row=1)
    #scan
    self.scanButton = Button(self.inst,text="Scan",bg=self.GREY,font=("Arial",self.labelFont),command=self.scanning)
    self.scanButton.grid(column=4,row=1,padx=20)
    #output
    self.textvar = StringVar()
    self.textvar.set("djbfhjsbfjhbsfhub")
    self.outputArea = Label(self.root,textvariable=self.textvar,bg="black",fg="black",relief="flat",font=("Arial",self.labelFont))
    self.outputArea.grid(column=1,row=2)    
    ##### Variables for scanning
    self.guiTarget = self.targetEntry.get()
    self.guiMethod = self.modeEntry.get()
    ## usage and option check
    options = scan.options
    print(options)
    if __name__ == "__main__":
      #Checking for needed arguments  
      if options.help:
        self.textvar.set(scan.usage_text)
      if options.IP is None:
         self.outputArea.config(text=scan.usage_text)
      if (options.port_scan is None) and (options.known_ports is None) and (options.specific_port is None):
         self.outputArea.config(text=scan.usage_text)
    ### end
    self.root.mainloop() 

  def scanning(self):
    Scannner = scan.Scanner()
    

# Calling the class
if __name__ == "__main__":
  gui = Gui()