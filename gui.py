# Modules
import time
import sys
import scan
import threading
from tkinter import *

# Main class
class Gui():
  # On every start up
  def __init__(self):
    ############################# VARIABLES ###########################################
    self.GREY = "#C0C0C0"
    self.labelFont = 13
    self.frameHeight = 38
    self.scanOpts = ["known_ports","specific_port","port_scan"]
    ############################# GUI  ###########################################
    #root
    self.height = 800
    self.width = 800
    self.root = Tk()
    self.root.title("Network Scanner")
    self.root.geometry(f"{self.width}x{self.height}")
    self.root.resizable(False, False)
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    #menu
    self.menu = Menu(self.root)
    self.root.config(menu=self.menu)
    self.fileMenu = Menu(self.menu, tearoff=0)
    self.fileMenu.add_command(label="Save scan report", command=self.saveFile)
    self.menu.add_cascade(label="Save file", menu=self.fileMenu)
    #info
    self.inst = Frame(self.root, bg=self.GREY,relief="flat",width=self.width,height=200)
    self.inst.grid(ipady=20,ipadx=100,sticky=NW)
    #target
    self.targetLabel = Label(self.inst,text="Target:",bg=self.GREY,font=("Arial",self.labelFont))
    self.targetLabel.grid(column=0,row=1,ipadx=20,ipady=20)
    self.targetEntry = Entry(self.inst,bg="white", font=("Arial", 11),borderwidth=1,relief="solid")
    self.targetEntry.grid(column=1,row=1)
    #mode
    self.variable = StringVar(self.root)
    self.variable.set(self.scanOpts[0])
    self.modeLabel = Label(self.inst, text="Mode:",bg=self.GREY,font=("Arial",self.labelFont))
    self.modeLabel.grid(column=2,row=1,ipadx=20)
    self.modeEntry = OptionMenu(self.inst, self.variable, *self.scanOpts)
    self.modeEntry.grid(column=3,row=1)
    #port 
    self.portLabel = Label(self.inst, text="Port:",bg=self.GREY, font=("Arial", self.labelFont))
    self.portLabel.grid(column=4, row=1, ipadx=20)
    self.portEntry = Entry(self.inst, bg="white", font=("Arial", 11), borderwidth=1, relief="solid",width=10)
    self.portEntry.grid(column=5, row=1)
    #scan
    self.scanButton = Button(self.inst,text="Scan",bg=self.GREY,font=("Arial",self.labelFont-1),command=self.scanning)
    self.scanButton.grid(column=6,row=1,padx=40)
    #output
    self.outputFrame = Frame(self.root,width=self.width,height=self.frameHeight, bg="black")
    self.outputFrame.grid()
    self.scrollbar = Scrollbar(self.outputFrame ,orient="vertical")
    self.scrollbar.grid(sticky=NS, row=0, column=0)
    self.outputArea = Listbox(self.outputFrame, yscrollcommand=self.scrollbar.set, width=self.width,height=self.frameHeight, bg="black", fg="white", bd=0, highlightthickness=0, font=("Verdana", self.labelFont-1))
    self.outputArea.grid(column=0, row=0, sticky=NSEW)
    self.scrollbar.config(command=self.outputArea.yview)
    ### end
    self.root.mainloop() 

  #file saving method
  def saveFile(self):
    string =  ''.join(self.outputArea.get(0,END))
    f = open("scan_report.txt", 'a')
    for i in string:
      f.write(i)
    f.close()

  #scanning from the gui
  def scanning(self):
    #calling methods
    scanner = scan.Scanner()
    # check args
    if self.targetEntry.get() == "":
      self.outputArea.insert(END, "No host was given.")
      self.outputArea.insert(END, "Please specify it.")
      self.outputArea.insert(END, "\n")
      return None
    #rewriting scanner options based on GUI input
    for opt in scanner.options:
      if opt == self.variable.get():
        if opt == "known_ports":
          scanner.options[opt] = scanner.options[opt] = True
        else:
          # check args
          if self.portEntry.get() == "":
            self.outputArea.insert(END, "No port / port range was given.")
            self.outputArea.insert(END, "Please specify it.")
            self.outputArea.insert(END, "\n")
            return None
          scanner.options[opt] = scanner.options[self.variable.get()] = self.portEntry.get()
      else:
        scanner.options[opt] = scanner.options[opt] = None
    scanner.options["IP"] = scanner.options["IP"] = self.targetEntry.get()
    scanner.LoopAndThread(self.targetEntry.get())
    # outputing to the screen
    self.outputArea.insert(END, "\n")
    self.outputArea.insert(END, f"Start time of scan: {time.ctime()}\n")
    self.outputArea.insert(END, f"Host: {self.targetEntry.get()}\n")
    self.outputArea.insert(END, "\n")
    self.outputArea.insert(END, f"PORT  STATE\n")
    #removing unneeded items in the array
    for ar in scanner.openPorts:
      if scanner.openPorts.count(ar) > 1:
        while scanner.openPorts.count(ar) != 1:
          scanner.openPorts.remove(ar)
    # outputing to the screen
    if scanner.options["specific_port"] != None:
      if len(scanner.openPorts) == 0:
          self.outputArea.insert(END, f"{self.portEntry.get()}      closed\n")
    for i in scanner.openPorts:
      self.outputArea.insert(END, f"{i}      open\n")
    self.outputArea.insert(END, "\n")
    self.outputArea.insert(END, f"Scan is done: {self.targetEntry.get()} scanned in  {(time.time() - scanner.startTime):.3} seconds\n")
    self.outputArea.insert(END, "________________________________________________________________________")
    self.outputArea.insert(END, "\n")

# Calling the class
if __name__ == "__main__":
  gui = Gui()
