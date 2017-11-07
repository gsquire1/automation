# Do NOT edit this file!
# It was generated by IdlC from PeripheralDeviceManager.idl.

use strict;

package Raritan::RPC::peripheral::DeviceManager_2_0_2::PackageEvent_2_0_0;

use constant typeId => "peripheral.DeviceManager_2_0_2.PackageEvent:2.0.0";
use Raritan::RPC::peripheral::PackageInfo_2_0_0;
use Raritan::RPC::peripheral::PackageInfo_2_0_0;
use Raritan::RPC::idl::Event;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::idl::Event::encode($in);
    $encoded->{'packageInfos'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'packageInfos'}}; $i0++) {
        $encoded->{'packageInfos'}->[$i0] = Raritan::RPC::peripheral::PackageInfo_2_0_0::encode($in->{'packageInfos'}->[$i0]);
    }
    $encoded->{'allPackages'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'allPackages'}}; $i0++) {
        $encoded->{'allPackages'}->[$i0] = Raritan::RPC::peripheral::PackageInfo_2_0_0::encode($in->{'allPackages'}->[$i0]);
    }
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::idl::Event::decode($agent, $in);
    $decoded->{'packageInfos'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'packageInfos'}}; $i0++) {
        $decoded->{'packageInfos'}->[$i0] = Raritan::RPC::peripheral::PackageInfo_2_0_0::decode($agent, $in->{'packageInfos'}->[$i0]);
    }
    $decoded->{'allPackages'} = [];
    for (my $i0 = 0; $i0 <= $#{$in->{'allPackages'}}; $i0++) {
        $decoded->{'allPackages'}->[$i0] = Raritan::RPC::peripheral::PackageInfo_2_0_0::decode($agent, $in->{'allPackages'}->[$i0]);
    }
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('peripheral.DeviceManager_2_0_2.PackageEvent', 2, 0, 0, 'Raritan::RPC::peripheral::DeviceManager_2_0_2::PackageEvent_2_0_0');
1;