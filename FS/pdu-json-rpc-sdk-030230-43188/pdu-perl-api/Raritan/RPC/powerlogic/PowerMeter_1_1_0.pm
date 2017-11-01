# Do NOT edit this file!
# It was generated by IdlC from PowerLogicPowerMeter.idl.

use strict;

package Raritan::RPC::powerlogic::PowerMeter_1_1_0;

use parent qw(Raritan::RPC::modbus::Device);

use constant typeId => "powerlogic.PowerMeter:1.1.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::powerlogic::PowerMeter_1_1_0::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::powerlogic::PowerMeter_1_1_0::Sensors;

sub getSensors($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSensors', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::powerlogic::PowerMeter_1_1_0::Sensors::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::powerlogic::PowerMeter_1_1_0::Setup;

sub getSetup($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSetup', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::powerlogic::PowerMeter_1_1_0::Setup::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::powerlogic::PowerMeter_1_1_0::ErrorStatus;

sub getErrorStatus($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getErrorStatus', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::powerlogic::PowerMeter_1_1_0::ErrorStatus::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

sub resetAllMinMaxValues($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'resetAllMinMaxValues', $args);
}

sub clearAllEnergyAccumulators($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'clearAllEnergyAccumulators', $args);
}

Raritan::RPC::Registry::registerProxyClass('powerlogic.PowerMeter', 1, 1, 0, 'Raritan::RPC::powerlogic::PowerMeter_1_1_0');
1;
