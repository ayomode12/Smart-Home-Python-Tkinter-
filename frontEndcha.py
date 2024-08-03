from tkinter import *
from tkinter import Spinbox
from backendchallenge import SmartHome, SmartPlug, CustomDevice

class SmartHomeSystem:
    def __init__(self, smartDevices):
        self.smartDevices = smartDevices
        self.win = Tk()
        self.win.title("SmartHome System")
        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(column=0, row=0)
        smartHomeDevices = self.smartDevices.devices
        self.smartHomeDevices = smartHomeDevices
        self.smartSystemWidgets = []
        self.plug_image = PhotoImage(file='smartPlug.png')
        self.resized_image = self.plug_image.subsample(2, 2)
        self.smart_image = PhotoImage(file='smartDoor.png')
        self.door_image = self.smart_image.subsample(2,2)
 
    def run(self):
        self.createWidgets()
        self.win.mainloop()

    def createWidgets(self):
        
        
        self.deleteAllWidgets()
        btnTurnOnAll = Button(
            self.mainFrame,
            text="Turn On All",
            command=self.turnOnAll
        )
        btnTurnOnAll.grid(row=0, column=0)

        btnTurnOffAll = Button(
            self.mainFrame,
            text="Turn Off All",
            command=self.turnOffAll
        )
        btnTurnOffAll.grid(row=0, column=1)

        for i in range(len(self.smartHomeDevices)):
            device = self.smartDevices.getDeviceAt(i)
            if isinstance(device, SmartPlug):
                label = Label(
                    self.mainFrame,
                    text=f"Plug: {device.switchedOn}, consumption Rate: {device.consumptionRate}",
                    image = self.resized_image,
                    compound = "right"
                )
                label.grid(row=i + 1, column=0)
                self.smartSystemWidgets.append(label)
                
            
                consumption_spinbox = Spinbox(
                    self.mainFrame,
                    from_=0,
                    to=150,
                    width=5,
                )
                consumption_spinbox.grid(row=i + 1, column=1)
                consumption_spinbox.delete(0, END)
                consumption_spinbox.insert(0, device.consumptionRate)
                consumption_spinbox.config(command=lambda index=i, spinbox =consumption_spinbox: self.updateConsumptionRate(index, spinbox))
                self.smartSystemWidgets.append(consumption_spinbox)

            elif isinstance(device, CustomDevice):
                label = Label(
                    self.mainFrame,
                    text=f"Smart Door: {device.switchedOn}, Locked: {device.locked} ",
                    image = self.door_image,
                    compound = "right"
                )
                label.grid(row=i + 1, column=0)
                self.smartSystemWidgets.append(label)

            toggleButton = Button(self.mainFrame, text="Toggle", command=lambda index=i: self.toggleDev(index))
            toggleButton.grid(row=i + 1, column=2)
            self.smartSystemWidgets.append(toggleButton)

            editButton = Button(self.mainFrame, text="Edit", command=lambda index=i: self.createNewWin(index))
            editButton.grid(row=i + 1, column=3)
            self.smartSystemWidgets.append(editButton)

            deleteButton = Button(self.mainFrame, text="Delete", command=lambda index=i: self.deleteDevice(index))
            deleteButton.grid(row=i + 1, column=4)
            self.smartSystemWidgets.append(deleteButton)

        addButton = Button(self.mainFrame, text="Add", command=self.addDeviceWindow)
        addButton.grid(row=len(self.smartHomeDevices) + 1, column=0)
        self.smartSystemWidgets.append(addButton)

    def updateConsumptionRate(self, index, spinbox):
        new_consumption_rate = int(spinbox.get())
        device = self.smartDevices.getDeviceAt(index)
        if isinstance(device, SmartPlug):
            device.setConsumptionRate(new_consumption_rate)
            self.createWidgets()


    
                
            
            
    def toggleDev(self, index):
        toggleDevice = self.smartDevices.getDeviceAt(index)
        toggleDevice.toggleSwitch()
        self.createWidgets()

    def deleteDevice(self, index):
        self.smartDevices.removeDeviceAt(index)
        self.createWidgets()

    def deleteAllWidgets(self):
        for widget in self.smartSystemWidgets:
            widget.destroy()
        self.smartSystemWidgets = []

    def turnOnAll(self):
        smartHomeDevices = self.smartDevices.devices
        for devices in smartHomeDevices:
            devices.switchedOn = True
        self.createWidgets()

    def turnOffAll(self):
        smartHomeDevices = self.smartDevices.devices
        for devices in smartHomeDevices:
            devices.switchedOn = False
        self.createWidgets()

    def createNewWin(self, index):
        device = self.smartDevices.getDeviceAt(index)
        newWin = Toplevel(self.win)
        consumption_var = IntVar()
        newWin.title("Edit Device")
        
        switchedOnlbl = Label(newWin,
                              text = f"Light: {device.switchedOn}",
                              )
        switchedOnlbl.grid(row=1, column=0)
        
        btnToggle = Button(
            newWin,
            text = "Toggle",
            command=lambda index=index: self.toggleDev(index)
            )
        btnToggle.grid(row=1, column=1)
        
        if isinstance(device, SmartPlug):
            label = Label(newWin, text = f"consumption Rate: {device.consumptionRate}")
            label.grid(row=2, column=0)
            entryCon = Entry(newWin, text=consumption_var )
            entryCon.grid(row=2, column=1)
            
            
        else:
            labelSmart = Label(newWin, text = f"locked: {device.locked}")
            labelSmart.grid(row=2, column=0)
            btnLocked = Button(newWin, text = "Toggle SmartDoor", command= lambda: self.toggleSmartDoor(index))
            btnLocked.grid(row=2, column=1)
        
        closebtn = Button(
            newWin,
            text ="Close",
            command= lambda: self.updateDevice(device, consumption_var, newWin)
            )
        closebtn.grid(row=3, column=0)
        
    def updateDevice(self, device, consumption_var, newWin):
        if isinstance(device, SmartPlug):
            newRate = consumption_var.get()
            device.setConsumptionRate(newRate)
            #plugLabel.config(text=f"consumptionRate:{device.consumptionRate}")
            
        else:
            pass
        newWin.destroy()
        self.createWidgets()


    def toggleSmartDoor(self, index):
        toggleDevice = self.smartDevices.getDeviceAt(index)
        toggleDevice.setLocked()
        self.createWidgets()

    def addDeviceWindow(self):
        addWin = Toplevel(self.win)
        addWin.title("Add Device")
        
        consumption_var = IntVar()

        def addSmartPlug():
            consumption_rate = consumption_var.get()
            new_device = SmartPlug(consumption_rate)
            self.smartDevices.addDevice(new_device)
            self.createWidgets()
            addWin.destroy()

        def addCustomDevice():
            new_device = CustomDevice()
            self.smartDevices.addDevice(new_device)
            self.createWidgets()
            addWin.destroy()

        consumption_label = Label(addWin, text="Enter Consumption Rate:")
        consumption_label.grid(row=0, column=0)

        consumption_spinbox = Spinbox(addWin, from_=0, to=150, textvariable=consumption_var)
        consumption_spinbox.grid(row=0, column=1)

        Label(addWin, text="Choose device type:").grid(row=1, column=0, columnspan=2)

        Button(addWin, text="Smart Plug", command=addSmartPlug).grid(row=2, column=0)
        Button(addWin, text="Custom Device", command=addCustomDevice).grid(row=2, column=1)

        closeButton = Button(addWin, text="Close", command=addWin.destroy)
        closeButton.grid(row=3, column=0)
        
    
            

def main():
    smartPlug1 = SmartPlug(45)
    smartPlug2 = SmartPlug(45)
    smartDoor = CustomDevice()
    smartPlug1.setConsumptionRate(150)
    smartPlug2.setConsumptionRate(25)
    smartDevices = SmartHome()
    smartDevices.addDevice(smartPlug1)
    smartDevices.addDevice(smartPlug2)
    smartDevices.addDevice(smartDoor)
    smartHome = SmartHomeSystem(smartDevices)
    smartHome.run()
    
    
main()

