# Do NOT edit this file!
# It was generated by IdlC from UserManager.idl.

use strict;

package Raritan::RPC::usermgmt::AccountChanged;

use constant typeId => "usermgmt.AccountChanged:1.0.0";
use Raritan::RPC::usermgmt::AccountEvent;
use Raritan::RPC::usermgmt::UserInfo;
use Raritan::RPC::usermgmt::UserInfo;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::usermgmt::AccountEvent::encode($in);
    $encoded->{'oldSettings'} = Raritan::RPC::usermgmt::UserInfo::encode($in->{'oldSettings'});
    $encoded->{'newSettings'} = Raritan::RPC::usermgmt::UserInfo::encode($in->{'newSettings'});
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::usermgmt::AccountEvent::decode($agent, $in);
    $decoded->{'oldSettings'} = Raritan::RPC::usermgmt::UserInfo::decode($agent, $in->{'oldSettings'});
    $decoded->{'newSettings'} = Raritan::RPC::usermgmt::UserInfo::decode($agent, $in->{'newSettings'});
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('usermgmt.AccountChanged', 1, 0, 0, 'Raritan::RPC::usermgmt::AccountChanged');
1;
