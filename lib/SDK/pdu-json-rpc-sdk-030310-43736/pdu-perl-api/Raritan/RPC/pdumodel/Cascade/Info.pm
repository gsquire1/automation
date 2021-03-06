# Do NOT edit this file!
# It was generated by IdlC from Cascade.idl.

use strict;

package Raritan::RPC::pdumodel::Cascade::Info;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'pduIds'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'pduIds'}}; $i0++) {
        $encoded->{'pduIds'}->[$i0] = 1 * $in->{'pduIds'}->[$i0];
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'pduIds'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'pduIds'}}; $i0++) {
        $decoded->{'pduIds'}->[$i0] = $in->{'pduIds'}->[$i0];
    }
    return $decoded;
}

1;
