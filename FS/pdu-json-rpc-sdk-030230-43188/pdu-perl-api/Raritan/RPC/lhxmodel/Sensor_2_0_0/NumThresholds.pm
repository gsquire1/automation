# Do NOT edit this file!
# It was generated by IdlC from LhxSensor.idl.

use strict;

package Raritan::RPC::lhxmodel::Sensor_2_0_0::NumThresholds;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'lowerCriticalIsEnabled'} = ($in->{'lowerCriticalIsEnabled'}) ? JSON::true : JSON::false;
    $encoded->{'lowerCritical'} = 1 * $in->{'lowerCritical'};
    $encoded->{'lowerWarningIsEnabled'} = ($in->{'lowerWarningIsEnabled'}) ? JSON::true : JSON::false;
    $encoded->{'lowerWarning'} = 1 * $in->{'lowerWarning'};
    $encoded->{'upperWarningIsEnabled'} = ($in->{'upperWarningIsEnabled'}) ? JSON::true : JSON::false;
    $encoded->{'upperWarning'} = 1 * $in->{'upperWarning'};
    $encoded->{'upperCriticalIsEnabled'} = ($in->{'upperCriticalIsEnabled'}) ? JSON::true : JSON::false;
    $encoded->{'upperCritical'} = 1 * $in->{'upperCritical'};
    $encoded->{'hysteresis'} = 1 * $in->{'hysteresis'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'lowerCriticalIsEnabled'} = ($in->{'lowerCriticalIsEnabled'}) ? 1 : 0;
    $decoded->{'lowerCritical'} = $in->{'lowerCritical'};
    $decoded->{'lowerWarningIsEnabled'} = ($in->{'lowerWarningIsEnabled'}) ? 1 : 0;
    $decoded->{'lowerWarning'} = $in->{'lowerWarning'};
    $decoded->{'upperWarningIsEnabled'} = ($in->{'upperWarningIsEnabled'}) ? 1 : 0;
    $decoded->{'upperWarning'} = $in->{'upperWarning'};
    $decoded->{'upperCriticalIsEnabled'} = ($in->{'upperCriticalIsEnabled'}) ? 1 : 0;
    $decoded->{'upperCritical'} = $in->{'upperCritical'};
    $decoded->{'hysteresis'} = $in->{'hysteresis'};
    return $decoded;
}

1;
