# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.2.30-3.2.39-branch-20160511-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libisys/src/idl/Firmware.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException
import raritan.rpc.firmware


# enumeration
class UpdateHistoryStatus(Enumeration):
    idlType = "firmware.UpdateHistoryStatus:1.0.0"
    values = ["SUCCESSFUL", "FAILED", "INCOMPLETE"]

UpdateHistoryStatus.SUCCESSFUL = UpdateHistoryStatus(0)
UpdateHistoryStatus.FAILED = UpdateHistoryStatus(1)
UpdateHistoryStatus.INCOMPLETE = UpdateHistoryStatus(2)

# structure
class UpdateHistoryEntry(Structure):
    idlType = "firmware.UpdateHistoryEntry:1.0.0"
    elements = ["timestamp", "oldVersion", "imageVersion", "imageMD5", "status"]

    def __init__(self, timestamp, oldVersion, imageVersion, imageMD5, status):
        typecheck.is_time(timestamp, AssertionError)
        typecheck.is_string(oldVersion, AssertionError)
        typecheck.is_string(imageVersion, AssertionError)
        typecheck.is_string(imageMD5, AssertionError)
        typecheck.is_enum(status, raritan.rpc.firmware.UpdateHistoryStatus, AssertionError)

        self.timestamp = timestamp
        self.oldVersion = oldVersion
        self.imageVersion = imageVersion
        self.imageMD5 = imageMD5
        self.status = status

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            timestamp = raritan.rpc.Time.decode(json['timestamp']),
            oldVersion = json['oldVersion'],
            imageVersion = json['imageVersion'],
            imageMD5 = json['imageMD5'],
            status = raritan.rpc.firmware.UpdateHistoryStatus.decode(json['status']),
        )
        return obj

    def encode(self):
        json = {}
        json['timestamp'] = raritan.rpc.Time.encode(self.timestamp)
        json['oldVersion'] = self.oldVersion
        json['imageVersion'] = self.imageVersion
        json['imageMD5'] = self.imageMD5
        json['status'] = raritan.rpc.firmware.UpdateHistoryStatus.encode(self.status)
        return json

# enumeration
class ImageState(Enumeration):
    idlType = "firmware.ImageState:1.0.0"
    values = ["NONE", "UPLOADING", "UPLOAD_FAILED", "DOWNLOADING", "DOWNLOAD_FAILED", "COMPLETE"]

ImageState.NONE = ImageState(0)
ImageState.UPLOADING = ImageState(1)
ImageState.UPLOAD_FAILED = ImageState(2)
ImageState.DOWNLOADING = ImageState(3)
ImageState.DOWNLOAD_FAILED = ImageState(4)
ImageState.COMPLETE = ImageState(5)

# structure
class ImageStatus(Structure):
    idlType = "firmware.ImageStatus:1.0.0"
    elements = ["state", "error_message", "time_started", "size_total", "size_done"]

    def __init__(self, state, error_message, time_started, size_total, size_done):
        typecheck.is_enum(state, raritan.rpc.firmware.ImageState, AssertionError)
        typecheck.is_string(error_message, AssertionError)
        typecheck.is_time(time_started, AssertionError)
        typecheck.is_int(size_total, AssertionError)
        typecheck.is_int(size_done, AssertionError)

        self.state = state
        self.error_message = error_message
        self.time_started = time_started
        self.size_total = size_total
        self.size_done = size_done

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            state = raritan.rpc.firmware.ImageState.decode(json['state']),
            error_message = json['error_message'],
            time_started = raritan.rpc.Time.decode(json['time_started']),
            size_total = json['size_total'],
            size_done = json['size_done'],
        )
        return obj

    def encode(self):
        json = {}
        json['state'] = raritan.rpc.firmware.ImageState.encode(self.state)
        json['error_message'] = self.error_message
        json['time_started'] = raritan.rpc.Time.encode(self.time_started)
        json['size_total'] = self.size_total
        json['size_done'] = self.size_done
        return json

