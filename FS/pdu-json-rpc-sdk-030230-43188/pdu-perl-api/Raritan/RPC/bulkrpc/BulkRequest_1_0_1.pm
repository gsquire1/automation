# Do NOT edit this file!
# It was generated by IdlC from BulkRequest.idl.

use strict;

package Raritan::RPC::bulkrpc::BulkRequest_1_0_1;

use parent qw(Raritan::RPC::RemoteObject);

use constant typeId => "bulkrpc.BulkRequest:1.0.1";

sub new {
    my ($class, $agent, $rid, $typeId) = @_;
    $typeId = $typeId || Raritan::RPC::bulkrpc::BulkRequest_1_0_1::typeId;
    return $class->SUPER::new($agent, $rid, $typeId);
}

use Raritan::RPC::bulkrpc::Request;
use Raritan::RPC::bulkrpc::Response;

sub performRequest($$$) {
    my ($self, $requests, $responses) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'requests'} = [];
    for (my $i0 = 0; $i0 <= $#{$requests}; $i0++) {
        $args->{'requests'}->[$i0] = Raritan::RPC::bulkrpc::Request::encode($requests->[$i0]);
    }
    my $rsp = $agent->json_rpc($self->{'rid'}, 'performRequest', $args);
    $$responses = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'responses'}}; $i0++) {
        $$responses->[$i0] = Raritan::RPC::bulkrpc::Response::decode($agent, $rsp->{'responses'}->[$i0]);
    }
}

use Raritan::RPC::bulkrpc::BulkRequest_1_0_1::Response;
use Raritan::RPC::bulkrpc::BulkRequest_1_0_1::Request;

sub performBulk($$$) {
    my ($self, $requests, $responses) = @_;
    my $agent = $self->{'agent'};
    my $args = {};
    $args->{'requests'} = [];
    for (my $i0 = 0; $i0 <= $#{$requests}; $i0++) {
        $args->{'requests'}->[$i0] = Raritan::RPC::bulkrpc::BulkRequest_1_0_1::Request::encode($requests->[$i0]);
    }
    my $rsp = $agent->json_rpc($self->{'rid'}, 'performBulk', $args);
    $$responses = [];
    for (my $i0 = 0; $i0 <= $#{$rsp->{'responses'}}; $i0++) {
        $$responses->[$i0] = Raritan::RPC::bulkrpc::BulkRequest_1_0_1::Response::decode($agent, $rsp->{'responses'}->[$i0]);
    }
}

Raritan::RPC::Registry::registerProxyClass('bulkrpc.BulkRequest', 1, 0, 1, 'Raritan::RPC::bulkrpc::BulkRequest_1_0_1');
1;
