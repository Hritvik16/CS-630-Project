import subprocess
import time

def run_density_test(density):
    print(f"\n{'='*60}")
    print(f"📦 TESTING OBSTACLE DENSITY: {int(density * 100)}% FULL")
    print(f"{'='*60}")

    worker_a = subprocess.Popen(
        ["python3", "worker.py", "--id", "A", "--port", "50051", "--peer_port", "50052", 
         "--mode", "optimistic", "--sim_type", "warehouse", "--density", str(density)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    worker_b = subprocess.Popen(
        ["python3", "worker.py", "--id", "B", "--port", "50052", "--peer_port", "50051", 
         "--mode", "optimistic", "--sim_type", "warehouse", "--density", str(density)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    time.sleep(2)

    try:
        master = subprocess.run(["python3", "master.py"], capture_output=True, text=True)
        output = master.stdout
        lines = output.split('\n')
        for line in lines:
            if line.startswith("0 "):
                throughput = line.split('|')[1].strip()
                print(f"✅ Throughput at {int(density * 100)}% density: {throughput} Ticks/sec")
                break
    finally:
        worker_a.terminate()
        worker_b.terminate()
        worker_a.wait()
        worker_b.wait()

if __name__ == "__main__":
    print("Starting Automated Density Stress Test...\n")
    densities = [0.05, 0.20, 0.40, 0.60]
    for d in densities:
        run_density_test(d)
    print("\n🎉 DENSITY BENCHMARKS COMPLETED!")