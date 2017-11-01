# Do NOT edit this file!
# It was generated by IdlC from SensorLogger.idl.

use strict;

package Raritan::RPC::sensors::Logger::Settings;

sub encode {
    my ($in) = @_;
    my $encoded = {};
    $encoded->{'isEnabled'} = ($in->{'isEnabled'}) ? JSON::true : JSON::false;
    $encoded->{'samplePeriod'} = 1 * $in->{'samplePeriod'};
    $encoded->{'samplesPerRecord'} = 1 * $in->{'samplesPerRecord'};
    $encoded->{'oldestRecId'} = 1 * $in->{'oldestRecId'};
    $encoded->{'newestRecId'} = 1 * $in->{'newestRecId'};
    $encoded->{'logCapacity'} = 1 * $in->{'logCapacity'};
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = {};
    $decoded->{'isEnabled'} = ($in->{'isEnabled'}) ? 1 : 0;
    $decoded->{'samplePeriod'} = $in->{'samplePeriod'};
    $decoded->{'samplesPerRecord'} = $in->{'samplesPerRecord'};
    $decoded->{'oldestRecId'} = $in->{'oldestRecId'};
    $decoded->{'newestRecId'} = $in->{'newestRecId'};
    $decoded->{'logCapacity'} = $in->{'logCapacity'};
    return $decoded;
}

1;
