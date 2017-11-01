# Do NOT edit this file!
# It was generated by IdlC from PeripheralDeviceManager.idl.

use strict;

package Raritan::RPC::peripheral::DeviceManager_2_0_2::DeviceTypeInfo;

use Raritan::RPC::sensors::Sensor_4_0_1::TypeSpec;
use Raritan::RPC::sensors::NumericSensor_4_0_1::Range;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'type'} = Raritan::RPC::sensors::Sensor_4_0_1::TypeSpec::encode($in->{'type'});
    $encoded->{'isActuator'} = ($in->{'isActuator'}) ? JSON::true : JSON::false;
    $encoded->{'identifier'} = "$in->{'identifier'}";
    $encoded->{'name'} = "$in->{'name'}";
    $encoded->{'defaultRange'} = Raritan::RPC::sensors::NumericSensor_4_0_1::Range::encode($in->{'defaultRange'});
    $encoded->{'defaultDecDigits'} = 1 * $in->{'defaultDecDigits'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'type'} = Raritan::RPC::sensors::Sensor_4_0_1::TypeSpec::decode($agent, $in->{'type'});
    $decoded->{'isActuator'} = ($in->{'isActuator'}) ? 1 : 0;
    $decoded->{'identifier'} = $in->{'identifier'};
    $decoded->{'name'} = $in->{'name'};
    $decoded->{'defaultRange'} = Raritan::RPC::sensors::NumericSensor_4_0_1::Range::decode($agent, $in->{'defaultRange'});
    $decoded->{'defaultDecDigits'} = $in->{'defaultDecDigits'};
    return $decoded;
}

1;
