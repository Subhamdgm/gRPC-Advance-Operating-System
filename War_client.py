import grpc
import war_pb2
import war_pb2_grpc

def run_simulation():
    # Create a gRPC channel to the server
    ip = input("Enter Server's Ip Address ")
    port=int(input("Enter Port "))
    channel = grpc.insecure_channel(f"{ip}:{port}")
    stub = war_pb2_grpc.WarzoneSimulatorStub(channel)

    # Get simulation parameters from the user (N, M, time, soldier speeds)
    N = int(input("Enter the size of the battlefield (N): "))
    M = int(input("Enter the number of soldiers (M): "))
    time = int(input("Enter the number of time steps: "))
    soldier_speeds = []
    for i in range(M):
        s = int(input(f"Enter speed for soldier {i + 1}: "))
        soldier_speeds.append(s)

    # Create a gRPC request with the parameters
    request = war_pb2.SimulationRequest(N=N, M=M, time=time, soldier_speeds=soldier_speeds)

    # Call the remote procedure and get the response
    response = stub.SimulateWar(request)

    # Process and print the simulation output
    for result in response.simulation_output:
        print(result)

if __name__ == "__main__":
    run_simulation()
