# Do NOT edit this file!
# It was generated by IdlC from EventService.idl.

use strict;

package Raritan::RPC::event::Service_1_0_1;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "event.Service:1.0.1";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::event::Service_1_0_1::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant INVALID_CHANNEL => 1;


sub createChannel($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'createChannel', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::ObjectCodec::decode($agent, $rsp->{'_ret_'}, 'event.Channel');
    return $_ret_;
}


sub destroyChannel($$) {
    my ($self, $channel) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'channel'} = Raritan::RPC::ObjectCodec::encode($channel);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'destroyChannel', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::idl::Event;

sub pushEvent($$) {
    my ($self, $event) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'event'} = Raritan::RPC::ValObjCodec::encode($event);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'pushEvent', $args);
}

use Raritan::RPC::idl::Event;

sub pushEvents($$) {
    my ($self, $events) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'events'} = [];
    for (my $i0 = 0; $i0 <= $#{$events}; $i0++) {
        $args->{'events'}->[$i0] = Raritan::RPC::ValObjCodec::encode($events->[$i0]);
    }
    my $rsp = $agent->json_rpc($self->{'rid'}, 'pushEvents', $args);
}

Raritan::RPC::Registry::registerProxyClass('event.Service', 1, 0, 1, 'Raritan::RPC::event::Service_1_0_1');
1;
