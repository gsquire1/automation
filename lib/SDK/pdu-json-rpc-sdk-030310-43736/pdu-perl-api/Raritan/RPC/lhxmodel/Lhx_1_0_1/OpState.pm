# Do NOT edit this file!
# It was generated by IdlC from Lhx.idl.

use strict;

package Raritan::RPC::lhxmodel::Lhx_1_0_1::OpState;

use Raritan::RPC::lhxmodel::Lhx_1_0_1::AlertStatus;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'on'} = ($in->{'on'}) ? JSON::true : JSON::false;
    $encoded->{'alertStatus'} = Raritan::RPC::lhxmodel::Lhx_1_0_1::AlertStatus::encode($in->{'alertStatus'});
    $encoded->{'operatingHoursLhx'} = 1 * $in->{'operatingHoursLhx'};
    $encoded->{'operatingHoursFan'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'operatingHoursFan'}}; $i0++) {
        $encoded->{'operatingHoursFan'}->[$i0] = 1 * $in->{'operatingHoursFan'}->[$i0];
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'on'} = ($in->{'on'}) ? 1 : 0;
    $decoded->{'alertStatus'} = Raritan::RPC::lhxmodel::Lhx_1_0_1::AlertStatus::decode($agent, $in->{'alertStatus'});
    $decoded->{'operatingHoursLhx'} = $in->{'operatingHoursLhx'};
    $decoded->{'operatingHoursFan'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'operatingHoursFan'}}; $i0++) {
        $decoded->{'operatingHoursFan'}->[$i0] = $in->{'operatingHoursFan'}->[$i0];
    }
    return $decoded;
}

1;