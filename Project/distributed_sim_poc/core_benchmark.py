import time
import random

def benchmark_core_mechanism(boundary_size: int, conflict_rate: float):
    # 1. Setup: Generate the local boundary (e.g., all EMPTY states)
    local_boundary = [0] * boundary_size
    
    # 2. Setup: Generate incoming peer boundary with a precise % of conflicts
    peer_boundary = []
    for _ in range(boundary_size):
        if random.random() < conflict_rate:
            peer_boundary.append(1) # Conflict! (1 > 0)
        else:
            peer_boundary.append(0) # Match!
            
    # --- START ISOLATED BENCHMARK ---
    start_time = time.perf_counter()
    
    conflicts_resolved = 0
    # The exact O(1) algorithm used in your worker nodes
    for i in range(boundary_size):
        if local_boundary[i] != peer_boundary[i]:
            conflicts_resolved += 1
            # The memoryless deterministic tie-breaker
            local_boundary[i] = max(local_boundary[i], peer_boundary[i])
            
    end_time = time.perf_counter()
    # --- END ISOLATED BENCHMARK ---
    
    execution_time_ms = (end_time - start_time) * 1000
    return execution_time_ms, conflicts_resolved

if __name__ == "__main__":
    sizes = [100, 10_000, 100_000, 1_000_000]
    conflict_rates = [0.0, 0.50, 1.0] # 0%, 50%, and 100% conflict density
    
    print(f"\n{'='*70}")
    print(f"⚙️  ISOLATED BENCHMARK: CORE O(1) DETERMINISTIC RESOLUTION")
    print(f"{'='*70}")
    print(f"{'Boundary Size (Cells)':<25} | {'Conflict Rate':<15} | {'Resolution Time (ms)':<20}")
    print("-" * 70)
    
    for size in sizes:
        for rate in conflict_rates:
            exec_time, actual_conflicts = benchmark_core_mechanism(size, rate)
            rate_str = f"{int(rate * 100)}%"
            print(f"{size:<25,} | {rate_str:<15} | {exec_time:.4f} ms")
        print("-" * 70)
        
    print("🎉 CORE ALGORITHM BENCHMARK COMPLETE!\n")