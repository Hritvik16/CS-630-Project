# import protocol_pb2
# import json
# import random

# # Base mapping
# EMPTY = protocol_pb2.EMPTY
# STATE_1 = protocol_pb2.TREE  # Tree or Robot
# STATE_2 = protocol_pb2.FIRE  # Fire or Package

# class ForestFireSim:
#     def __init__(self, width: int, height: int, density: float = 0.1):
#         self.width = width
#         self.height = height
#         # Fill with trees, but randomly ignite some fires based on density
#         self.grid = [[STATE_1 for _ in range(width)] for _ in range(height)]
        
#         # Spark initial fires based on density parameter
#         for r in range(height):
#             for c in range(width):
#                 if random.random() < density:
#                     self.grid[r][c] = STATE_2
#         # Guarantee center fire
#         self.grid[height // 2][width // 2] = STATE_2

#     def step(self):
#         new_grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
#         for r in range(self.height):
#             for c in range(self.width):
#                 state = self.grid[r][c]
#                 fire_neighbors, tree_neighbors = 0, 0
#                 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                     nr, nc = r + dr, c + dc
#                     if 0 <= nr < self.height and 0 <= nc < self.width:
#                         if self.grid[nr][nc] == STATE_2: fire_neighbors += 1
#                         elif self.grid[nr][nc] == STATE_1: tree_neighbors += 1

#                 if state == STATE_1 and fire_neighbors >= 1: new_grid[r][c] = STATE_2
#                 elif state == STATE_2: new_grid[r][c] = EMPTY
#                 elif state == EMPTY and tree_neighbors == 2: new_grid[r][c] = STATE_1
#                 else: new_grid[r][c] = state
#         self.grid = new_grid

#     def get_boundary(self, is_left_node: bool) -> list:
#         col = self.width - 1 if is_left_node else 0
#         return [self.grid[r][col] for r in range(self.height)]

#     def resolve_boundary_conflict(self, peer_boundary: list, is_left_node: bool) -> bool:
#         col = self.width - 1 if is_left_node else 0
#         conflict = False
#         for r in range(self.height):
#             local_state, peer_state = self.grid[r][col], peer_boundary[r]
#             if local_state != peer_state:
#                 conflict = True
#                 self.grid[r][col] = max(local_state, peer_state)
#         return conflict

# class WarehouseRobotSim:
#     def __init__(self, width: int, height: int, density: float = 0.05):
#         self.width = width
#         self.height = height
#         self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        
#         # Scatter random packages based on density
#         for r in range(height):
#             for c in range(1, width): # Leave column 0 for robots
#                 if random.random() < density:
#                     self.grid[r][c] = STATE_2
        
#         # Fleet of robots on the far left
#         for r in range(height):
#             self.grid[r][0] = STATE_1

#     def step(self):
#         new_grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
#         claimed_cells = set()
        
#         for r in range(self.height):
#             for c in range(self.width):
#                 if self.grid[r][c] == STATE_2:
#                     new_grid[r][c] = STATE_2
#                     claimed_cells.add((r, c))

#         center_row = self.height // 2
#         for r in range(self.height):
#             for c in range(self.width):
#                 if self.grid[r][c] == STATE_1:
#                     target_r = r + 1 if r < center_row else (r - 1 if r > center_row else r)
#                     target_c = c + 1
                    
#                     if target_c >= self.width or target_r < 0 or target_r >= self.height or (target_r, target_c) in claimed_cells:
#                         if target_c < self.width and (r, target_c) not in claimed_cells:
#                             new_grid[r][target_c] = STATE_1
#                             claimed_cells.add((r, target_c))
#                         else:
#                             new_grid[r][c] = STATE_1
#                             claimed_cells.add((r, c))
#                     else:
#                         new_grid[target_r][target_c] = STATE_1
#                         claimed_cells.add((target_r, target_c))
#         self.grid = new_grid

#     def get_boundary(self, is_left_node: bool) -> list:
#         col = self.width - 1 if is_left_node else 0
#         return [self.grid[r][col] for r in range(self.height)]

#     def resolve_boundary_conflict(self, peer_boundary: list, is_left_node: bool) -> bool:
#         col = self.width - 1 if is_left_node else 0
#         conflict = False
#         for r in range(self.height):
#             local_state, peer_state = self.grid[r][col], peer_boundary[r]
#             if local_state != peer_state:
#                 conflict = True
#                 self.grid[r][col] = max(local_state, peer_state)
#         return conflict

