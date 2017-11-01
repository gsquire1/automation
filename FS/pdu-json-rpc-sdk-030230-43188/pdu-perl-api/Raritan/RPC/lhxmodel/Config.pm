# Do NOT edit this file!
# It was generated by IdlC from LhxConfig.idl.

use strict;

package Raritan::RPC::lhxmodel::Config;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "lhxmodel.Config:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::lhxmodel::Config::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant NO_ERROR => 0;

use constant ERR_INVALID_PARAMS => 1;

use Raritan::RPC::lhxmodel::Config::ComSettings;

sub getComSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getComSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::lhxmodel::Config::ComSettings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::lhxmodel::Config::ComSettings;

sub setComSettings($$) {
    my ($self, $settings) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'settings'} = Raritan::RPC::lhxmodel::Config::ComSettings::encode($settings);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setComSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub getName($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getName', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub setName($$) {
    my ($self, $name) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setName', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('lhxmodel.Config', 1, 0, 0, 'Raritan::RPC::lhxmodel::Config');
1;
