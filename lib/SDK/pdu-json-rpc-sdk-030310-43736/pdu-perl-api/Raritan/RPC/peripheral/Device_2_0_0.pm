# Do NOT edit this file!
# It was generated by IdlC from PeripheralDeviceSlot.idl.

use strict;

package Raritan::RPC::peripheral::Device_2_0_0;

use constant typeId => "peripheral.Device:2.0.0";
use Raritan::RPC::peripheral::DeviceID_2_0_0;
use Raritan::RPC::peripheral::PosElement;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'deviceID'} = Raritan::RPC::peripheral::DeviceID_2_0_0::encode($in->{'deviceID'});
    $encoded->{'position'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'position'}}; $i0++) {
        $encoded->{'position'}->[$i0] = Raritan::RPC::peripheral::PosElement::encode($in->{'position'}->[$i0]);
    }
    $encoded->{'packageClass'} = "$in->{'packageClass'}";
    $encoded->{'device'} = Raritan::RPC::ObjectCodec::encode($in->{'device'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'deviceID'} = Raritan::RPC::peripheral::DeviceID_2_0_0::decode($agent, $in->{'deviceID'});
    $decoded->{'position'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'position'}}; $i0++) {
        $decoded->{'position'}->[$i0] = Raritan::RPC::peripheral::PosElement::decode($agent, $in->{'position'}->[$i0]);
    }
    $decoded->{'packageClass'} = $in->{'packageClass'};
    $decoded->{'device'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'device'}, 'sensors.Sensor');
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('peripheral.Device', 2, 0, 0, 'Raritan::RPC::peripheral::Device_2_0_0');
1;
