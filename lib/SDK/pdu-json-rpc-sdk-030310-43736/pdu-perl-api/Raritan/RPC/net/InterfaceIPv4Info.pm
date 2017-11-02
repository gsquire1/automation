# Do NOT edit this file!
# It was generated by IdlC from Net.idl.

use strict;

package Raritan::RPC::net::InterfaceIPv4Info;

use Raritan::RPC::net::IpAddrCidr;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'enabled'} = ($in->{'enabled'}) ? JSON::true : JSON::false;
    $encoded->{'configMethod'} = $in->{'configMethod'};
    $encoded->{'addrsCidr'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'addrsCidr'}}; $i0++) {
        $encoded->{'addrsCidr'}->[$i0] = Raritan::RPC::net::IpAddrCidr::encode($in->{'addrsCidr'}->[$i0]);
    }
    $encoded->{'dhcpServerAddr'} = "$in->{'dhcpServerAddr'}";
    $encoded->{'dhcpPreferredHostname'} = "$in->{'dhcpPreferredHostname'}";
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'enabled'} = ($in->{'enabled'}) ? 1 : 0;
    $decoded->{'configMethod'} = $in->{'configMethod'};
    $decoded->{'addrsCidr'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'addrsCidr'}}; $i0++) {
        $decoded->{'addrsCidr'}->[$i0] = Raritan::RPC::net::IpAddrCidr::decode($agent, $in->{'addrsCidr'}->[$i0]);
    }
    $decoded->{'dhcpServerAddr'} = $in->{'dhcpServerAddr'};
    $decoded->{'dhcpPreferredHostname'} = $in->{'dhcpPreferredHostname'};
    return $decoded;
}

1;
