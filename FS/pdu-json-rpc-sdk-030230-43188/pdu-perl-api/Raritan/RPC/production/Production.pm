# Do NOT edit this file!
# It was generated by IdlC from Production.idl.

use strict;

package Raritan::RPC::production::Production;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "production.Production:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::production::Production::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

sub enterFactoryConfigMode($$) {
    my ($self, $password) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'password'} = "$password";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'enterFactoryConfigMode', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub leaveFactoryConfigMode($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'leaveFactoryConfigMode', $args);
}

sub isFactoryConfigModeEnabled($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'isFactoryConfigModeEnabled', $args);
    my $_ret_;
    $_ret_ = ($rsp->{'_ret_'}) ? 1 : 0;
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('production.Production', 1, 0, 0, 'Raritan::RPC::production::Production');
1;