# structure
class ImageInfo(Structure):
    idlType = "firmware.ImageInfo:1.0.1"
    elements = ["valid", "version", "min_required_version", "min_downgrade_version", "product", "platform", "oem", "hwid_whitelist", "hwid_blacklist", "compatible", "signature_present", "signed_by", "signature_good", "certified_by", "certificate_good", "model_list_present", "model_supported"]

    def __init__(self, valid, version, min_required_version, min_downgrade_version, product, platform, oem, hwid_whitelist, hwid_blacklist, compatible, signature_present, signed_by, signature_good, certified_by, certificate_good, model_list_present, model_supported):
        typecheck.is_bool(valid, AssertionError)
        typecheck.is_string(version, AssertionError)
        typecheck.is_string(min_required_version, AssertionError)
        typecheck.is_string(min_downgrade_version, AssertionError)
        typecheck.is_string(product, AssertionError)
        typecheck.is_string(platform, AssertionError)
        typecheck.is_string(oem, AssertionError)
        typecheck.is_string(hwid_whitelist, AssertionError)
        typecheck.is_string(hwid_blacklist, AssertionError)
        typecheck.is_bool(compatible, AssertionError)
        typecheck.is_bool(signature_present, AssertionError)
        typecheck.is_string(signed_by, AssertionError)
        typecheck.is_bool(signature_good, AssertionError)
        typecheck.is_string(certified_by, AssertionError)
        typecheck.is_bool(certificate_good, AssertionError)
        typecheck.is_bool(model_list_present, AssertionError)
        typecheck.is_bool(model_supported, AssertionError)

        self.valid = valid
        self.version = version
        self.min_required_version = min_required_version
        self.min_downgrade_version = min_downgrade_version
        self.product = product
        self.platform = platform
        self.oem = oem
        self.hwid_whitelist = hwid_whitelist
        self.hwid_blacklist = hwid_blacklist
        self.compatible = compatible
        self.signature_present = signature_present
        self.signed_by = signed_by
        self.signature_good = signature_good
        self.certified_by = certified_by
        self.certificate_good = certificate_good
        self.model_list_present = model_list_present
        self.model_supported = model_supported

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            valid = json['valid'],
            version = json['version'],
            min_required_version = json['min_required_version'],
            min_downgrade_version = json['min_downgrade_version'],
            product = json['product'],
            platform = json['platform'],
            oem = json['oem'],
            hwid_whitelist = json['hwid_whitelist'],
            hwid_blacklist = json['hwid_blacklist'],
            compatible = json['compatible'],
            signature_present = json['signature_present'],
            signed_by = json['signed_by'],
            signature_good = json['signature_good'],
            certified_by = json['certified_by'],
            certificate_good = json['certificate_good'],
            model_list_present = json['model_list_present'],
            model_supported = json['model_supported'],
        )
        return obj

    def encode(self):
        json = {}
        json['valid'] = self.valid
        json['version'] = self.version
        json['min_required_version'] = self.min_required_version
        json['min_downgrade_version'] = self.min_downgrade_version
        json['product'] = self.product
        json['platform'] = self.platform
        json['oem'] = self.oem
        json['hwid_whitelist'] = self.hwid_whitelist
        json['hwid_blacklist'] = self.hwid_blacklist
        json['compatible'] = self.compatible
        json['signature_present'] = self.signature_present
        json['signed_by'] = self.signed_by
        json['signature_good'] = self.signature_good
        json['certified_by'] = self.certified_by
        json['certificate_good'] = self.certificate_good
        json['model_list_present'] = self.model_list_present
        json['model_supported'] = self.model_supported
        return json

# enumeration
class UpdateFlags(Enumeration):
    idlType = "firmware.UpdateFlags:1.0.0"
    values = ["CROSS_OEM", "CROSS_HW", "ALLOW_UNTRUSTED"]

UpdateFlags.CROSS_OEM = UpdateFlags(0)
UpdateFlags.CROSS_HW = UpdateFlags(1)
UpdateFlags.ALLOW_UNTRUSTED = UpdateFlags(2)

