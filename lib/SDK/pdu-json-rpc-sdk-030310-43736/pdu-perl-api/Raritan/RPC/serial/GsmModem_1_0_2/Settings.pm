# Do NOT edit this file!
# It was generated by IdlC from GsmModem.idl.

use strict;

package Raritan::RPC::serial::GsmModem_1_0_2::Settings;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'pin'} = "$in->{'pin'}";
    $encoded->{'smsc'} = "$in->{'smsc'}";
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'pin'} = $in->{'pin'};
    $decoded->{'smsc'} = $in->{'smsc'};
    return $decoded;
}

1;
