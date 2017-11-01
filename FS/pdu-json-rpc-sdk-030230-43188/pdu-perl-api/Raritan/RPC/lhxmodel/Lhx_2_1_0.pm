# Do NOT edit this file!
# It was generated by IdlC from Lhx.idl.

use strict;

package Raritan::RPC::lhxmodel::Lhx_2_1_0;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "lhxmodel.Lhx:2.1.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::lhxmodel::Lhx_2_1_0::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant ERR_INVALID_PARAMS => 1;

use Raritan::RPC::lhxmodel::Lhx_2_1_0::MetaData;

sub getMetaData($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getMetaData', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::lhxmodel::Lhx_2_1_0::MetaData::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::lhxmodel::Lhx_2_1_0::Settings;

sub getSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::lhxmodel::Lhx_2_1_0::Settings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::lhxmodel::Lhx_2_1_0::Settings;

sub setSettings($$) {
    my ($self, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'settings'} = Raritan::RPC::lhxmodel::Lhx_2_1_0::Settings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::lhxmodel::Lhx_2_1_0::Sensors;

sub getSensors($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSensors', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::lhxmodel::Lhx_2_1_0::Sensors::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::lhxmodel::Lhx_2_1_0::OpState;

sub getOpState($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getOpState', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::lhxmodel::Lhx_2_1_0::OpState::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}


sub setPowerState($$) {
    my ($self, $state) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'state'} = $state;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setPowerState', $args);
}


sub getParameters($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getParameters', $args);
    my $_ret_;
    $_ret_ = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'_ret_'}}; $i0++) {
        $_ret_->[$i0] = Raritan::RPC::ObjectCodec::decode($agent, $rsp->{'_ret_'}->[$i0], 'lhxmodel.Parameter');
    }
    return $_ret_;
}


sub getActualValues($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getActualValues', $args);
    my $_ret_;
    $_ret_ = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'_ret_'}}; $i0++) {
        $_ret_->[$i0] = Raritan::RPC::ObjectCodec::decode($agent, $rsp->{'_ret_'}->[$i0], 'lhxmodel.Parameter');
    }
    return $_ret_;
}

sub requestMaximumCooling($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'requestMaximumCooling', $args);
}

sub acknowledgeAlertStatus($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'acknowledgeAlertStatus', $args);
}

Raritan::RPC::Registry::registerProxyClass('lhxmodel.Lhx', 2, 1, 0, 'Raritan::RPC::lhxmodel::Lhx_2_1_0');
1;