# interface
class Firmware(Interface):
    idlType = "firmware.Firmware:2.0.0"

    class _reboot(Interface.Method):
        name = 'reboot'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            return None

    class _factoryReset(Interface.Method):
        name = 'factoryReset'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            return None

    class _getVersion(Interface.Method):
        name = 'getVersion'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            typecheck.is_string(_ret_, DecodeException)
            return _ret_

    class _getUpdateHistory(Interface.Method):
        name = 'getUpdateHistory'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = [raritan.rpc.firmware.UpdateHistoryEntry.decode(x0, agent) for x0 in rsp['_ret_']]
            for x0 in _ret_:
                typecheck.is_struct(x0, raritan.rpc.firmware.UpdateHistoryEntry, DecodeException)
            return _ret_

    class _getImageStatus(Interface.Method):
        name = 'getImageStatus'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = raritan.rpc.firmware.ImageStatus.decode(rsp['_ret_'], agent)
            typecheck.is_struct(_ret_, raritan.rpc.firmware.ImageStatus, DecodeException)
            return _ret_

    class _discardImage(Interface.Method):
        name = 'discardImage'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            return None

    class _getImageInfo(Interface.Method):
        name = 'getImageInfo'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = rsp['_ret_']
            info = raritan.rpc.firmware.ImageInfo.decode(rsp['info'], agent)
            typecheck.is_bool(_ret_, DecodeException)
            typecheck.is_struct(info, raritan.rpc.firmware.ImageInfo, DecodeException)
            return (_ret_, info)

    class _startUpdate(Interface.Method):
        name = 'startUpdate'

        @staticmethod
        def encode(flags):
            for x0 in flags:
                typecheck.is_enum(x0, raritan.rpc.firmware.UpdateFlags, AssertionError)
            args = {}
            args['flags'] = [raritan.rpc.firmware.UpdateFlags.encode(x0) for x0 in flags]
            return args

        @staticmethod
        def decode(rsp, agent):
            return None
    def __init__(self, target, agent):
        super(Firmware, self).__init__(target, agent)
        self.reboot = Firmware._reboot(self)
        self.factoryReset = Firmware._factoryReset(self)
        self.getVersion = Firmware._getVersion(self)
        self.getUpdateHistory = Firmware._getUpdateHistory(self)
        self.getImageStatus = Firmware._getImageStatus(self)
        self.discardImage = Firmware._discardImage(self)
        self.getImageInfo = Firmware._getImageInfo(self)
        self.startUpdate = Firmware._startUpdate(self)
# Do NOT edit this file!
# It was generated by IdlC class idl.json.python.ProxyAsnVisitor.

#
# Section generated from "/home/nb/builds/MEGA/px2-3.2.30-3.2.39-branch-20160511-none-release-none-pdu-raritan/fwcomponents/mkdist/tmp/px2_final/libisys/src/idl/FirmwareUpdateStatus.idl"
#

import raritan.rpc
from raritan.rpc import Interface, Structure, ValueObject, Enumeration, typecheck, DecodeException
import raritan.rpc.firmware


# structure
class UpdateStatus(Structure):
    idlType = "firmware.UpdateStatus:1.0.0"
    elements = ["state", "elapsed", "estimated", "error_message"]

    def __init__(self, state, elapsed, estimated, error_message):
        typecheck.is_string(state, AssertionError)
        typecheck.is_int(elapsed, AssertionError)
        typecheck.is_int(estimated, AssertionError)
        typecheck.is_string(error_message, AssertionError)

        self.state = state
        self.elapsed = elapsed
        self.estimated = estimated
        self.error_message = error_message

    @classmethod
    def decode(cls, json, agent):
        obj = cls(
            state = json['state'],
            elapsed = json['elapsed'],
            estimated = json['estimated'],
            error_message = json['error_message'],
        )
        return obj

    def encode(self):
        json = {}
        json['state'] = self.state
        json['elapsed'] = self.elapsed
        json['estimated'] = self.estimated
        json['error_message'] = self.error_message
        return json

# interface
class FirmwareUpdateStatus(Interface):
    idlType = "firmware.FirmwareUpdateStatus:1.0.0"

    class _getStatus(Interface.Method):
        name = 'getStatus'

        @staticmethod
        def encode():
            args = {}
            return args

        @staticmethod
        def decode(rsp, agent):
            _ret_ = raritan.rpc.firmware.UpdateStatus.decode(rsp['_ret_'], agent)
            typecheck.is_struct(_ret_, raritan.rpc.firmware.UpdateStatus, DecodeException)
            return _ret_
    def __init__(self, target, agent):
        super(FirmwareUpdateStatus, self).__init__(target, agent)
        self.getStatus = FirmwareUpdateStatus._getStatus(self)
