# Do NOT edit this file!
# It was generated by IdlC from testrpc.idl.

use strict;

package Raritan::RPC::test::Control;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "test.Control:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::test::Control::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

sub isTestMode($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'isTestMode', $args);
    my $_ret_;
    $_ret_ = ($rsp->{'_ret_'}) ? 1 : 0;
    return $_ret_;
}

sub setTestMode($$) {
    my ($self, $isTestModeOn) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'isTestModeOn'} = ($isTestModeOn) ? JSON::true : JSON::false;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setTestMode', $args);
}

Raritan::RPC::Registry::registerProxyClass('test.Control', 1, 0, 0, 'Raritan::RPC::test::Control');
1;
