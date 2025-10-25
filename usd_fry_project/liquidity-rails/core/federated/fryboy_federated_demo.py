#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent B Federated Learning Demo
================================

Quick demo script to test the federated learning setup with simulated clients.
This runs everything in a single process for easy testing.

Note: "Fryboy" and "Agent B" are the same - the embedded FRY market maker.
"""

import multiprocessing
import time
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_server():
    """Run the Fryboy federated learning server"""
    from fryboy_federated_server import start_fryboy_server
    
    logger.info("Starting Fryboy Server...")
    start_fryboy_server(
        server_address="[::]:8080",
        num_rounds=10,  # Short demo
        min_clients=2,
        fraction_fit=1.0,  # Use all available clients
    )


def run_client(client_id, venue):
    """Run a Fryboy federated learning client"""
    import time
    time.sleep(2)  # Wait for server to start
    
    from fryboy_federated_client import start_fryboy_client
    
    logger.info(f"Starting Client {client_id} on {venue}...")
    try:
        start_fryboy_client(
            server_address="localhost:8080",
            client_id=client_id,
            venue=venue,
            initial_capital=1000000,
        )
    except Exception as e:
        logger.error(f"Client {client_id} error: {e}")


def main():
    """Run federated learning demo with multiple clients"""
    
    print("\n" + "="*70)
    print("FRYBOY FEDERATED LEARNING DEMO")
    print("="*70)
    print("\nThis demo will:")
    print("1. Start a Fryboy federated learning server")
    print("2. Launch 3 Agent B clients (Binance, OKX, Bybit)")
    print("3. Train for 10 rounds with FRY-specific metrics")
    print("4. Display performance report")
    print("\nPress Ctrl+C to stop at any time")
    print("="*70 + "\n")
    
    time.sleep(2)
    
    # Create processes
    server_process = multiprocessing.Process(target=run_server)
    
    clients = [
        multiprocessing.Process(target=run_client, args=("binance_agent", "binance")),
        multiprocessing.Process(target=run_client, args=("okx_agent", "okx")),
        multiprocessing.Process(target=run_client, args=("bybit_agent", "bybit")),
    ]
    
    try:
        # Start server
        server_process.start()
        logger.info("Server process started")
        
        # Start clients
        time.sleep(3)  # Give server time to initialize
        for client in clients:
            client.start()
            time.sleep(1)  # Stagger client starts
        
        logger.info("All clients started, training in progress...")
        
        # Wait for server to complete
        server_process.join()
        
        # Wait for clients to finish
        for client in clients:
            client.join(timeout=10)
            if client.is_alive():
                client.terminate()
        
        print("\n" + "="*70)
        print("DEMO COMPLETE!")
        print("="*70)
        print("\nCheck the logs above for:")
        print("- FRY alpha weights per client")
        print("- Regime distribution across clients")
        print("- Total FRY minted and slippage harvested")
        print("- Final performance report")
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nStopping demo...")
        server_process.terminate()
        for client in clients:
            client.terminate()
        print("Demo stopped")
    except Exception as e:
        logger.error(f"Demo error: {e}")
        server_process.terminate()
        for client in clients:
            client.terminate()


if __name__ == "__main__":
    # Required for multiprocessing on macOS
    multiprocessing.set_start_method('spawn', force=True)
    main()
