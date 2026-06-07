# Asynchronous Deterministic Coupling for Distributed Spatial Simulations
**Author**: Hritvik
**Course**: CS 630 - Distributed Systems

## Overview
This project implements a Memoryless Optimistic Synchronization protocol for distributed spatial environments. It avoids traditional state-saving rollbacks by utilizing a strict deterministic O(1) resolution hierarchy during boundary state conflicts. 

## Requirements
To run the automated benchmarking suite, ensure you have Python 3 installed. You can install all necessary dependencies using the provided requirements file:


pip install -r requirements.txt

## Project Structure
* `simulation.py`: The deterministic O(1) grid matrices for both the Warehouse Robot routing and Forest Fire cellular automata.
* `worker.py`: The gRPC node daemon running the local physics boundaries and resolving conflicts.
* `master.py`: The orchestration script that injects synthetic network latency and aggregates throughput data.
* `protocol.proto`: The auto-compiled schema for distributed network data exchange.
* `run_benchmarks.py`: The automated test harness that executes the latency curve benchmark.
* `run_density.py`: The automated test harness evaluating throughput against varying spatial obstacle densities.
* `core_benchmark.py`: Isolated mathematical benchmark to evaluate the O(1) resolution matrix without network overhead.
* `visual_demo.py`: The visualizer script rendering the live distributed grids.

## How to Run

*(Note: Ensure ports 50051 and 50052 are free before running any of the networked benchmarks below).*

### 1. The Latency vs. Throughput Benchmark
To reproduce the primary throughput data found in the project report, run this suite. It dynamically spins up the worker processes, executes both simulations across a latency spectrum (0ms to 100ms), and prints the final metrics.
`python3 run_benchmarks.py`

### 2. The Entity Density Stress Test
To reproduce the data for Experiment 2, this suite tests the system's immunity to spatial chaos by scaling the warehouse obstacle density from 5% up to 60%.
`python3 run_density.py`

### 3. The Core Algorithm Scalability Benchmark
To isolate the raw mathematical time complexity of the O(1) deterministic matrix (removing all network and physics overhead), run the core benchmark. This tests resolution times for massive boundary sizes up to 1,000,000 cells.
`python3 core_benchmark.py`

### 4. The Visual Demo (For macOS)
To view the real-time boundary conflict resolution and visual logging, a macOS launch script is provided. This uses AppleScript to automatically open multiple terminal windows side-by-side, rendering a live view of the distributed cluster.
`bash mac_demo.sh`
