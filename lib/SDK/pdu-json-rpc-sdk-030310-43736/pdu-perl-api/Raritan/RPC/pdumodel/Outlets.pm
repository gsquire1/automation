# Do NOT edit this file!
# It was generated by IdlC from Outlets.idl.

use strict;

package Raritan::RPC::pdumodel::Outlets;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "pdumodel.Outlets:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::pdumodel::Outlets::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::pdumodel::Outlets::Info;

sub getInfo($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getInfo', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::Outlets::Info::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('pdumodel.Outlets', 1, 0, 0, 'Raritan::RPC::pdumodel::Outlets');
1;