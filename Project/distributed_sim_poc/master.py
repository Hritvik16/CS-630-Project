import grpc
import protocol_pb2
import protocol_pb2_grpc
import time
from concurrent import futures

def trigger_worker(stub, tick_number, latency_ms):
    request = protocol_pb2.TickRequest(tick_number=tick_number, latency_ms=latency_ms)
    return stub.ComputeTick(request)

def run_worker_loop(stub, num_ticks, latency_ms):
    for tick in range(1, num_ticks + 1):
        trigger_worker(stub, tick, latency_ms)

def run_benchmark(stub_a, stub_b, latency_ms, num_ticks=200):
    start_wall_time = time.time()
    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_a = executor.submit(run_worker_loop, stub_a, num_ticks, latency_ms)
        future_b = executor.submit(run_worker_loop, stub_b, num_ticks, latency_ms)
        future_a.result()
        future_b.result()
            
    total_wall_time = time.time() - start_wall_time
    throughput = num_ticks / total_wall_time
    return throughput

def run_simulation():
    with grpc.insecure_channel('localhost:50051') as channel_a, \
         grpc.insecure_channel('localhost:50052') as channel_b:
         
        stub_a = protocol_pb2_grpc.WorkerNodeStub(channel_a)
        stub_b = protocol_pb2_grpc.WorkerNodeStub(channel_b)
        
        
        latencies = [0, 5, 10, 25, 50, 75, 100]
        results = {}
        
        for lat in latencies:
            fps = run_benchmark(stub_a, stub_b, lat, num_ticks=50) 
            results[lat] = fps
            
        print("\nFINAL BENCHMARK RESULTS")
        print("Latency (ms) | Throughput (Ticks/sec)")
        print("-----------------------------------")
        for lat, fps in results.items():
            print(f"{lat:<12} | {fps:.2f}")

if __name__ == '__main__':
    run_simulation()