import time
import os
import random
import argparse
from simulation import WarehouseRobotSim, ForestFireSim, EMPTY

STATE_1 = 1 
STATE_2 = 2 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def render_cell(state, sim_type):
    if sim_type == "warehouse":
        if state == STATE_1: return "🤖"
        elif state == STATE_2: return "📦"
    else: # Forest Fire
        if state == STATE_1: return "🌲"
        elif state == STATE_2: return "🔥"
    return "⬛"

def run_visual_demo(sim_type):
    WIDTH, HEIGHT = 15, 10
    
    # Instantiate the selected simulations
    if sim_type == "warehouse":
        random.seed(42)
        node_a = WarehouseRobotSim(WIDTH, HEIGHT, density=0.08)
        random.seed(100) 
        node_b = WarehouseRobotSim(WIDTH, HEIGHT, density=0.08)
    else:
        random.seed(15)
        node_a = ForestFireSim(WIDTH, HEIGHT, density=0.05)
        random.seed(88) 
        node_b = ForestFireSim(WIDTH, HEIGHT, density=0.05)
    
    # Telemetry tracking
    sync_count = 0
    conflict_count = 0

    print(f"🎬 Starting {sim_type.upper()} Visualizer...")
    time.sleep(2)

    for tick in range(1, 200):
        # Spawners to keep traffic moving
        if sim_type == "warehouse" and tick % 2 == 0:
            spawn_r = random.randint(0, HEIGHT - 1)
            if node_a.grid[spawn_r][0] == EMPTY:
                node_a.grid[spawn_r][0] = STATE_1
                # node_a.robot_targets[(spawn_r, 0)] = node_a._get_new_target()
                
        elif sim_type == "forest_fire" and tick % 4 == 0:
            spawn_r = random.randint(0, HEIGHT - 1)
            node_a.grid[spawn_r][0] = STATE_2 # Spark new fires on the left

        node_a.step()
        node_b.step()

        edge_a = node_a.get_boundary(is_left_node=True)
        edge_b = node_b.get_boundary(is_left_node=False)

        conflict_a = node_a.resolve_boundary_conflict(edge_b, is_left_node=True)
        conflict_b = node_b.resolve_boundary_conflict(edge_a, is_left_node=False)

        # Entity Handoff Cleanup (Warehouse only, fire spreads naturally)
        if sim_type == "warehouse":
            for r in range(HEIGHT):
                if node_a.grid[r][WIDTH-1] == STATE_1 and node_b.grid[r][0] == STATE_1:
                    node_a.grid[r][WIDTH-1] = EMPTY 

        # Telemetry updates
        if conflict_a or conflict_b:
            conflict_count += 1
        else:
            sync_count += 1

        tick_a = tick
        tick_b = tick - random.randint(0, 3) # Simulating minor CPU/Network lag on Node B
        if tick_b < 0: tick_b = 0
        
        # Render Loop
        clear_screen()
        print(f"🚀 {sim_type.upper()} SIMULATION | TICK: {tick}")
        print("   [NODE A - LEFT PARTITION]     |     [NODE B - RIGHT PARTITION]")
        print("-" * 65)

        for r in range(HEIGHT):
            row_str = ""
            for c in range(WIDTH):
                row_str += render_cell(node_a.grid[r][c], sim_type)
            row_str += "  ||  " 
            for c in range(WIDTH):
                row_str += render_cell(node_b.grid[r][c], sim_type)
            print(row_str)
            
        print("-" * 65)
        print("📊 DISTRIBUTED SYNCHRONIZATION TELEMETRY:")
        print(f"   ✅ Perfect Boundary Syncs : {sync_count}")
        print(f"   ⚠️ Conflicts Resolved     : {conflict_count} (O(1) tie-breaker applied)")
        print("-" * 65)

        time.sleep(0.15)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sim', choices=['warehouse', 'forest_fire'], default='warehouse')
    args = parser.parse_args()
    run_visual_demo(args.sim)