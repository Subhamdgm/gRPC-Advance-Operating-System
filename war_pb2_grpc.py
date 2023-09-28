# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import war_pb2 as war__pb2


class WarzoneSimulatorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SimulateWar = channel.unary_unary(
                '/warzone.WarzoneSimulator/SimulateWar',
                request_serializer=war__pb2.SimulationRequest.SerializeToString,
                response_deserializer=war__pb2.SimulationResponse.FromString,
                )


class WarzoneSimulatorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SimulateWar(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WarzoneSimulatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SimulateWar': grpc.unary_unary_rpc_method_handler(
                    servicer.SimulateWar,
                    request_deserializer=war__pb2.SimulationRequest.FromString,
                    response_serializer=war__pb2.SimulationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'warzone.WarzoneSimulator', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WarzoneSimulator(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SimulateWar(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/warzone.WarzoneSimulator/SimulateWar',
            war__pb2.SimulationRequest.SerializeToString,
            war__pb2.SimulationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
