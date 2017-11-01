# Do NOT edit this file!
# It was generated by IdlC from Webcam.idl.

use strict;

package Raritan::RPC::webcam::Format;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'x'} = 1 * $in->{'x'};
    $encoded->{'y'} = 1 * $in->{'y'};
    $encoded->{'pixelFormat'} = 1 * $in->{'pixelFormat'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'x'} = $in->{'x'};
    $decoded->{'y'} = $in->{'y'};
    $decoded->{'pixelFormat'} = $in->{'pixelFormat'};
    return $decoded;
}

1;
