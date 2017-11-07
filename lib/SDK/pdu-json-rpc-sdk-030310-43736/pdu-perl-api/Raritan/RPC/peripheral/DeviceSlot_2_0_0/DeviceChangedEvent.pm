# Do NOT edit this file!
# It was generated by IdlC from PeripheralDeviceSlot.idl.

use strict;

package Raritan::RPC::peripheral::DeviceSlot_2_0_0::DeviceChangedEvent;

use constant typeId => "peripheral.DeviceSlot_2_0_0.DeviceChangedEvent:1.0.0";
use Raritan::RPC::peripheral::Device_2_0_0;
use Raritan::RPC::peripheral::Device_2_0_0;
use Raritan::RPC::idl::Event;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::idl::Event::encode($in);
    $encoded->{'oldDevice'} = Raritan::RPC::ValObjCodec::encode($in->{'oldDevice'});
    $encoded->{'newDevice'} = Raritan::RPC::ValObjCodec::encode($in->{'newDevice'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::idl::Event::decode($agent, $in);
    $decoded->{'oldDevice'} = Raritan::RPC::ValObjCodec::decode($agent, $in->{'oldDevice'}, 'peripheral.Device');
    $decoded->{'newDevice'} = Raritan::RPC::ValObjCodec::decode($agent, $in->{'newDevice'}, 'peripheral.Device');
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('peripheral.DeviceSlot_2_0_0.DeviceChangedEvent', 1, 0, 0, 'Raritan::RPC::peripheral::DeviceSlot_2_0_0::DeviceChangedEvent');
1;