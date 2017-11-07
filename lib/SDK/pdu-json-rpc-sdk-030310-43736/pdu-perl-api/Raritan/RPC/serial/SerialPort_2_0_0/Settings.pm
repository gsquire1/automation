# Do NOT edit this file!
# It was generated by IdlC from SerialPort.idl.

use strict;

package Raritan::RPC::serial::SerialPort_2_0_0::Settings;


sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'consoleBaudRate'} = $in->{'consoleBaudRate'};
    $encoded->{'modemBaudRate'} = $in->{'modemBaudRate'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'consoleBaudRate'} = $in->{'consoleBaudRate'};
    $decoded->{'modemBaudRate'} = $in->{'modemBaudRate'};
    return $decoded;
}

1;