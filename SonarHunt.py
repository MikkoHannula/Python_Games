import random
import math

class SonarTreasureHunt:
    def __init__(self, width=60, height=15, num_treasures=3, num_probes=20):
        self.width = width
        self.height = height
        self.num_treasures = num_treasures
        self.num_probes = num_probes
        self.board = self.create_board()
        self.treasures = self.place_treasures()
        self.probes_used = 0
        self.probe_spots = []  # Track exact probe locations
        
    def create_board(self):
        """Create an ASCII sea board with wavy lines and water textures."""
        board = []
        wave_chars = ['~', '≈', '≒', '≓']
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Create a wavy, textured sea background
                wave_type = wave_chars[(x + y) % len(wave_chars)]
                row.append(wave_type)
            board.append(row)
        
        return board
    
    def place_treasures(self):
        """Randomly place treasures on the board."""
        treasures = []
        for _ in range(self.num_treasures):
            while True:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                
                # Ensure treasures are not too close to each other
                if not any(math.dist((x,y), (tx,ty)) < 10 for tx, ty in treasures):
                    treasures.append((x, y))
                    break
        
        return treasures
    
    def calculate_distance(self, probe_x, probe_y, treasure_x, treasure_y):
        """Calculate Euclidean distance between probe and treasure."""
        return math.sqrt((probe_x - treasure_x)**2 + (probe_y - treasure_y)**2)
    
    def launch_probe(self, x, y):
        """Launch a sonar probe and get distance to nearest treasure."""
        if self.probes_used >= self.num_probes:
            return "No more probes available!"
        
        self.probes_used += 1
        
        # Track exact probe location
        self.probe_spots.append((x, y))
        
        # Calculate distances to all treasures
        distances = [
            self.calculate_distance(x, y, tx, ty) 
            for tx, ty in self.treasures
        ]
        
        # Find the closest treasure
        if distances:
            closest_distance = min(distances)
            
            # Mark probe spot on board
            self.mark_probe_spot(x, y)
            
            # Determine distance category
            if closest_distance <= 9:
                if closest_distance <= 3:
                    return f"TREASURE DETECTED! Very close! ({closest_distance:.1f} units)"
                elif closest_distance <= 6:
                    return f"Getting warmer! ({closest_distance:.1f} units)"
                else:
                    return f"Treasure nearby. ({closest_distance:.1f} units)"
            else:
                return f"No treasure in range. ({closest_distance:.1f} units)"
        
        return "No treasures left!"
    
    def mark_probe_spot(self, x, y):
        """Mark the exact probe location on the board."""
        # Stay within board boundaries
        if 0 <= x < self.width and 0 <= y < self.height:
            # Mark with probe symbol (using 'X')
            self.board[y][x] = 'X'
    
    def display_board(self):
        """Display the current state of the game board with coordinate markers."""
        # Top coordinate row
        top_header = " " * 4  # Padding for side Y coordinates
        for x in range(self.width):
            # Use modulo to only show every 5th x-coordinate
            top_header += str(x % 10) if x % 5 == 0 else " "
        print(top_header)
        
        # Print board with Y-coordinates
        for y, row in enumerate(self.board):
            # Format Y-coordinate with right-aligned 3-digit padding
            y_coord = f"{y:3d} "
            print(y_coord + "".join(row))
        
        # Bottom coordinate row (similar to top)
        bottom_header = " " * 4
        for x in range(self.width):
            bottom_header += str(x % 10) if x % 5 == 0 else " "
        print(bottom_header)
        
        print(f"Probes Used: {self.probes_used}/{self.num_probes}")
    
    def play(self):
        """Main game loop."""
        print("🌊 SONAR TREASURE HUNT 🌊")
        print("Find the hidden treasures using your limited probes!")
        print("Tip: 'X' marks your probe spots. Use the coordinates to aim carefully!")
        print("Nearby probes might help you triangulate treasure locations!")
        
        while self.probes_used < self.num_probes:
            self.display_board()
            
            try:
                x = int(input(f"Enter X coordinate (0-{self.width-1}): "))
                y = int(input(f"Enter Y coordinate (0-{self.height-1}): "))
                
                if x < 0 or x >= self.width or y < 0 or y >= self.height:
                    print("Coordinates out of bounds. Try again.")
                    continue
                
                result = self.launch_probe(x, y)
                print(result)
                
                # Check if all treasures are found
                if all(any(self.board[ty][tx] == 'X' for tx, ty in self.probe_spots 
                           if abs(tx - tx2) <= 3 and abs(ty - ty2) <= 3) 
                        for tx2, ty2 in self.treasures):
                    print("🏆 Congratulations! You've found all the treasures! 🏆")
                    break
            
            except ValueError:
                print("Please enter valid numbers!")
        
        print("Game Over!")
        print("Treasure Locations:", self.treasures)
        print("Probe Locations:", self.probe_spots)

# Run the game
if __name__ == "__main__":
    game = SonarTreasureHunt()
    game.play()