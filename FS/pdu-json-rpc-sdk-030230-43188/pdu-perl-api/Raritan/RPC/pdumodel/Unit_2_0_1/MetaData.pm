# Do NOT edit this file!
# It was generated by IdlC from Unit.idl.

use strict;

package Raritan::RPC::pdumodel::Unit_2_0_1::MetaData;


sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'hasOrientationSensor'} = ($in->{'hasOrientationSensor'}) ? JSON::true : JSON::false;
    $encoded->{'supportedDisplayOrientations'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'supportedDisplayOrientations'}}; $i0++) {
        $encoded->{'supportedDisplayOrientations'}->[$i0] = $in->{'supportedDisplayOrientations'}->[$i0];
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'hasOrientationSensor'} = ($in->{'hasOrientationSensor'}) ? 1 : 0;
    $decoded->{'supportedDisplayOrientations'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'supportedDisplayOrientations'}}; $i0++) {
        $decoded->{'supportedDisplayOrientations'}->[$i0] = $in->{'supportedDisplayOrientations'}->[$i0];
    }
    return $decoded;
}

1;
