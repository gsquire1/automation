# Do NOT edit this file!
# It was generated by IdlC from SerialPort.idl.

use strict;

package Raritan::RPC::serial::SerialPort_3_0_0;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "serial.SerialPort:3.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::serial::SerialPort_3_0_0::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant SUCCESS => 0;

use constant ERR_INVALID_VALUE => 1;

use Raritan::RPC::serial::SerialPort_3_0_0::Settings;

sub getSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::serial::SerialPort_3_0_0::Settings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::serial::SerialPort_3_0_0::Settings;

sub setSettings($$) {
    my ($self, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'settings'} = Raritan::RPC::serial::SerialPort_3_0_0::Settings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::serial::SerialPort_3_0_0::State;

sub getState($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getState', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::serial::SerialPort_3_0_0::State::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

sub getModem($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getModem', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::ObjectCodec::decode($agent, $rsp->{'_ret_'}, 'idl.Object');
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('serial.SerialPort', 3, 0, 0, 'Raritan::RPC::serial::SerialPort_3_0_0');
1;
