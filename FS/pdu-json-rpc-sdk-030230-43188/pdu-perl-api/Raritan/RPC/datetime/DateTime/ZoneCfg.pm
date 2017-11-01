# Do NOT edit this file!
# It was generated by IdlC from DateTime.idl.

use strict;

package Raritan::RPC::datetime::DateTime::ZoneCfg;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'id'} = 1 * $in->{'id'};
    $encoded->{'name'} = "$in->{'name'}";
    $encoded->{'enableAutoDST'} = ($in->{'enableAutoDST'}) ? JSON::true : JSON::false;
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'id'} = $in->{'id'};
    $decoded->{'name'} = $in->{'name'};
    $decoded->{'enableAutoDST'} = ($in->{'enableAutoDST'}) ? 1 : 0;
    return $decoded;
}

1;
