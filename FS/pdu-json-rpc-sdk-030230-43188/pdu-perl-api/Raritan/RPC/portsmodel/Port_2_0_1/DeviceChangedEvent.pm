# Do NOT edit this file!
# It was generated by IdlC from Port.idl.

use strict;

package Raritan::RPC::portsmodel::Port_2_0_1::DeviceChangedEvent;

use constant typeId => "portsmodel.Port_2_0_1.DeviceChangedEvent:1.0.0";
use Raritan::RPC::idl::Event;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::idl::Event::encode($in);
    $encoded->{'oldDevice'} = Raritan::RPC::ObjectCodec::encode($in->{'oldDevice'});
    $encoded->{'newDevice'} = Raritan::RPC::ObjectCodec::encode($in->{'newDevice'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::idl::Event::decode($agent, $in);
    $decoded->{'oldDevice'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'oldDevice'}, 'idl.Object');
    $decoded->{'newDevice'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'newDevice'}, 'idl.Object');
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('portsmodel.Port_2_0_1.DeviceChangedEvent', 1, 0, 0, 'Raritan::RPC::portsmodel::Port_2_0_1::DeviceChangedEvent');
1;
