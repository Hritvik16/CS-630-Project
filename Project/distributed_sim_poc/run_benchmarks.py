import subprocess
import time

def run_suite(mode, sim_type, width=100, height=100):
    print(f"\n{'='*60}")
    print(f"🚀 STARTING: {sim_type.upper()} | {mode.upper()} MODE | {width}x{height} Grid")
    print(f"{'='*60}")

    worker_a = subprocess.Popen(
        ["python3", "worker.py", "--id", "A", "--port", "50051", "--peer_port", "50052", 
         "--mode", mode, "--sim_type", sim_type, "--width", str(width), "--height", str(height)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    worker_b = subprocess.Popen(
        ["python3", "worker.py", "--id", "B", "--port", "50052", "--peer_port", "50051", 
         "--mode", mode, "--sim_type", sim_type, "--width", str(width), "--height", str(height)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    time.sleep(2) # Give gRPC time to bind

    try:
        master = subprocess.run(["python3", "master.py"], capture_output=True, text=True)
        
        output = master.stdout
        if "FINAL BENCHMARK RESULTS" in output:
            table = output[output.find("FINAL BENCHMARK RESULTS"):]
            print(table)
        else:
            print("Error: Could not find benchmark table.")
            
    finally:
        worker_a.terminate()
        worker_b.terminate()
        worker_a.wait()
        worker_b.wait()

if __name__ == "__main__":
    print("Starting automated dual-benchmark suite...\n")
    
    for sim in ['warehouse', 'forest_fire']:
        run_suite("optimistic", sim)
        run_suite("conservative", sim)
    
    print("\n🎉 ALL BENCHMARKS COMPLETED SUCCESSFULLY! 🎉")