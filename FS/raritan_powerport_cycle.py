#!/usr/bin/env python3

import sys, time
sys.path.append('/home/automation/lib/SDK')
#sys.path.append("pdu-python-api")
from raritan.rpc import Agent, pdumodel, firmware, sensors


ip = "10.39.36.112"
user = "user"
pw = "pass"
try:
    ip = sys.argv[1]
    user = sys.argv[2]
    pw = sys.argv[3]
except IndexError:
    pass # use defaults

agent = Agent("https", ip, user, pw, disable_certificate_verification=True)
pdu = pdumodel.Pdu("/model/pdu/0", agent)
firmware_proxy = firmware.Firmware("/firmware", agent)

inlets = pdu.getInlets()
ocps = pdu.getOverCurrentProtectors()
outlets = pdu.getOutlets()
#print(outlets)
print ("PDU: %s" % (ip))
print ("Firmware version: %s" % (firmware_proxy.getVersion()))
print ("Number of inlets: %d" % (len(inlets)))
print ("Number of over current protectors: %d" % (len(ocps)))
print ("Number of outlets: %d" % (len(outlets)))
port=1
outlet = outlets[port]

outlet_metadata = outlet.getMetaData()
outlet_settings = outlet.getSettings()

print ("Outlet %s:" % (format(outlet_metadata.label)))
print ("  Name: %s" % (outlet_settings.name if outlet_settings.name != "" else "(none)"))
print ("  Switchable: %s" % ("yes" if outlet_metadata.isSwitchable else "no"))


if outlet_metadata.isSwitchable:
    outlet_state = outlet.getState()
    print("OUTLET_GET_STATE")
    print(outlet_state)
    if outlet_state.available:
        #print ("  Status :%s" % ("on" if outlet_state.value == outlet_state_sensor.OnOffState.ON.val else "off"))
        print ("  Status :%s" % ("on" if outlet_state.powerState == pdumodel.Outlet.PowerState.PS_ON else "off"))
    print ("  Turning outlet off...")
    outlet.setPowerState(outlet.PowerState.PS_OFF)
    print ("  Sleeping 4 seconds...")
    time.sleep(4)
    print ("  Turning outlet on...")
    outlet.setPowerState(outlet.PowerState.PS_ON)
    outlet_state = outlet.getState()
    if outlet_state.available:
        print ("  Status :%s" % ("on" if outlet_state.powerState == pdumodel.Outlet.PowerState.PS_ON else "off"))
else:
    print("THIS PDU DOES NOT SUPPPORT CLI POWERCYCLING")
   
          