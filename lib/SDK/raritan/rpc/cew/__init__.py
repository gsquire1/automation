# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.3.10-3.3.19-branch-20170217-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libidl_client/cew/idl/EnergyWiseSettings.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException

# structure
class EnergyWiseSettings(Structure):
    idlType = "cew.EnergyWiseSettings:1.0.0"
    elements = ["enabled", "domainName", "secret", "port", "pollingInterval"]

    def __init__(self, enabled, domainName, secret, port, pollingInterval):
        typecheck.is_bool(enabled, AssertionError)
        typecheck.is_string(domainName, AssertionError)
        typecheck.is_string(secret, AssertionError)
        typecheck.is_int(port, AssertionError)
        typecheck.is_int(pollingInterval, AssertionError)

        self.enabled = enabled
        self.domainName = domainName
        self.secret = secret
        self.port = port
        self.pollingInterval = pollingInterval

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            enabled = json['enabled'],
            domainName = json['domainName'],
            secret = json['secret'],
            port = json['port'],
            pollingInterval = json['pollingInterval'],
        )
        return obj

    def encode(self):
        json = {}
        json['enabled'] = self.enabled
        json['domainName'] = self.domainName
        json['secret'] = self.secret
        json['port'] = self.port
        json['pollingInterval'] = self.pollingInterval
        return json
# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.3.10-3.3.19-branch-20170217-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libidl_client/cew/idl/EnergyWiseManager.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException
import raritan.rpc.cew


# interface
class EnergyWiseManager(Interface):
    idlType = "cew.EnergyWiseManager:1.0.0"

    class _getSettings(Interface.Method):
        name = 'getSettings'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = raritan.rpc.cew.EnergyWiseSettings.decode(rsp['_ret_'], agent)
            typecheck.is_struct(_ret_, raritan.rpc.cew.EnergyWiseSettings, DecodeException)
            return _ret_

    class _setSettings(Interface.Method):
        name = 'setSettings'

        @staticmethod
        def encode(settings):
            typecheck.is_struct(settings, raritan.rpc.cew.EnergyWiseSettings, AssertionError)
            args = {}
            args['settings'] = raritan.rpc.cew.EnergyWiseSettings.encode(settings)
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_int(_ret_, DecodeException)
            return _ret_
    def __init__(self, target, agent):
        super(EnergyWiseManager, self).__init__(target, agent)
        self.getSettings = EnergyWiseManager._getSettings(self)
        self.setSettings = EnergyWiseManager._setSettings(self)