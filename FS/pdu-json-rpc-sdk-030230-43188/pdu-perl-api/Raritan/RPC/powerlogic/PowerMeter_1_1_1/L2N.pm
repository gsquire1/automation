# Do NOT edit this file!
# It was generated by IdlC from PowerLogicPowerMeter.idl.

use strict;

package Raritan::RPC::powerlogic::PowerMeter_1_1_1::L2N;

use Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading;
use Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading;
use Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'l1'} = Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading::encode($in->{'l1'});
    $encoded->{'l2'} = Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading::encode($in->{'l2'});
    $encoded->{'l3'} = Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading::encode($in->{'l3'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'l1'} = Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading::decode($agent, $in->{'l1'});
    $decoded->{'l2'} = Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading::decode($agent, $in->{'l2'});
    $decoded->{'l3'} = Raritan::RPC::powerlogic::PowerMeter_1_1_1::MinMaxReading::decode($agent, $in->{'l3'});
    return $decoded;
}

1;
