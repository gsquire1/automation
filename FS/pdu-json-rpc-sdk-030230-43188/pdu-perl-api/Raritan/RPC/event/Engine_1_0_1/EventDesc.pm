# Do NOT edit this file!
# It was generated by IdlC from EventEngine.idl.

use strict;

package Raritan::RPC::event::Engine_1_0_1::EventDesc;

use Raritan::RPC::event::Engine_1_0_1::EventDesc;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'eventDescType'} = $in->{'eventDescType'};
    $encoded->{'eventType'} = $in->{'eventType'};
    $encoded->{'dynNodeContext'} = "$in->{'dynNodeContext'}";
    $encoded->{'idComp'} = "$in->{'idComp'}";
    $encoded->{'name'} = "$in->{'name'}";
    $encoded->{'entries'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'entries'}}; $i0++) {
        $encoded->{'entries'}->[$i0] = Raritan::RPC::event::Engine_1_0_1::EventDesc::encode($in->{'entries'}->[$i0]);
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'eventDescType'} = $in->{'eventDescType'};
    $decoded->{'eventType'} = $in->{'eventType'};
    $decoded->{'dynNodeContext'} = $in->{'dynNodeContext'};
    $decoded->{'idComp'} = $in->{'idComp'};
    $decoded->{'name'} = $in->{'name'};
    $decoded->{'entries'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'entries'}}; $i0++) {
        $decoded->{'entries'}->[$i0] = Raritan::RPC::event::Engine_1_0_1::EventDesc::decode($agent, $in->{'entries'}->[$i0]);
    }
    return $decoded;
}

1;
