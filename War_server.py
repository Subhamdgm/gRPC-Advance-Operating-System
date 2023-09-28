import grpc
from concurrent import futures
import war_pb2
import war_pb2_grpc
import random
import time
import datetime
import logging

current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Configure logging to write to a file named output.log
logging.basicConfig(filename='output1.log', level=logging.INFO)
logging.info(f"Created on {current_datetime}")


class Soldier:
    def __init__(self, soldier_id, x, y, N, speed):
        self.soldier_id = soldier_id
        self.x = x
        self.y = y
        self.N = N
        self.speed = speed
        self.is_alive = True
        self.is_commander = False
        self.commander = None  # Stores the commander reference

    # Change soldiers position
    def move(self, new_x, new_y):
        self.x = int(round(new_x))
        self.y = int(round(new_y))
        logging.info(f"Soldier {self.soldier_id} moved to ({self.x},{self.y})")

    # Called when a soldier is within impact radius
    def take_shelter(self, missile_x, missile_y, impact_radius):
        if self.commander and self.is_alive:
            distance = ((self.x - missile_x) ** 2 + (self.y - missile_y) ** 2) ** 0.5
            distance = int(distance)
            if distance <= impact_radius-1 and self.speed > 0:
                # Calculate a direction away from the missile
                dx = missile_x - self.x
                dy = missile_y - self.y
                direction_x = 1 if dx >= 0 else -1
                direction_y = 1 if dy >= 0 else -1

                
                max_move = self.speed

                # Move multiple steps while considering the speed
                
                new_x = self.x + direction_x * max_move
                new_y = self.y + direction_y * max_move

                # Ensure the new coordinates are within bounds
                new_x = max(0, min(new_x, self.N - 1))
                new_y = max(0, min(new_y, self.N - 1))

                # Check if the soldier is still within impact radius after moving
                new_distance = ((self.x - missile_x) ** 2 + (self.y - missile_y) ** 2) ** 0.5
                new_distance = int(new_distance)
                if new_distance <= impact_radius-1:
                    self.is_alive = False
                
                # Update the soldier's position
                self.move(new_x, new_y)

class Warzone:
    def __init__(self, N, M):
        self.N = N
        self.M = M
        self.casualties = []
        # Initialize soldiers
        self.soldiers = []
        self.initialize_soldiers()
                           
    #Initialize soldiers
    def initialize_soldiers(self):
            # print("(speed should be between 0-4)")
            for i in range(1, self.M + 1):
                s = 0  # Initialize with speed 0, which will be updated by the client
                self.soldiers.append(Soldier(i, random.randint(0, self.N - 1), random.randint(0, self.N - 1), self.N, s))
            print("")

    # Function for simulating an approaching missile
    def missile_approaching(self, missile_x, missile_y, impact_radius):
        for soldier in self.soldiers:
            if soldier.is_alive:
                distance = ((soldier.x - missile_x) ** 2 + (soldier.y - missile_y) ** 2) ** 0.5
                distance = int(distance)
                if distance <= impact_radius-1:
                    soldier.take_shelter(missile_x, missile_y, impact_radius)
                    #If a soldier is still within the impact_radius it should be dead
                    if not soldier.is_alive:
                        self.casualties.append(soldier.soldier_id)
                    

    # Function for election of a commander
    def commander_election(self):
        alive_soldiers = [soldier for soldier in self.soldiers if soldier.is_alive and not soldier.is_commander]
        if not alive_soldiers:
            return None  # No new commander elected

        new_commander = random.choice(alive_soldiers)
        new_commander.is_commander = True
        for soldier in alive_soldiers:
            soldier.commander = new_commander
        print(f"Soldier {new_commander.soldier_id} elected as the new commander.")
        return new_commander.soldier_id

    # Check if the battle was won/lost
    def check_battle_result(self):
        alive_count = sum(1 for soldier in self.soldiers if soldier.is_alive)
        casualties_count = len(self.casualties)

        if casualties_count <= alive_count:
            return True
        else:
            return False

    # Print a grid for visualization

    def print_layout(self, missile_x, missile_y, impact_radius):
        layout = []
        for i in range(self.N):
            row = []
            for j in range(self.N):
                if (i, j) == (missile_x, missile_y):
                    row.append("X")
                else:
                    soldier_id = next((soldier.soldier_id for soldier in self.soldiers if (i, j) == (soldier.x, soldier.y) and soldier.is_alive), None)
                    if soldier_id is not None:
                        row.append(str(soldier_id))
                    else:
                        row.append(".")
            layout.append(" ".join(row))
        return layout


