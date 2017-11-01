# Do NOT edit this file!
# It was generated by IdlC from Pdu.idl.

use strict;

package Raritan::RPC::pdumodel::Pdu_4_0_0::SettingsChangedEvent;

use constant typeId => "pdumodel.Pdu_4_0_0.SettingsChangedEvent:1.0.0";
use Raritan::RPC::pdumodel::Pdu_4_0_0::Settings;
use Raritan::RPC::event::UserEvent;
use Raritan::RPC::pdumodel::Pdu_4_0_0::Settings;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::event::UserEvent::encode($in);
    $encoded->{'oldSettings'} = Raritan::RPC::pdumodel::Pdu_4_0_0::Settings::encode($in->{'oldSettings'});
    $encoded->{'newSettings'} = Raritan::RPC::pdumodel::Pdu_4_0_0::Settings::encode($in->{'newSettings'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::event::UserEvent::decode($agent, $in);
    $decoded->{'oldSettings'} = Raritan::RPC::pdumodel::Pdu_4_0_0::Settings::decode($agent, $in->{'oldSettings'});
    $decoded->{'newSettings'} = Raritan::RPC::pdumodel::Pdu_4_0_0::Settings::decode($agent, $in->{'newSettings'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('pdumodel.Pdu_4_0_0.SettingsChangedEvent', 1, 0, 0, 'Raritan::RPC::pdumodel::Pdu_4_0_0::SettingsChangedEvent');
1;
