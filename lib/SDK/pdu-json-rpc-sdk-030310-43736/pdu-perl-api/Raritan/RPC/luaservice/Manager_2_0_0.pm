# Do NOT edit this file!
# It was generated by IdlC from LuaService.idl.

use strict;

package Raritan::RPC::luaservice::Manager_2_0_0;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "luaservice.Manager:2.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::luaservice::Manager_2_0_0::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant NO_ERROR => 0;

use constant ERR_INVALID_NAME => 1;

use constant ERR_NO_SUCH_SCRIPT => 2;

use constant ERR_MAX_SCRIPT_NUMBERS_EXCEEDED => 3;

use constant ERR_MAX_SCRIPT_SIZE_EXCEEDED => 4;

use constant ERR_MAX_ALL_SCRIPT_SIZE_EXCEEDED => 5;

use constant ERR_NOT_TERMINATED => 6;

use constant ERR_NOT_RUNNING => 7;

use constant ERR_INVALID_ADDR => 8;

use constant ERR_TOO_MANY_ARGUMENTS => 10;

use constant ERR_ARGUMENT_NOT_VALID => 11;

use Raritan::RPC::luaservice::ScriptOptions_2_0_0;

sub setScript($$$$) {
    my ($self, $name, $script, $options) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    $args->{'script'} = "$script";
    $args->{'options'} = Raritan::RPC::luaservice::ScriptOptions_2_0_0::encode($options);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setScript', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub getScript($$$) {
    my ($self, $name, $script) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getScript', $args);
    $$script = $rsp->{'script'};
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub getScriptNames($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getScriptNames', $args);
    my $_ret_;
    $_ret_ = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'_ret_'}}; $i0++) {
        $_ret_->[$i0] = $rsp->{'_ret_'}->[$i0];
    }
    return $_ret_;
}

sub deleteScript($$) {
    my ($self, $name) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'deleteScript', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::luaservice::ScriptOptions_2_0_0;

sub setScriptOptions($$$) {
    my ($self, $name, $options) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    $args->{'options'} = Raritan::RPC::luaservice::ScriptOptions_2_0_0::encode($options);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setScriptOptions', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::luaservice::ScriptOptions_2_0_0;

sub getScriptOptions($$$) {
    my ($self, $name, $options) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getScriptOptions', $args);
    $$options = Raritan::RPC::luaservice::ScriptOptions_2_0_0::decode($agent, $rsp->{'options'});
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::luaservice::Environment_2_0_0;

sub getEnvironment($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getEnvironment', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::luaservice::Environment_2_0_0::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

sub getScriptOutput($$$$$$$) {
    my ($self, $name, $iAddr, $oAddr, $nAddr, $oString, $more) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    $args->{'iAddr'} = 1 * $iAddr;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getScriptOutput', $args);
    $$oAddr = $rsp->{'oAddr'};
    $$nAddr = $rsp->{'nAddr'};
    $$oString = $rsp->{'oString'};
    $$more = ($rsp->{'more'}) ? 1 : 0;
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub startScript($$) {
    my ($self, $name) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'startScript', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub startScriptWithArgs($$$) {
    my ($self, $name, $arguments) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    $args->{'arguments'} = [];
    foreach my $key0 (keys %{$arguments}) {
        my $value0 = $arguments->{$key0};
        my $elem0 = {};
        $elem0->{'key'} = "$key0";
        $elem0->{'value'} = "$value0";
        push(@{$args->{'arguments'}}, $elem0);
    }
    my $rsp = $agent->json_rpc($self->{'rid'}, 'startScriptWithArgs', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub terminateScript($$) {
    my ($self, $name) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'terminateScript', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::luaservice::ScriptState;

sub getScriptState($$$) {
    my ($self, $name, $state) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'name'} = "$name";
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getScriptState', $args);
    $$state = Raritan::RPC::luaservice::ScriptState::decode($agent, $rsp->{'state'});
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::luaservice::ScriptState;

sub getScriptStates($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getScriptStates', $args);
    my $_ret_;
    $_ret_ = {};
    for (my $i0 = 0; $i0 <= $#{$rsp->{'_ret_'}}; $i0++) {
        my $key0 = $rsp->{'_ret_'}->[$i0]->{'key'};
        my $value0 = Raritan::RPC::luaservice::ScriptState::decode($agent, $rsp->{'_ret_'}->[$i0]->{'value'});
        $_ret_->{$key0} = $value0;
    }
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('luaservice.Manager', 2, 0, 0, 'Raritan::RPC::luaservice::Manager_2_0_0');
1;
