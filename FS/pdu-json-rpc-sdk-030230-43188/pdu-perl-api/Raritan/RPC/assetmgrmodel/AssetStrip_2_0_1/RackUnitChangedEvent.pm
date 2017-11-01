# Do NOT edit this file!
# It was generated by IdlC from AssetStrip.idl.

use strict;

package Raritan::RPC::assetmgrmodel::AssetStrip_2_0_1::RackUnitChangedEvent;

use constant typeId => "assetmgrmodel.AssetStrip_2_0_1.RackUnitChangedEvent:1.0.0";
use Raritan::RPC::assetmgrmodel::AssetStrip_2_0_1::RackUnitInfo;
use Raritan::RPC::event::UserEvent;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::event::UserEvent::encode($in);
    $encoded->{'rackUnitNumber'} = 1 * $in->{'rackUnitNumber'};
    $encoded->{'rackUnit'} = Raritan::RPC::assetmgrmodel::AssetStrip_2_0_1::RackUnitInfo::encode($in->{'rackUnit'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::event::UserEvent::decode($agent, $in);
    $decoded->{'rackUnitNumber'} = $in->{'rackUnitNumber'};
    $decoded->{'rackUnit'} = Raritan::RPC::assetmgrmodel::AssetStrip_2_0_1::RackUnitInfo::decode($agent, $in->{'rackUnit'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('assetmgrmodel.AssetStrip_2_0_1.RackUnitChangedEvent', 1, 0, 0, 'Raritan::RPC::assetmgrmodel::AssetStrip_2_0_1::RackUnitChangedEvent');
1;
