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
    self.height = 1000
    self.width = 1000
    self.root = Tk()
    self.root.title("Network Scanner")
    self.root.geometry(f"{self.width}x{self.height}")
    self.root.minsize(600, 600)
    #info
    self.inst = Frame(self.root, bg=self.GREY,relief="flat",width=self.width,height=200)
    self.inst.grid()
    #target
    self.targetLabel = Label(self.inst,text="Target:",bg=self.GREY,font=("Arial",self.labelFont))
    self.targetLabel.grid(column=0,row=1,ipadx=20,ipady=20)
    self.targetEntry = Entry(self.inst,bg="white", font=("Arial", 11),borderwidth=2,relief="ridge")
    self.targetEntry.grid(column=1,row=1)
    #mode
    self.modeLabel = Label(self.inst, text="Mode:",bg=self.GREY,font=("Arial",self.labelFont))
    self.modeLabel.grid(column=2,row=1,ipadx=20)
    self.modeEntry = Entry(self.inst, bg="white", font=("Arial", 11),borderwidth=2,relief="ridge")
    self.modeEntry.grid(column=3,row=1)
    #scan
    self.scanButton = Button(self.inst,text="Scan",bg=self.GREY,font=("Arial",self.labelFont))
    self.scanButton.grid(column=4,row=1,padx=20)
    #output
    self.outputArea = Label(self.root,bg="white",relief="flat",fg="white",font=("Arial",self.labelFont))
    self.outputArea.grid()
    ### end
    self.root.mainloop()
   
# Calling the class
if __name__ == "__main__":
  gui = Gui()
