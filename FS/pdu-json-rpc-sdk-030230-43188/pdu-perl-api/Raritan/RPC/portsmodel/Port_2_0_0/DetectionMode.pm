# Do NOT edit this file!
# It was generated by IdlC from Port.idl.

use strict;

package Raritan::RPC::portsmodel::Port_2_0_0::DetectionMode;


sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'type'} = $in->{'type'};
    $encoded->{'pinnedDeviceType'} = "$in->{'pinnedDeviceType'}";
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'type'} = $in->{'type'};
    $decoded->{'pinnedDeviceType'} = $in->{'pinnedDeviceType'};
    return $decoded;
}

1;
