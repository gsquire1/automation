# Do NOT edit this file!
# It was generated by IdlC from PowerMeter.idl.

use strict;

package Raritan::RPC::pdumodel::PowerMeter_1_0_1::SettingsChangedEvent;

use constant typeId => "pdumodel.PowerMeter_1_0_1.SettingsChangedEvent:1.0.0";
use Raritan::RPC::pdumodel::PowerMeter_1_0_1::Settings;
use Raritan::RPC::event::UserEvent;
use Raritan::RPC::pdumodel::PowerMeter_1_0_1::Settings;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::event::UserEvent::encode($in);
    $encoded->{'oldSettings'} = Raritan::RPC::pdumodel::PowerMeter_1_0_1::Settings::encode($in->{'oldSettings'});
    $encoded->{'newSettings'} = Raritan::RPC::pdumodel::PowerMeter_1_0_1::Settings::encode($in->{'newSettings'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::event::UserEvent::decode($agent, $in);
    $decoded->{'oldSettings'} = Raritan::RPC::pdumodel::PowerMeter_1_0_1::Settings::decode($agent, $in->{'oldSettings'});
    $decoded->{'newSettings'} = Raritan::RPC::pdumodel::PowerMeter_1_0_1::Settings::decode($agent, $in->{'newSettings'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('pdumodel.PowerMeter_1_0_1.SettingsChangedEvent', 1, 0, 0, 'Raritan::RPC::pdumodel::PowerMeter_1_0_1::SettingsChangedEvent');
1;
