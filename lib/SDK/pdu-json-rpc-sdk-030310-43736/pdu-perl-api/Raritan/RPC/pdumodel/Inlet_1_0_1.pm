# Do NOT edit this file!
# It was generated by IdlC from Inlet.idl.

use strict;

package Raritan::RPC::pdumodel::Inlet_1_0_1;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "pdumodel.Inlet:1.0.1";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::pdumodel::Inlet_1_0_1::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::pdumodel::Inlet_1_0_1::MetaData;

sub getMetaData($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getMetaData', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::Inlet_1_0_1::MetaData::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::pdumodel::Inlet_1_0_1::Sensors;

sub getSensors($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSensors', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::Inlet_1_0_1::Sensors::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::pdumodel::Pole;

sub getPoles($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getPoles', $args);
    my $_ret_;
    $_ret_ = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'_ret_'}}; $i0++) {
        $_ret_->[$i0] = Raritan::RPC::pdumodel::Pole::decode($agent, $rsp->{'_ret_'}->[$i0]);
    }
    return $_ret_;
}

use Raritan::RPC::pdumodel::Inlet_1_0_1::Settings;

sub getSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::Inlet_1_0_1::Settings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::pdumodel::Inlet_1_0_1::Settings;

sub setSettings($$) {
    my ($self, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'settings'} = Raritan::RPC::pdumodel::Inlet_1_0_1::Settings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('pdumodel.Inlet', 1, 0, 1, 'Raritan::RPC::pdumodel::Inlet_1_0_1');
1;