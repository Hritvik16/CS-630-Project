import time
import grpc
import threading
from concurrent import futures
import protocol_pb2
import protocol_pb2_grpc
from simulation import ForestFireSim, WarehouseRobotSim

class WorkerService(protocol_pb2_grpc.WorkerNodeServicer):
    def __init__(self, node_id: str, port: str, peer_port: str, mode: str, sim_type: str, width: int, height: int, density: float):
        self.node_id = node_id
        self.port = port
        self.peer_port = peer_port
        self.mode = mode
        
        self.peer_boundary_received = threading.Event()
        self.is_left_node = (node_id == "A")
        self.icon = "🤖 [NODE A]" if self.is_left_node else "🖥️ [NODE B]"
        
        if sim_type == "warehouse":
            self.sim = WarehouseRobotSim(width, height, density=density)
        else:
            self.sim = ForestFireSim(width, height, density=density)
            
        print(f"{self.icon} Online | Port: {port} | Mode: {mode.upper()} | Sim: {sim_type.upper()} | Density: {density}")
        
    def ComputeTick(self, request, context):
        start_time = time.time()
        
        if self.mode == "conservative":
            self.peer_boundary_received.clear()
        
        self.sim.step()
        edge = self.sim.get_boundary(self.is_left_node)
        
        def background_network_task():
            if hasattr(request, 'latency_ms') and request.latency_ms > 0:
                time.sleep(request.latency_ms / 1000.0) 
            try:
                with grpc.insecure_channel(f'localhost:{self.peer_port}') as channel:
                    stub = protocol_pb2_grpc.WorkerNodeStub(channel)
                    boundary_data = protocol_pb2.BoundaryData(
                        tick_number=request.tick_number,
                        sender_id=self.node_id,
                        edge_cells=edge
                    )
                    stub.ReceiveBoundary(boundary_data)
            except Exception:
                pass 

        threading.Thread(target=background_network_task).start()

        if self.mode == "conservative":
            self.peer_boundary_received.wait() 

        compute_time = (time.time() - start_time) * 1000
        return protocol_pb2.TickResponse(success=True, computation_time_ms=compute_time)

    def ReceiveBoundary(self, request, context):
        conflict = self.sim.resolve_boundary_conflict(request.edge_cells, self.is_left_node)
        
        if conflict:
            print(f"{self.icon} ⚠️ CONFLICT: Peer mismatch at boundary! -> ⚡ Resolved locally in O(1).")
        else:
            print(f"{self.icon} ✅ Boundary Sync: Perfect Match.")
            
        if self.mode == "conservative":
            self.peer_boundary_received.set()
            
        return protocol_pb2.BoundaryAck(conflict_detected=conflict, resolved_locally=True)

def serve(args):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    protocol_pb2_grpc.add_WorkerNodeServicer_to_server(
        WorkerService(args.id, args.port, args.peer_port, args.mode, args.sim_type, args.width, args.height, args.density), server
    )
    server.add_insecure_port(f'[::]:{args.port}')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--peer_port', required=True)
    parser.add_argument('--mode', choices=['optimistic', 'conservative'], default='optimistic')
    parser.add_argument('--sim_type', choices=['forest_fire', 'warehouse'], default='warehouse')
    parser.add_argument('--width', type=int, default=100)
    parser.add_argument('--height', type=int, default=100)
    parser.add_argument('--density', type=float, default=0.05)
    args = parser.parse_args()
    serve(args)