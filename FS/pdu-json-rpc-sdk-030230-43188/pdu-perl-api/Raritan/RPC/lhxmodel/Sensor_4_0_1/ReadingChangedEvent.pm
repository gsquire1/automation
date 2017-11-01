# Do NOT edit this file!
# It was generated by IdlC from LhxSensor.idl.

use strict;

package Raritan::RPC::lhxmodel::Sensor_4_0_1::ReadingChangedEvent;

use constant typeId => "lhxmodel.Sensor_4_0_1.ReadingChangedEvent:1.0.0";
use Raritan::RPC::lhxmodel::Sensor_4_0_1::Reading;
use Raritan::RPC::idl::Event;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::idl::Event::encode($in);
    $encoded->{'newReading'} = Raritan::RPC::lhxmodel::Sensor_4_0_1::Reading::encode($in->{'newReading'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::idl::Event::decode($agent, $in);
    $decoded->{'newReading'} = Raritan::RPC::lhxmodel::Sensor_4_0_1::Reading::decode($agent, $in->{'newReading'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('lhxmodel.Sensor_4_0_1.ReadingChangedEvent', 1, 0, 0, 'Raritan::RPC::lhxmodel::Sensor_4_0_1::ReadingChangedEvent');
1;
