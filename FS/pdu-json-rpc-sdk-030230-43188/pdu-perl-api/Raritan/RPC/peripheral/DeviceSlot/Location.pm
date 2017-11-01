# Do NOT edit this file!
# It was generated by IdlC from PeripheralDeviceSlot.idl.

use strict;

package Raritan::RPC::peripheral::DeviceSlot::Location;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'x'} = "$in->{'x'}";
    $encoded->{'y'} = "$in->{'y'}";
    $encoded->{'z'} = "$in->{'z'}";
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'x'} = $in->{'x'};
    $decoded->{'y'} = $in->{'y'};
    $decoded->{'z'} = $in->{'z'};
    return $decoded;
}

1;
