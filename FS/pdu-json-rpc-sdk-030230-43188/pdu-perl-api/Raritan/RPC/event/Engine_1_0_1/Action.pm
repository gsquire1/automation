# Do NOT edit this file!
# It was generated by IdlC from EventEngine.idl.

use strict;

package Raritan::RPC::event::Engine_1_0_1::Action;

use Raritan::RPC::event::KeyValue;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'id'} = "$in->{'id'}";
    $encoded->{'name'} = "$in->{'name'}";
    $encoded->{'isSystem'} = ($in->{'isSystem'}) ? JSON::true : JSON::false;
    $encoded->{'type'} = "$in->{'type'}";
    $encoded->{'arguments'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'arguments'}}; $i0++) {
        $encoded->{'arguments'}->[$i0] = Raritan::RPC::event::KeyValue::encode($in->{'arguments'}->[$i0]);
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'id'} = $in->{'id'};
    $decoded->{'name'} = $in->{'name'};
    $decoded->{'isSystem'} = ($in->{'isSystem'}) ? 1 : 0;
    $decoded->{'type'} = $in->{'type'};
    $decoded->{'arguments'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'arguments'}}; $i0++) {
        $decoded->{'arguments'}->[$i0] = Raritan::RPC::event::KeyValue::decode($agent, $in->{'arguments'}->[$i0]);
    }
    return $decoded;
}

1;
