# Do NOT edit this file!
# It was generated by IdlC from Net.idl.

use strict;

package Raritan::RPC::net::Net_2_0_2;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "net.Net:2.0.2";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::net::Net_2_0_2::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use constant ERR_INVALID_PARAMS => 1;

use Raritan::RPC::net::NetworkConfigIP;

sub setNetworkConfigIP($$) {
    my ($self, $cfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'cfg'} = Raritan::RPC::net::NetworkConfigIP::encode($cfg);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigIP', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::net::NetworkConfigIP;

sub getNetworkConfigIP($$) {
    my ($self, $cfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getNetworkConfigIP', $args);
    $$cfg = Raritan::RPC::net::NetworkConfigIP::decode($agent, $rsp->{'cfg'});
}

use Raritan::RPC::net::NetworkConfigIPv4;

sub setNetworkConfigIPv4($$) {
    my ($self, $cfg4) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'cfg4'} = Raritan::RPC::net::NetworkConfigIPv4::encode($cfg4);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigIPv4', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::net::NetworkConfigIPv4;
use Raritan::RPC::net::NetworkConfigIPv4;

sub getNetworkConfigIPv4($$$) {
    my ($self, $cfg4, $cfg4current) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getNetworkConfigIPv4', $args);
    $$cfg4 = Raritan::RPC::net::NetworkConfigIPv4::decode($agent, $rsp->{'cfg4'});
    $$cfg4current = Raritan::RPC::net::NetworkConfigIPv4::decode($agent, $rsp->{'cfg4current'});
}

use Raritan::RPC::net::IPv4RoutingEntry;
use Raritan::RPC::net::IPv4RoutingEntry;

sub getNetworkConfigRoutesIPv4($$$) {
    my ($self, $static_routes, $active_routes) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getNetworkConfigRoutesIPv4', $args);
    $$static_routes = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'static_routes'}}; $i0++) {
        $$static_routes->[$i0] = Raritan::RPC::net::IPv4RoutingEntry::decode($agent, $rsp->{'static_routes'}->[$i0]);
    }
    $$active_routes = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'active_routes'}}; $i0++) {
        $$active_routes->[$i0] = Raritan::RPC::net::IPv4RoutingEntry::decode($agent, $rsp->{'active_routes'}->[$i0]);
    }
}

use Raritan::RPC::net::IPv4RoutingEntry;

sub setNetworkConfigRoutesIPv4($$) {
    my ($self, $static_routes) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'static_routes'} = [];
    for (my $i0 = 0; $i0 <= $#{$static_routes}; $i0++) {
        $args->{'static_routes'}->[$i0] = Raritan::RPC::net::IPv4RoutingEntry::encode($static_routes->[$i0]);
    }
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigRoutesIPv4', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::net::IPv6RoutingEntry;
use Raritan::RPC::net::IPv6RoutingEntry;

sub getNetworkConfigRoutesIPv6($$$) {
    my ($self, $static_routes, $active_routes) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getNetworkConfigRoutesIPv6', $args);
    $$static_routes = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'static_routes'}}; $i0++) {
        $$static_routes->[$i0] = Raritan::RPC::net::IPv6RoutingEntry::decode($agent, $rsp->{'static_routes'}->[$i0]);
    }
    $$active_routes = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'active_routes'}}; $i0++) {
        $$active_routes->[$i0] = Raritan::RPC::net::IPv6RoutingEntry::decode($agent, $rsp->{'active_routes'}->[$i0]);
    }
}

use Raritan::RPC::net::IPv6RoutingEntry;

sub setNetworkConfigRoutesIPv6($$) {
    my ($self, $static_routes) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'static_routes'} = [];
    for (my $i0 = 0; $i0 <= $#{$static_routes}; $i0++) {
        $args->{'static_routes'}->[$i0] = Raritan::RPC::net::IPv6RoutingEntry::encode($static_routes->[$i0]);
    }
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigRoutesIPv6', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::net::NetworkConfigIPv6;

sub setNetworkConfigIPv6($$) {
    my ($self, $cfg6) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'cfg6'} = Raritan::RPC::net::NetworkConfigIPv6::encode($cfg6);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigIPv6', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::net::NetworkConfigIPv6;
use Raritan::RPC::net::NetworkActiveValuesIPv6;

sub getNetworkConfigIPv6($$$) {
    my ($self, $cfg6, $ipv6current) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getNetworkConfigIPv6', $args);
    $$cfg6 = Raritan::RPC::net::NetworkConfigIPv6::decode($agent, $rsp->{'cfg6'});
    $$ipv6current = Raritan::RPC::net::NetworkActiveValuesIPv6::decode($agent, $rsp->{'ipv6current'});
}

use Raritan::RPC::net::ServiceConfig;

sub setNetworkConfigServices($$) {
    my ($self, $services) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'services'} = [];
    for (my $i0 = 0; $i0 <= $#{$services}; $i0++) {
        $args->{'services'}->[$i0] = Raritan::RPC::net::ServiceConfig::encode($services->[$i0]);
    }
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigServices', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::net::ServiceConfig;

sub getNetworkConfigServices($$) {
    my ($self, $services) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getNetworkConfigServices', $args);
    $$services = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'services'}}; $i0++) {
        $$services->[$i0] = Raritan::RPC::net::ServiceConfig::decode($agent, $rsp->{'services'}->[$i0]);
    }
}

use Raritan::RPC::net::InterfaceState_2_0_0;
use Raritan::RPC::net::LanInterfaceParameters_2_0_0;
use Raritan::RPC::net::WirelessInterfaceSettings;
use Raritan::RPC::net::LanInterfaceSettings;

sub getNetworkConfigInterface($$$$$) {
    my ($self, $state, $lan, $lancurrent, $wlan) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getNetworkConfigInterface', $args);
    $$state = Raritan::RPC::net::InterfaceState_2_0_0::decode($agent, $rsp->{'state'});
    $$lan = Raritan::RPC::net::LanInterfaceSettings::decode($agent, $rsp->{'lan'});
    $$lancurrent = Raritan::RPC::net::LanInterfaceParameters_2_0_0::decode($agent, $rsp->{'lancurrent'});
    $$wlan = Raritan::RPC::net::WirelessInterfaceSettings::decode($agent, $rsp->{'wlan'});
}

use Raritan::RPC::net::InterfaceState_2_0_0;

sub getMACs($$$$) {
    my ($self, $state, $ethmac, $wlanmac) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getMACs', $args);
    $$state = Raritan::RPC::net::InterfaceState_2_0_0::decode($agent, $rsp->{'state'});
    $$ethmac = $rsp->{'ethmac'};
    $$wlanmac = $rsp->{'wlanmac'};
}

use Raritan::RPC::net::LanInterfaceSettings;

sub setNetworkConfigLan($$) {
    my ($self, $lancfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'lancfg'} = Raritan::RPC::net::LanInterfaceSettings::encode($lancfg);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigLan', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::net::WirelessInterfaceSettings;

sub setNetworkConfigWLan($$) {
    my ($self, $wlancfg) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'wlancfg'} = Raritan::RPC::net::WirelessInterfaceSettings::encode($wlancfg);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setNetworkConfigWLan', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub getBridgeSlaveCount($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getBridgeSlaveCount', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

Raritan::RPC::Registry::registerProxyClass('net.Net', 2, 0, 2, 'Raritan::RPC::net::Net_2_0_2');
1;
