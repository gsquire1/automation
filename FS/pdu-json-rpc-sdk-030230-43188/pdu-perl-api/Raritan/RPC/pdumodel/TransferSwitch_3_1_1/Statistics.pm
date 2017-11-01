# Do NOT edit this file!
# It was generated by IdlC from TransferSwitch.idl.

use strict;

package Raritan::RPC::pdumodel::TransferSwitch_3_1_1::Statistics;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'transferCount'} = 1 * $in->{'transferCount'};
    $encoded->{'powerFailDetectTime'} = 1 * $in->{'powerFailDetectTime'};
    $encoded->{'relayOpenTime'} = 1 * $in->{'relayOpenTime'};
    $encoded->{'totalTransferTime'} = 1 * $in->{'totalTransferTime'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'transferCount'} = $in->{'transferCount'};
    $decoded->{'powerFailDetectTime'} = $in->{'powerFailDetectTime'};
    $decoded->{'relayOpenTime'} = $in->{'relayOpenTime'};
    $decoded->{'totalTransferTime'} = $in->{'totalTransferTime'};
    return $decoded;
}

1;
