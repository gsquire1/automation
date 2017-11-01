# Do NOT edit this file!
# It was generated by IdlC from PowerMeterController.idl.

use strict;

package Raritan::RPC::pdumodel::PowerMeterController::PowerMeterDeletedEvent;

use constant typeId => "pdumodel.PowerMeterController.PowerMeterDeletedEvent:1.0.0";
use Raritan::RPC::event::UserEvent;
use Raritan::RPC::pdumodel::PowerMeter::Config;
use Raritan::RPC::pdumodel::PowerMeter::Settings;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::event::UserEvent::encode($in);
    $encoded->{'config'} = Raritan::RPC::pdumodel::PowerMeter::Config::encode($in->{'config'});
    $encoded->{'settings'} = Raritan::RPC::pdumodel::PowerMeter::Settings::encode($in->{'settings'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::event::UserEvent::decode($agent, $in);
    $decoded->{'config'} = Raritan::RPC::pdumodel::PowerMeter::Config::decode($agent, $in->{'config'});
    $decoded->{'settings'} = Raritan::RPC::pdumodel::PowerMeter::Settings::decode($agent, $in->{'settings'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('pdumodel.PowerMeterController.PowerMeterDeletedEvent', 1, 0, 0, 'Raritan::RPC::pdumodel::PowerMeterController::PowerMeterDeletedEvent');
1;
