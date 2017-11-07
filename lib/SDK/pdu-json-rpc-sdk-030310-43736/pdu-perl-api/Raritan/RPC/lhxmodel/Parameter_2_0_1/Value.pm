# Do NOT edit this file!
# It was generated by IdlC from LhxParameter.idl.

use strict;

package Raritan::RPC::lhxmodel::Parameter_2_0_1::Value;

use Raritan::RPC::lhxmodel::Parameter_2_0_1::Status;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'timestamp'} = 1 * $in->{'timestamp'};
    $encoded->{'status'} = Raritan::RPC::lhxmodel::Parameter_2_0_1::Status::encode($in->{'status'});
    $encoded->{'value'} = 1 * $in->{'value'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'timestamp'} = $in->{'timestamp'};
    $decoded->{'status'} = Raritan::RPC::lhxmodel::Parameter_2_0_1::Status::decode($agent, $in->{'status'});
    $decoded->{'value'} = $in->{'value'};
    return $decoded;
}

1;