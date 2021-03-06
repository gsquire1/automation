# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.3.10-3.3.19-branch-20170217-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libauth_mgmt/src/idl/LdapServerSettings.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException
import raritan.rpc.auth.ldapsrv


# enumeration
class ServerType(Enumeration):
    idlType = "auth.ldapsrv.ServerType:1.0.0"
    values = ["ACTIVE_DIRECTORY", "OPEN_LDAP"]

ServerType.ACTIVE_DIRECTORY = ServerType(0)
ServerType.OPEN_LDAP = ServerType(1)

# enumeration
class SecurityProtocol(Enumeration):
    idlType = "auth.ldapsrv.SecurityProtocol:1.0.0"
    values = ["SEC_PROTO_NONE", "SEC_PROTO_SSL", "SEC_PROTO_STARTTLS"]

SecurityProtocol.SEC_PROTO_NONE = SecurityProtocol(0)
SecurityProtocol.SEC_PROTO_SSL = SecurityProtocol(1)
SecurityProtocol.SEC_PROTO_STARTTLS = SecurityProtocol(2)

# structure
class ServerSettings(Structure):
    idlType = "auth.ldapsrv.ServerSettings:2.0.0"
    elements = ["id", "server", "adoptSettingsId", "type", "secProto", "port", "sslPort", "forceTrustedCert", "allowOffTimeRangeCerts", "certificate", "adsDomain", "useAnonymousBind", "bindDN", "bindPwd", "searchBaseDN", "loginNameAttr", "userEntryObjClass", "userSearchFilter"]

    def __init__(self, id, server, adoptSettingsId, type, secProto, port, sslPort, forceTrustedCert, allowOffTimeRangeCerts, certificate, adsDomain, useAnonymousBind, bindDN, bindPwd, searchBaseDN, loginNameAttr, userEntryObjClass, userSearchFilter):
        typecheck.is_string(id, AssertionError)
        typecheck.is_string(server, AssertionError)
        typecheck.is_string(adoptSettingsId, AssertionError)
        typecheck.is_enum(type, raritan.rpc.auth.ldapsrv.ServerType, AssertionError)
        typecheck.is_enum(secProto, raritan.rpc.auth.ldapsrv.SecurityProtocol, AssertionError)
        typecheck.is_int(port, AssertionError)
        typecheck.is_int(sslPort, AssertionError)
        typecheck.is_bool(forceTrustedCert, AssertionError)
        typecheck.is_bool(allowOffTimeRangeCerts, AssertionError)
        typecheck.is_string(certificate, AssertionError)
        typecheck.is_string(adsDomain, AssertionError)
        typecheck.is_bool(useAnonymousBind, AssertionError)
        typecheck.is_string(bindDN, AssertionError)
        typecheck.is_string(bindPwd, AssertionError)
        typecheck.is_string(searchBaseDN, AssertionError)
        typecheck.is_string(loginNameAttr, AssertionError)
        typecheck.is_string(userEntryObjClass, AssertionError)
        typecheck.is_string(userSearchFilter, AssertionError)

        self.id = id
        self.server = server
        self.adoptSettingsId = adoptSettingsId
        self.type = type
        self.secProto = secProto
        self.port = port
        self.sslPort = sslPort
        self.forceTrustedCert = forceTrustedCert
        self.allowOffTimeRangeCerts = allowOffTimeRangeCerts
        self.certificate = certificate
        self.adsDomain = adsDomain
        self.useAnonymousBind = useAnonymousBind
        self.bindDN = bindDN
        self.bindPwd = bindPwd
        self.searchBaseDN = searchBaseDN
        self.loginNameAttr = loginNameAttr
        self.userEntryObjClass = userEntryObjClass
        self.userSearchFilter = userSearchFilter

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            id = json['id'],
            server = json['server'],
            adoptSettingsId = json['adoptSettingsId'],
            type = raritan.rpc.auth.ldapsrv.ServerType.decode(json['type']),
            secProto = raritan.rpc.auth.ldapsrv.SecurityProtocol.decode(json['secProto']),
            port = json['port'],
            sslPort = json['sslPort'],
            forceTrustedCert = json['forceTrustedCert'],
            allowOffTimeRangeCerts = json['allowOffTimeRangeCerts'],
            certificate = json['certificate'],
            adsDomain = json['adsDomain'],
            useAnonymousBind = json['useAnonymousBind'],
            bindDN = json['bindDN'],
            bindPwd = json['bindPwd'],
            searchBaseDN = json['searchBaseDN'],
            loginNameAttr = json['loginNameAttr'],
            userEntryObjClass = json['userEntryObjClass'],
            userSearchFilter = json['userSearchFilter'],
        )
        return obj

    def encode(self):
        json = {}
        json['id'] = self.id
        json['server'] = self.server
        json['adoptSettingsId'] = self.adoptSettingsId
        json['type'] = raritan.rpc.auth.ldapsrv.ServerType.encode(self.type)
        json['secProto'] = raritan.rpc.auth.ldapsrv.SecurityProtocol.encode(self.secProto)
        json['port'] = self.port
        json['sslPort'] = self.sslPort
        json['forceTrustedCert'] = self.forceTrustedCert
        json['allowOffTimeRangeCerts'] = self.allowOffTimeRangeCerts
        json['certificate'] = self.certificate
        json['adsDomain'] = self.adsDomain
        json['useAnonymousBind'] = self.useAnonymousBind
        json['bindDN'] = self.bindDN
        json['bindPwd'] = self.bindPwd
        json['searchBaseDN'] = self.searchBaseDN
        json['loginNameAttr'] = self.loginNameAttr
        json['userEntryObjClass'] = self.userEntryObjClass
        json['userSearchFilter'] = self.userSearchFilter
        return json
