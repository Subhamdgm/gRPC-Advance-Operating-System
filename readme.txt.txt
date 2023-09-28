                                                           Assignment 1 - Remote Procedure Calls
                                                                                  -------------------------------------



Team Details: 1)Priyansh Deshmukh(Bits_Id : 2023H1120193P)
                       2)Subham Anand       (Bits_Id : 2023H1120195P)
Branch: M.E (Software System)

Instructions Needed to Run the Program

a)Install Python with latest version as well as add in system path variable.

b)Install Visual Studio Code 

c)Download the Protocol Buffers Compiler (protoc):

You can download the Protocol Buffers compiler from the official GitHub repository: https://github.com/protocolbuffers/protobuf/releases

d)Windows:
Extract the downloaded .zip file, and then add the directory containing protoc.exe to your system's PATH environment variable.

e)Verify the Installation:    protoc --version

f)Install gRPC tools by running the commands in cmd:   pip install grpcio-tools

g) We have to run Python grpc_tools.protoc creating *pb2.py files from proto files
     ----------------------------------------------------------------------------------------------------------
	python -m grpc_tools.protoc --proto_path=./ --python_out=./ war.proto     #My protofile name is (war.proto)

h)It will create 2 files in the same directory: war_pb2.py and war_pb2_grpc.py

i)Now 3 files are there i).proto ii) war_client.py iii)war_server.py 

                              To Run the Code
------------------------------------------------------------------------------------
Note1 : Before Running just change the IP address : if you want to test in 2 machines : Just include Servers IP Address in server & Client side  For Particular Connection / Else if U want to test in Localhost Just Mention "localhost:8000" in main()
#8000: Port number

1.)Run the war_server.py file .Server will start and wait for listening clients inputs.
2)Run the War_client.py file. Enter the inputs (i.e All the HyperParameters)
3)Connection will be established and server will work according to the user input and send data to client side .








