# Do NOT edit this file!
# It was generated by IdlC from EventEngine.idl.

use strict;

package Raritan::RPC::event::Engine::Condition;

use Raritan::RPC::event::Engine::Condition;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'negate'} = ($in->{'negate'}) ? JSON::true : JSON::false;
    $encoded->{'operation'} = $in->{'operation'};
    $encoded->{'matchType'} = $in->{'matchType'};
    $encoded->{'eventId'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'eventId'}}; $i0++) {
        $encoded->{'eventId'}->[$i0] = "$in->{'eventId'}->[$i0]";
    }
    $encoded->{'conditions'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'conditions'}}; $i0++) {
        $encoded->{'conditions'}->[$i0] = Raritan::RPC::event::Engine::Condition::encode($in->{'conditions'}->[$i0]);
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'negate'} = ($in->{'negate'}) ? 1 : 0;
    $decoded->{'operation'} = $in->{'operation'};
    $decoded->{'matchType'} = $in->{'matchType'};
    $decoded->{'eventId'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'eventId'}}; $i0++) {
        $decoded->{'eventId'}->[$i0] = $in->{'eventId'}->[$i0];
    }
    $decoded->{'conditions'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'conditions'}}; $i0++) {
        $decoded->{'conditions'}->[$i0] = Raritan::RPC::event::Engine::Condition::decode($agent, $in->{'conditions'}->[$i0]);
    }
    return $decoded;
}

1;
