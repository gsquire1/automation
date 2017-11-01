# Do NOT edit this file!
# It was generated by IdlC from SensorLogger.idl.

use strict;

package Raritan::RPC::pdumodel::SensorLogger;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "pdumodel.SensorLogger:1.0.0";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::pdumodel::SensorLogger::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::pdumodel::SensorLogger::Settings;

sub getSettings($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSettings', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::SensorLogger::Settings::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

sub setSettings($$$) {
    my ($self, $isEnabled, $samplesPerRecord) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'isEnabled'} = ($isEnabled) ? JSON::true : JSON::false;
    $args->{'samplesPerRecord'} = 1 * $samplesPerRecord;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setSettings', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub getTimeStamps($$$$) {
    my ($self, $timestamps, $recid, $count) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'recid'} = 1 * $recid;
    $args->{'count'} = 1 * $count;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getTimeStamps', $args);
    $$timestamps = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'timestamps'}}; $i0++) {
        $$timestamps->[$i0] = $rsp->{'timestamps'}->[$i0];
    }
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::pdumodel::SensorLogger::Record;

sub getSensorRecords($$$$$) {
    my ($self, $recs, $sensor, $recid, $count) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'sensor'} = Raritan::RPC::ObjectCodec::encode($sensor);
    $args->{'recid'} = 1 * $recid;
    $args->{'count'} = 1 * $count;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSensorRecords', $args);
    $$recs = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'recs'}}; $i0++) {
        $$recs->[$i0] = Raritan::RPC::pdumodel::SensorLogger::Record::decode($agent, $rsp->{'recs'}->[$i0]);
    }
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::pdumodel::SensorLogger::Record;

sub getExternalSensorRecords($$$$$) {
    my ($self, $recs, $extsensor, $recid, $count) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'extsensor'} = Raritan::RPC::ObjectCodec::encode($extsensor);
    $args->{'recid'} = 1 * $recid;
    $args->{'count'} = 1 * $count;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getExternalSensorRecords', $args);
    $$recs = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'recs'}}; $i0++) {
        $$recs->[$i0] = Raritan::RPC::pdumodel::SensorLogger::Record::decode($agent, $rsp->{'recs'}->[$i0]);
    }
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::pdumodel::SensorLogger::TimedRecord;

sub getSensorTimedRecords($$$$$) {
    my ($self, $recs, $sensor, $recid, $count) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'sensor'} = Raritan::RPC::ObjectCodec::encode($sensor);
    $args->{'recid'} = 1 * $recid;
    $args->{'count'} = 1 * $count;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getSensorTimedRecords', $args);
    $$recs = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'recs'}}; $i0++) {
        $$recs->[$i0] = Raritan::RPC::pdumodel::SensorLogger::TimedRecord::decode($agent, $rsp->{'recs'}->[$i0]);
    }
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::pdumodel::SensorLogger::TimedRecord;

sub getExtSensorTimedRecords($$$$$) {
    my ($self, $recs, $extsensor, $recid, $count) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'extsensor'} = Raritan::RPC::ObjectCodec::encode($extsensor);
    $args->{'recid'} = 1 * $recid;
    $args->{'count'} = 1 * $count;
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getExtSensorTimedRecords', $args);
    $$recs = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'recs'}}; $i0++) {
        $$recs->[$i0] = Raritan::RPC::pdumodel::SensorLogger::TimedRecord::decode($agent, $rsp->{'recs'}->[$i0]);
    }
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

use Raritan::RPC::pdumodel::SensorLogger::SensorSet;

sub getLoggedSensors($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'getLoggedSensors', $args);
    my $_ret_;
    $_ret_ = Raritan::RPC::pdumodel::SensorLogger::SensorSet::decode($agent, $rsp->{'_ret_'});
    return $_ret_;
}

use Raritan::RPC::pdumodel::SensorLogger::SensorSet;

sub setLoggedSensors($$) {
    my ($self, $sensors) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'sensors'} = Raritan::RPC::pdumodel::SensorLogger::SensorSet::encode($sensors);
    my $rsp = $agent->json_rpc($self->{'rid'}, 'setLoggedSensors', $args);
    my $_ret_;
    $_ret_ = $rsp->{'_ret_'};
    return $_ret_;
}

sub enableAllSensors($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'enableAllSensors', $args);
}

sub disableAllSensors($) {
    my ($self) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    my $rsp = $agent->json_rpc($self->{'rid'}, 'disableAllSensors', $args);
}

Raritan::RPC::Registry::registerProxyClass('pdumodel.SensorLogger', 1, 0, 0, 'Raritan::RPC::pdumodel::SensorLogger');
1;
