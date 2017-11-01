# Do NOT edit this file!
# It was generated by IdlC from UserManager.idl.

use strict;

package Raritan::RPC::usermgmt::PasswordChanged;

use constant typeId => "usermgmt.PasswordChanged:1.0.0";
use Raritan::RPC::usermgmt::AccountEvent;

sub encode {
    my ($in) = @_;
    my $encoded = Raritan::RPC::usermgmt::AccountEvent::encode($in);
    return $encoded;
}

sub decode {
    my ($agent, $in) = @_;
    my $decoded = Raritan::RPC::usermgmt::AccountEvent::decode($agent, $in);
    return $decoded;
}

Raritan::RPC::Registry::registerCodecClass('usermgmt.PasswordChanged', 1, 0, 0, 'Raritan::RPC::usermgmt::PasswordChanged');
1;
