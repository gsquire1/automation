# Do NOT edit this file!
# It was generated by IdlC from Panel.idl.

use strict;

package Raritan::RPC::pdumodel::Panel;

use parent qw(Raritan::RPC::pdumodel::PowerMeter);

use constant typeId => "pdumodel.Panel:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::pdumodel::Panel::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::pdumodel::Panel::PanelSettings;

sub getPanelSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getPanelSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::Panel::PanelSettings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::pdumodel::Panel::PanelSettings;

sub setPanelSettings($$) {
    my ($self, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'settings'} = Raritan::RPC::pdumodel::Panel::PanelSettings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setPanelSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}


sub getCircuits($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getCircuits', $args);
    my $_ret_;
    $_ret_ = {};
    for (my $i0 = 0; $i0 <= $#{$rsp->{'_ret_'}}; $i0++) {
        my $key0 = $rsp->{'_ret_'}->[$i0]->{'key'};
        my $value0 = Raritan::RPC::ObjectCodec::decode($agent, $rsp->{'_ret_'}->[$i0]->{'value'}, 'pdumodel.Circuit');
        $_ret_->{$key0} = $value0;
    }
    return $_ret_;
}

use Raritan::RPC::pdumodel::Circuit::Settings;
use Raritan::RPC::pdumodel::Circuit::Config;

sub createCircuit($$$$) {
    my ($self, $circuit, $config, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'config'} = Raritan::RPC::pdumodel::Circuit::Config::encode($config);
    $args->{'settings'} = Raritan::RPC::pdumodel::Circuit::Settings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'createCircuit', $args);
    $$circuit = Raritan::RPC::ObjectCodec::decode($agent, $rsp->{'circuit'}, 'pdumodel.Circuit');
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub deleteCircuit($$) {
    my ($self, $position) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'position'} = 1 * $position;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'deleteCircuit', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('pdumodel.Panel', 1, 0, 0, 'Raritan::RPC::pdumodel::Panel');
1;
