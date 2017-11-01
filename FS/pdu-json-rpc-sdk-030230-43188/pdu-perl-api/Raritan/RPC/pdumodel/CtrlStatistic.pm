# Do NOT edit this file!
# It was generated by IdlC from Controller.idl.

use strict;

package Raritan::RPC::pdumodel::CtrlStatistic;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'masterCSumErrCnt'} = 1 * $in->{'masterCSumErrCnt'};
    $encoded->{'slaveCSumErrCnt'} = 1 * $in->{'slaveCSumErrCnt'};
    $encoded->{'timeoutCnt'} = 1 * $in->{'timeoutCnt'};
    $encoded->{'resetCnt'} = 1 * $in->{'resetCnt'};
    $encoded->{'emResetCnt'} = 1 * $in->{'emResetCnt'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'masterCSumErrCnt'} = $in->{'masterCSumErrCnt'};
    $decoded->{'slaveCSumErrCnt'} = $in->{'slaveCSumErrCnt'};
    $decoded->{'timeoutCnt'} = $in->{'timeoutCnt'};
    $decoded->{'resetCnt'} = $in->{'resetCnt'};
    $decoded->{'emResetCnt'} = $in->{'emResetCnt'};
    return $decoded;
}

1;
