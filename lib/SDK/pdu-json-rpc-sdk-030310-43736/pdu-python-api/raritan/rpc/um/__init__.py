# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.3.10-3.3.19-branch-20170217-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libum_local/src/idl/SnmpV3.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException

# interface
class SnmpV3(Interface):
    idlType = "um.SnmpV3:1.0.0"

    # enumeration
    class SecurityLevel(Enumeration):
        idlType = "um.SnmpV3.SecurityLevel:1.0.0"
        values = ["NO_AUTH_NO_PRIV", "AUTH_NO_PRIV", "AUTH_PRIV"]

    SecurityLevel.NO_AUTH_NO_PRIV = SecurityLevel(0)
    SecurityLevel.AUTH_NO_PRIV = SecurityLevel(1)
    SecurityLevel.AUTH_PRIV = SecurityLevel(2)

    # enumeration
    class AuthProtocol(Enumeration):
        idlType = "um.SnmpV3.AuthProtocol:1.0.0"
        values = ["MD5", "SHA1"]

    AuthProtocol.MD5 = AuthProtocol(0)
    AuthProtocol.SHA1 = AuthProtocol(1)

    # enumeration
    class PrivProtocol(Enumeration):
        idlType = "um.SnmpV3.PrivProtocol:1.0.0"
        values = ["DES", "AES128"]

    PrivProtocol.DES = PrivProtocol(0)
    PrivProtocol.AES128 = PrivProtocol(1)