#Server implementation
class WarzoneSimulatorServicer(war_pb2_grpc.WarzoneSimulatorServicer):
    def SimulateWar(self, request, context):
        # Extract parameters from the gRPC request
        N = request.N
        M = request.M
        time = request.time
        soldier_speeds = request.soldier_speeds

        # Initialize the Warzone with the provided parameters
        warzone = Warzone(N=N, M=M)
        
        # Set soldier speeds
        for i, soldier_speed in enumerate(soldier_speeds):
            if 0 <= soldier_speed < 5:
                warzone.soldiers[i].speed = soldier_speed
            else:
                # Handle invalid speed values
                return war_pb2.SimulationResponse(
                    simulation_output=["Invalid speed value for soldier {}".format(i + 1)]
                )

        simulation_output = []

         # Randomly elect a commander
        commander = random.choice(warzone.soldiers)
        commander.is_commander = True
        simulation_output.append("\nCommander is soldier {}\n".format(commander.soldier_id))
        logging.info(f"Commander is Soldier {commander.soldier_id}")
        for soldier in warzone.soldiers:
            soldier.commander = commander
        
        for soldier in warzone.soldiers:
                simulation_output.append("Soldier {} is at ({},{})".format(soldier.soldier_id, soldier.x, soldier.y))
                logging.info(f"Soldier {soldier.soldier_id} is at ({soldier.x},{soldier.y})")
        

        for t in range(1, time+1):
            missile_x = random.randint(0, N-1)
            missile_y = random.randint(0, N-1)
            impact_radius = random.randint(1, 4)

            simulation_output.append("\nTime {}: Missile approaching ({}, {}) with radius {}".format(t, missile_x, missile_y, impact_radius))
            logging.info(f"\nTime {t}: Missile approaching ({missile_x}, {missile_y}) with radius {impact_radius}")

            warzone.missile_approaching(missile_x, missile_y, impact_radius)

            for soldier in warzone.soldiers:
                if soldier.is_alive:
                    distance = ((soldier.x - missile_x) ** 2 + (soldier.y - missile_y) ** 2) ** 0.5
                    distance = int(distance)
                    if distance <= impact_radius-1:
                        soldier.is_alive = False
                        warzone.casualties.append(soldier.soldier_id)
                        if soldier.is_commander:
                            new_commander = warzone.commander_election()
                            simulation_output.append("New commander is: {}".format(new_commander))
                            logging.info(f"New commander is: {new_commander}")

            # Visualize the battlefield layout at each time step
            layout_output = warzone.print_layout(missile_x,missile_y, impact_radius)
            simulation_output.append("\n".join(layout_output))
            logging.info("\n".join(layout_output))
            simulation_output.append("Casualties: {}".format(warzone.casualties))
            logging.info(f"Casualties: {warzone.casualties}")
            simulation_output.append("------------------------------------------------------------------")
            logging.info("------------------------------------------------------------------")

        # Check the battle result
        if warzone.check_battle_result():
            simulation_output.append("The battle was won!")
            logging.info("The battle was won!\n")
        else:
            simulation_output.append("The battle was lost!")
            logging.info("The battle was lost!\n")

        # Create a response with the simulation output
        response = war_pb2.SimulationResponse(simulation_output=simulation_output)

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    war_pb2_grpc.add_WarzoneSimulatorServicer_to_server(WarzoneSimulatorServicer(), server)
    server.add_insecure_port("[::]:50051")  # Listen on port 50051
    server.start()
    print("Server Started.......")
    
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
