# Do NOT edit this file!
# It was generated by IdlC from AnalogModem.idl.

use strict;

package Raritan::RPC::serial::AnalogModem;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "serial.AnalogModem:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::serial::AnalogModem::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant SUCCESS => 0;

use constant ERR_INVALID_VALUE => 1;

use Raritan::RPC::serial::AnalogModem::Settings;

sub getSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::serial::AnalogModem::Settings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::serial::AnalogModem::Settings;

sub setSettings($$) {
    my ($self, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'settings'} = Raritan::RPC::serial::AnalogModem::Settings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('serial.AnalogModem', 1, 0, 0, 'Raritan::RPC::serial::AnalogModem');
1;
