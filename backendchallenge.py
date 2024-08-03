class Device:
    def __init__(self, switchedOn=False):
        self.switchedOn = switchedOn

    def toggleSwitch(self):
        self.switchedOn = not self.switchedOn

    def getSwitchedOn(self):
        return self.switchedOn

    def __str__(self):
        return f"The device's switched on state is {self.switchedOn}"


class SmartPlug(Device):
    def __init__(self, consumptionRate, switchedOn=False):
        super().__init__(switchedOn)
        self.consumptionRate = consumptionRate

    def getConsumptionRate(self):
        return self.consumptionRate

    def setConsumptionRate(self, rate):
        #if rate <= 151:
        self.consumptionRate = rate

    def __str__(self):
        output = super().__str__() + "\n"
        output += f"The consumption rate of the device is {self.consumptionRate}"
        return output

def testSmartPlug():
    smartPlug = SmartPlug(45)
    smartPlug.toggleSwitch()
    #print(smartPlug.getSwitchOn())
    print(smartPlug.getConsumptionRate())
    smartPlug.setConsumptionRate(29)
    print(smartPlug.getConsumptionRate())
    print(smartPlug)
    
testSmartPlug()

class CustomDevice(Device):
    def __init__(self, locked=True, switchedOn=False):
        super().__init__(switchedOn)
        self.locked = locked

    def getLocked(self):
        return self.locked

    def setLocked(self):
        self.locked = not self.locked

    def __str__(self):
        output = super().__str__() + "\n"
        output += f"The current state of the smart door is {self.locked}"
        return output


class SmartHome:
    def __init__(self):
        self.devices = []

    def getDevices(self):
        return self.devices

    def getDeviceAt(self, index):
        return self.devices[index]

    def removeDeviceAt(self, index):
        del self.devices[index]

    def addDevice(self, device):
        self.devices.append(device)

    def toggleSwitchAt(self, index):
        self.devices[index].toggleSwitch()

    def turnOnAll(self):
        for device in self.devices:
            device.switched_on = True

    def turnOffAll(self):
        for device in self.devices:
            device.switched_on = False

    def __str__(self):
        output = "Your smart home has the following devices:\n"
        for device in self.devices:
            output += str(device) + "\n"
        return output



# def test_smart_home():
#     smarthome = SmartHome()
#     smartplug1 = SmartPlug(45)
#     smartplug2 = SmartPlug(45)
#     smartdoor = CustomDevice()
#     smartplug1.toggleSwitch()
# 
#     smarthome.addDevice(smartplug1)
#     smarthome.addDevice(smartplug2)
#     smarthome.addDevice(smartdoor)
# 
#     print(smarthome)
# 
#     smarthome.removeDeviceAt(0)
#     print(smarthome)
# 
# 
# test_smart_home()