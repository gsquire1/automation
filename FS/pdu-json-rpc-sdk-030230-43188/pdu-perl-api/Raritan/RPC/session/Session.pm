# Do NOT edit this file!
# It was generated by IdlC from SessionManager.idl.

use strict;

package Raritan::RPC::session::Session;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'token'} = "$in->{'token'}";
    $encoded->{'username'} = "$in->{'username'}";
    $encoded->{'remoteIp'} = "$in->{'remoteIp'}";
    $encoded->{'clientType'} = "$in->{'clientType'}";
    $encoded->{'creationTime'} = 1 * $in->{'creationTime'};
    $encoded->{'timeout'} = 1 * $in->{'timeout'};
    $encoded->{'idle'} = 1 * $in->{'idle'};
    $encoded->{'userIdle'} = 1 * $in->{'userIdle'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'token'} = $in->{'token'};
    $decoded->{'username'} = $in->{'username'};
    $decoded->{'remoteIp'} = $in->{'remoteIp'};
    $decoded->{'clientType'} = $in->{'clientType'};
    $decoded->{'creationTime'} = $in->{'creationTime'};
    $decoded->{'timeout'} = $in->{'timeout'};
    $decoded->{'idle'} = $in->{'idle'};
    $decoded->{'userIdle'} = $in->{'userIdle'};
    return $decoded;
}

1;
