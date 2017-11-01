# Do NOT edit this file!
# It was generated by IdlC from Pdu.idl.

use strict;

package Raritan::RPC::pdumodel::Pdu_2_2_3::Statistic;

use Raritan::RPC::peripheral::DeviceManager_1_0_3::Statistics;
use Raritan::RPC::pdumodel::CtrlStatistic;
use Raritan::RPC::pdumodel::OutletStatistic;
use Raritan::RPC::pdumodel::CircuitBreakerStatistic;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'cbStats'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'cbStats'}}; $i0++) {
        $encoded->{'cbStats'}->[$i0] = Raritan::RPC::pdumodel::CircuitBreakerStatistic::encode($in->{'cbStats'}->[$i0]);
    }
    $encoded->{'ctrlStats'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'ctrlStats'}}; $i0++) {
        $encoded->{'ctrlStats'}->[$i0] = Raritan::RPC::pdumodel::CtrlStatistic::encode($in->{'ctrlStats'}->[$i0]);
    }
    $encoded->{'outletStats'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'outletStats'}}; $i0++) {
        $encoded->{'outletStats'}->[$i0] = Raritan::RPC::pdumodel::OutletStatistic::encode($in->{'outletStats'}->[$i0]);
    }
    $encoded->{'peripheralStats'} = Raritan::RPC::peripheral::DeviceManager_1_0_3::Statistics::encode($in->{'peripheralStats'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'cbStats'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'cbStats'}}; $i0++) {
        $decoded->{'cbStats'}->[$i0] = Raritan::RPC::pdumodel::CircuitBreakerStatistic::decode($agent, $in->{'cbStats'}->[$i0]);
    }
    $decoded->{'ctrlStats'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'ctrlStats'}}; $i0++) {
        $decoded->{'ctrlStats'}->[$i0] = Raritan::RPC::pdumodel::CtrlStatistic::decode($agent, $in->{'ctrlStats'}->[$i0]);
    }
    $decoded->{'outletStats'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'outletStats'}}; $i0++) {
        $decoded->{'outletStats'}->[$i0] = Raritan::RPC::pdumodel::OutletStatistic::decode($agent, $in->{'outletStats'}->[$i0]);
    }
    $decoded->{'peripheralStats'} = Raritan::RPC::peripheral::DeviceManager_1_0_3::Statistics::decode($agent, $in->{'peripheralStats'});
    return $decoded;
}

1;
