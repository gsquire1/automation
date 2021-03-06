# Do NOT edit this file!
# It was generated by IdlC from SensorLogger.idl.

use strict;

package Raritan::RPC::pdumodel::SensorLogger::SensorSet;


sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'sensors'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'sensors'}}; $i0++) {
        $encoded->{'sensors'}->[$i0] = Raritan::RPC::ObjectCodec::encode($in->{'sensors'}->[$i0]);
    }
    $encoded->{'extsens'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'extsens'}}; $i0++) {
        $encoded->{'extsens'}->[$i0] = Raritan::RPC::ObjectCodec::encode($in->{'extsens'}->[$i0]);
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'sensors'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'sensors'}}; $i0++) {
        $decoded->{'sensors'}->[$i0] = Raritan::RPC::ObjectCodec::decode($agent, $in->{'sensors'}->[$i0], 'sensors.Sensor');
    }
    $decoded->{'extsens'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'extsens'}}; $i0++) {
        $decoded->{'extsens'}->[$i0] = Raritan::RPC::ObjectCodec::decode($agent, $in->{'extsens'}->[$i0], 'sensors.ExternalSensorSlot');
    }
    return $decoded;
}

1;
