# Do NOT edit this file!
# It was generated by IdlC from Security.idl.

use strict;

package Raritan::RPC::security::IpFw;

use Raritan::RPC::security::IpfwRuleset;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'enabled'} = ($in->{'enabled'}) ? JSON::true : JSON::false;
    $encoded->{'defaultPolicy'} = $in->{'defaultPolicy'};
    $encoded->{'ruleSet'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'ruleSet'}}; $i0++) {
        $encoded->{'ruleSet'}->[$i0] = Raritan::RPC::security::IpfwRuleset::encode($in->{'ruleSet'}->[$i0]);
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'enabled'} = ($in->{'enabled'}) ? 1 : 0;
    $decoded->{'defaultPolicy'} = $in->{'defaultPolicy'};
    $decoded->{'ruleSet'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'ruleSet'}}; $i0++) {
        $decoded->{'ruleSet'}->[$i0] = Raritan::RPC::security::IpfwRuleset::decode($agent, $in->{'ruleSet'}->[$i0]);
    }
    return $decoded;
}

1;