import protocol_pb2
import random

STATE_1 = protocol_pb2.TREE  # Tree or Robot
STATE_2 = protocol_pb2.FIRE  # Fire or Package
EMPTY = protocol_pb2.EMPTY

class ForestFireSim:
    def __init__(self, width: int, height: int, density: float = 0.1):
        self.width = width
        self.height = height
        # Start with a lush forest
        self.grid = [[STATE_1 for _ in range(width)] for _ in range(height)]
        
    def step(self):
        new_grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        for r in range(self.height):
            for c in range(self.width):
                state = self.grid[r][c]
                fire_neighbors = 0
                
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.height and 0 <= nc < self.width:
                        if self.grid[nr][nc] == STATE_2: 
                            fire_neighbors += 1

                if state == STATE_1 and fire_neighbors >= 1: 
                    new_grid[r][c] = STATE_2
                elif state == STATE_2: 
                    new_grid[r][c] = EMPTY
                elif state == EMPTY:
                    # THE FIX: 8% chance to regrow a tree, keeping the simulation alive forever
                    if random.random() < 0.08:
                        new_grid[r][c] = STATE_1
                else: 
                    new_grid[r][c] = state
        self.grid = new_grid

    def get_boundary(self, is_left_node: bool) -> list:
        col = self.width - 1 if is_left_node else 0
        return [self.grid[r][col] for r in range(self.height)]

    def resolve_boundary_conflict(self, peer_boundary: list, is_left_node: bool) -> bool:
        col = self.width - 1 if is_left_node else 0
        conflict = False
        for r in range(self.height):
            local_state, peer_state = self.grid[r][col], peer_boundary[r]
            if local_state != peer_state:
                conflict = True
                self.grid[r][col] = max(local_state, peer_state)
        return conflict

class WarehouseRobotSim:
    def __init__(self, width: int, height: int, density: float = 0.05):
        self.width = width
        self.height = height
        self.grid = [[EMPTY for _ in range(width)] for _ in range(height)]
        
        # Scatter random packages based on density
        for r in range(height):
            for c in range(1, width - 1): # Leave edges clear for spawning/exiting
                if random.random() < density:
                    self.grid[r][c] = STATE_2

    def step(self):
        new_grid = [[EMPTY for _ in range(self.width)] for _ in range(self.height)]
        claimed_cells = set()
        
        # Lock in static packages
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] == STATE_2:
                    new_grid[r][c] = STATE_2
                    claimed_cells.add((r, c))

        # Dynamic swarm pathfinding
        for r in range(self.height):
            for c in range(self.width):
                if self.grid[r][c] == STATE_1:
                    
                    # THE FIX: Always push right. If blocked, slide up or down along the package.
                    moves = [(r, c+1), (r-1, c+1), (r+1, c+1), (r-1, c), (r+1, c)]
                    if random.random() < 0.5: # Add chaos so they don't move in perfect sync
                        moves = [(r, c+1), (r+1, c+1), (r-1, c+1), (r+1, c), (r-1, c)]
                        
                    moved = False
                    for nr, nc in moves:
                        if 0 <= nr < self.height and 0 <= nc < self.width:
                            if (nr, nc) not in claimed_cells and self.grid[nr][nc] != STATE_2:
                                new_grid[nr][nc] = STATE_1
                                claimed_cells.add((nr, nc))
                                moved = True
                                break
                    
                    if not moved:
                        new_grid[r][c] = STATE_1
                        claimed_cells.add((r, c))
                        
        self.grid = new_grid

    def get_boundary(self, is_left_node: bool) -> list:
        col = self.width - 1 if is_left_node else 0
        return [self.grid[r][col] for r in range(self.height)]

    def resolve_boundary_conflict(self, peer_boundary: list, is_left_node: bool) -> bool:
        col = self.width - 1 if is_left_node else 0
        conflict = False
        for r in range(self.height):
            local_state, peer_state = self.grid[r][col], peer_boundary[r]
            if local_state != peer_state:
                conflict = True
                self.grid[r][col] = max(local_state, peer_state)
        return conflict