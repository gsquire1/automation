#!/usr/bin/env python

import sys, time

sys.path.append("pdu-python-api")
from raritan.rpc import Agent, pdumodel, firmware, sensors

# ip = "10.0.42.2"
# user = "admin"
# pw = "raritan"

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

print ("PDU: ", ip)
print ("Firmware version: ", firmware_proxy.getVersion())
print ("Number of inlets: ", len(inlets))
print ("Number of over current protectors: ", len(ocps))
print ("Number of outlets: ", len(outlets))

outlet = outlets[1]

# outlet_sensors = outlet.getSensors()
# print(outlet_sensors)
outlet_metadata = outlet.getMetaData()
print("METADATA")
print(outlet_metadata)
outlet_settings = outlet.getSettings()
print("OUTLET_SETTINGS")
print(outlet_settings)
print("OUTLET")
print(outlet)
print("OUTLET_STATE")
outlet_state = outlet.getState()
print(outlet_state)
# print("OUTLET_STATE_VALUE")
# outlet_state = outlet.powerState()
# print(outlet_state)
print ("Outlet %s:" % (format(outlet_metadata.label)))
print ("  Name: %s" % (outlet_settings.name if outlet_settings.name != "" else "(none)"))
print ("  Switchable: %s" % ("yes" if outlet_metadata.isSwitchable else "no"))
print ("  Power State: %s" % ("on" if outlet_state.powerState == pdumodel.Outlet.PowerState.PS_ON else "off"))
#print(outlet_state.powerState)
outlet.setPowerState(outlet.PowerState.PS_ON)
time.sleep(5)
outlet_state = outlet.getState()
print(outlet_state.powerState)
# print ("  Turning outlet on...")
# outlet.setPowerState(outlet.PowerState.PS_ON)
# outlet_state = outlet_state_sensor.getState()
sys.exit()
# print("OUTLET_POWER_STATE_VALUE")
# outlet_power = outlet.PowerState
# print(outlet_power)
if outlet_state.available:
    print("OUTLET_STATE_AVAILABLE")
    print (outlet_state.available)
    print ("  Status :", "on" if outlet_state.value == outlet_state_sensor.OnOffState.ON.val else "off")

print ("  Turning outlet on...")
outlet.setPowerState(outlet.PowerState.PS_ON)
outlet_state = outlet_state_sensor.getState()
sys.exit()

sys.exit(0)

print ("  Turning outlet on...")
outlet.setPowerState(outlet.PowerState.PS_ON)
outlet_state = outlet_state_sensor.getState()
if outlet_state.available:
    print "  Status :", "on" if outlet_state.value == outlet_state_sensor.OnOffState.ON.val else "off"

print "Outlet {10}:".format(outlet_metadata.label)
print "  Name: ", outlet_settings.name if outlet_settings.name != "" else "(none)"
print "  Switchable: ", "yes" if outlet_metadata.isSwitchable else "no"
sys.exit(0)
if outlet_sensors.voltage:
    sensor_reading = outlet_sensors.voltage.getReading()
    print "  Voltage:", "{0} V".format(sensor_reading.value) if sensor_reading.valid else "n/a"

if outlet_sensors.current:
    sensor_reading = outlet_sensors.current.getReading()
    print "  Current:", "{0} A".format(sensor_reading.value) if sensor_reading.valid else "n/a"

if outlet_metadata.isSwitchable:
    outlet_state_sensor = outlet_sensors.outletState
    outlet_state = outlet_state_sensor.getState()
    if outlet_state.available:
        print "  Status :", "on" if outlet_state.value == outlet_state_sensor.OnOffState.ON.val else "off"
    print "  Turning outlet off..."
    outlet.setPowerState(outlet.PowerState.PS_OFF)
    print "  Sleeping 4 seconds..."
    time.sleep(4)
    print "  Turning outlet on..."
    outlet.setPowerState(outlet.PowerState.PS_ON)
    outlet_state = outlet_state_sensor.getState()
    if outlet_state.available:
        print "  Status :", "on" if outlet_state.value == outlet_state_sensor.OnOffState.ON.val else "off"
