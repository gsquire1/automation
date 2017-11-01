# Do NOT edit this file!
# It was generated by IdlC from ServerMonitor.idl.

use strict;

package Raritan::RPC::servermon::ServerMonitor::Server;

use Raritan::RPC::servermon::ServerMonitor::ServerSettings;
use Raritan::RPC::servermon::ServerMonitor::ServerStatus;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'settings'} = Raritan::RPC::servermon::ServerMonitor::ServerSettings::encode($in->{'settings'});
    $encoded->{'status'} = Raritan::RPC::servermon::ServerMonitor::ServerStatus::encode($in->{'status'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'settings'} = Raritan::RPC::servermon::ServerMonitor::ServerSettings::decode($agent, $in->{'settings'});
    $decoded->{'status'} = Raritan::RPC::servermon::ServerMonitor::ServerStatus::decode($agent, $in->{'status'});
    return $decoded;
}

1;
