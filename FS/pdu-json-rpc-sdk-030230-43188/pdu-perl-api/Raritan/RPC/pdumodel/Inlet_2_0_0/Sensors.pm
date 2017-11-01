# Do NOT edit this file!
# It was generated by IdlC from Inlet.idl.

use strict;

package Raritan::RPC::pdumodel::Inlet_2_0_0::Sensors;


sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'voltage'} = Raritan::RPC::ObjectCodec::encode($in->{'voltage'});
    $encoded->{'current'} = Raritan::RPC::ObjectCodec::encode($in->{'current'});
    $encoded->{'peakCurrent'} = Raritan::RPC::ObjectCodec::encode($in->{'peakCurrent'});
    $encoded->{'residualCurrent'} = Raritan::RPC::ObjectCodec::encode($in->{'residualCurrent'});
    $encoded->{'activePower'} = Raritan::RPC::ObjectCodec::encode($in->{'activePower'});
    $encoded->{'reactivePower'} = Raritan::RPC::ObjectCodec::encode($in->{'reactivePower'});
    $encoded->{'apparentPower'} = Raritan::RPC::ObjectCodec::encode($in->{'apparentPower'});
    $encoded->{'powerFactor'} = Raritan::RPC::ObjectCodec::encode($in->{'powerFactor'});
    $encoded->{'displacementPowerFactor'} = Raritan::RPC::ObjectCodec::encode($in->{'displacementPowerFactor'});
    $encoded->{'activeEnergy'} = Raritan::RPC::ObjectCodec::encode($in->{'activeEnergy'});
    $encoded->{'apparentEnergy'} = Raritan::RPC::ObjectCodec::encode($in->{'apparentEnergy'});
    $encoded->{'unbalancedCurrent'} = Raritan::RPC::ObjectCodec::encode($in->{'unbalancedCurrent'});
    $encoded->{'lineFrequency'} = Raritan::RPC::ObjectCodec::encode($in->{'lineFrequency'});
    $encoded->{'phaseAngle'} = Raritan::RPC::ObjectCodec::encode($in->{'phaseAngle'});
    $encoded->{'powerQuality'} = Raritan::RPC::ObjectCodec::encode($in->{'powerQuality'});
    $encoded->{'surgeProtectorStatus'} = Raritan::RPC::ObjectCodec::encode($in->{'surgeProtectorStatus'});
    $encoded->{'residualCurrentStatus'} = Raritan::RPC::ObjectCodec::encode($in->{'residualCurrentStatus'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'voltage'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'voltage'}, 'sensors.NumericSensor');
    $decoded->{'current'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'current'}, 'sensors.NumericSensor');
    $decoded->{'peakCurrent'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'peakCurrent'}, 'sensors.NumericSensor');
    $decoded->{'residualCurrent'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'residualCurrent'}, 'sensors.NumericSensor');
    $decoded->{'activePower'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'activePower'}, 'sensors.NumericSensor');
    $decoded->{'reactivePower'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'reactivePower'}, 'sensors.NumericSensor');
    $decoded->{'apparentPower'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'apparentPower'}, 'sensors.NumericSensor');
    $decoded->{'powerFactor'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'powerFactor'}, 'sensors.NumericSensor');
    $decoded->{'displacementPowerFactor'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'displacementPowerFactor'}, 'sensors.NumericSensor');
    $decoded->{'activeEnergy'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'activeEnergy'}, 'sensors.NumericSensor');
    $decoded->{'apparentEnergy'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'apparentEnergy'}, 'sensors.NumericSensor');
    $decoded->{'unbalancedCurrent'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'unbalancedCurrent'}, 'sensors.NumericSensor');
    $decoded->{'lineFrequency'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'lineFrequency'}, 'sensors.NumericSensor');
    $decoded->{'phaseAngle'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'phaseAngle'}, 'sensors.NumericSensor');
    $decoded->{'powerQuality'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'powerQuality'}, 'sensors.StateSensor');
    $decoded->{'surgeProtectorStatus'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'surgeProtectorStatus'}, 'sensors.StateSensor');
    $decoded->{'residualCurrentStatus'} = Raritan::RPC::ObjectCodec::decode($agent, $in->{'residualCurrentStatus'}, 'pdumodel.ResidualCurrentStateSensor');
    return $decoded;
}

1;
