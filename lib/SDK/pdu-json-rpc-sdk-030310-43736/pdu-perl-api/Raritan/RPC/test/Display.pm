# Do NOT edit this file!
# It was generated by IdlC from TestDisplay.idl.

use strict;

package Raritan::RPC::test::Display;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "test.Display:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::test::Display::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::test::Display::Info;

sub getInfo($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getInfo', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::test::Display::Info::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

sub testSequence($$) {
    my ($self, $cycleTime_ms) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'cycleTime_ms'} = 1 * $cycleTime_ms;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'testSequence', $args);
}

Raritan::RPC::Registry::registerProxyClass('test.Display', 1, 0, 0, 'Raritan::RPC::test::Display');
1;