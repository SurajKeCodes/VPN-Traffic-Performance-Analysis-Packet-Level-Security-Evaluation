import subprocess
import time

# VPN servers (file names must be in same folder)
servers = [
    ("US", "vpnbook-us16-udp25000.ovpn"),
    ("UK", "vpnbook-uk205-udp25000.ovpn"),
    ("GERMANY", "vpnbook-de20-udp25000.ovpn")
]

USERNAME = "vpnbook"
PASSWORD = "939pxfv"

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def get_ping():
    result = run_cmd("ping -c 5 google.com")
    for line in result.stdout.split("\n"):
        if "rtt min/avg/max" in line:
            return float(line.split("/")[4])
    return None

def get_speed():
    result = run_cmd("curl -o /dev/null -s -w '%{speed_download}' http://speedtest.tele2.net/1MB.zip")
    speed_bytes = float(result.stdout)
    speed_mbps = (speed_bytes * 8) / (1024 * 1024)
    return round(speed_mbps, 2)

def start_vpn(config):
    print(f"\n🔐 Connecting to {config}...")
    cmd = f"echo -e '{USERNAME}\\n{PASSWORD}' | sudo openvpn --config {config} --auth-nocache"
    return subprocess.Popen(cmd, shell=True)

def wait_for_tun0():
    print("⏳ Waiting for VPN (tun0)...")
    for _ in range(20):  # wait max 20 sec
        result = subprocess.run("ip a", shell=True, capture_output=True, text=True)
        if "tun0" in result.stdout:
            print("✅ VPN Connected (tun0 ready)")
            return True
        time.sleep(1)
    print("❌ tun0 not found!")
    return False

def stop_vpn(process):
    print("❌ Disconnecting VPN...")
    process.terminate()
    time.sleep(3)

def capture_packets(label, interface):
    print(f"📡 Capturing packets: {label} on {interface}")
    subprocess.run(f"sudo timeout 10 tcpdump -i {interface} -w {label}.pcap", shell=True)

def run_test(label):
    print(f"\n--- {label} ---")
    latency = get_ping()
    speed = get_speed()
    print(f"Latency: {latency} ms | Speed: {speed} Mbps")
    return latency, speed

def main():
    results = {}

    # 🔴 WITHOUT VPN (eth0)
    input("➡️ Press ENTER for WITHOUT VPN test...")
    results["No VPN"] = run_test("No VPN")
    capture_packets("no_vpn", "eth0")

    # 🔵 WITH VPN (tun0)
    for name, config in servers:
        input(f"\n➡️ Press ENTER to test {name} VPN...")

        vpn = start_vpn(config)

        # ✅ wait until tun0 is ready
        if not wait_for_tun0():
            print("Skipping this VPN...")
            continue

        results[name] = run_test(name)
        capture_packets(name, "tun0")

        stop_vpn(vpn)

    print("\n=== FINAL RESULTS ===")
    for key, value in results.items():
        print(f"{key}: Latency={value[0]} ms, Speed={value[1]} Mbps")

if __name__ == "__main__":
    main()
