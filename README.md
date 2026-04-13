# 🔐 VPN Traffic Performance Analysis & Packet-Level Security Evaluation

## 🚀 Overview

This project analyzes the impact of Virtual Private Networks (VPNs) on network performance and security. It compares **latency, throughput, and packet-level behavior** between normal internet traffic and VPN-secured traffic using OpenVPN and packet capture tools.

The project demonstrates how VPNs encrypt data and alter traffic flow using real-world experimentation on multiple servers.


## 🎯 Objectives

* Measure network performance (latency & throughput) with and without VPN
* Analyze encrypted vs non-encrypted traffic
* Understand VPN tunneling using **tun interfaces**
* Perform packet-level inspection using Wireshark/tcpdump



<img width="1189" height="753" alt="image" src="https://github.com/user-attachments/assets/245d28e2-04d6-49ca-b137-77f0695168a3" />

<img width="1901" height="778" alt="image" src="https://github.com/user-attachments/assets/df2c24fa-8d0a-4eda-b8dc-ce8ece2ebebb" />

<img width="1895" height="741" alt="image" src="https://github.com/user-attachments/assets/82a0b7f2-33f5-48e5-8ea4-b4ec77289e6e" />  

## 🛠️ Tech Stack

* **Operating System:** Kali Linux
* **VPN:** OpenVPN
* **Packet Analysis:** Wireshark, tcpdump
* **Networking Tools:** ping, curl
* **Programming (Optional Automation):** Python



## 🌐 VPN Servers Used

* 🇺🇸 US Server (vpnbook-us16)
* 🇬🇧 UK Server (vpnbook-uk205)
* 🇩🇪 Germany Server (vpnbook-de20)



## ⚙️ Methodology

### 🔴 Without VPN

* Measured latency using `ping`
* Measured speed using `curl`
* Captured packets using:

  ```bash
  tcpdump -i eth0 -w no_vpn.pcap
  ```


### 🔵 With VPN

* Connected using OpenVPN:

  ```bash
  sudo openvpn --config <server>.ovpn
  ```
* Verified VPN tunnel (`tun0`) using:

  ```bash
  ip a
  ```
* Measured performance again
* Captured encrypted traffic:

  ```bash
  tcpdump -i tun0 -w <server>.pcap
  ```

---

## 📊 Results

| Case        | Latency (ms) | Speed (Mbps) |
| ----------- | ------------ | ------------ |
| No VPN      | ~99          | ~1.58        |
| US VPN      | ~116         | ~1.33        |
| UK VPN      | ~103         | ~1.37        |
| Germany VPN | ~102         | ~1.40        |

---

## 🔍 Packet Analysis

### Without VPN

* Protocol: TCP / HTTP
* Data: Readable
* Traffic: Direct communication

### With VPN

* Protocol: UDP (OpenVPN)
* Data: Encrypted
* Interface: `tun0`
* Payload: Not readable

---

## 🧠 Key Insights

* VPN introduces **encryption and tunneling**
* Latency may increase due to routing and encryption overhead
* Throughput depends on server location and network conditions
* Packet capture confirms **secure communication via encryption**

---

## 📁 Project Structure

```
vpn-project/
│── vpn_auto_analysis.py
│── vpnbook-*.ovpn
│── no_vpn.pcap
│── US.pcap
│── UK.pcap
│── GERMANY.pcap
```

---

## 📌 Conclusion

This project demonstrates that VPNs significantly enhance privacy by encrypting network traffic, making it unreadable to external observers. While there may be slight performance variations, the security benefits outweigh the trade-offs.

---

## 🚀 Future Improvements

* Automated result visualization (graphs)
* Multi-threaded testing
* Integration with WireGuard VPN
* Advanced traffic analysis using Scapy

---

## 👨‍💻 Author

**Suraj Borkute**
📍 Nagpur, India
📧 [surajborkute.tech@gmail.com](mailto:surajborkute.tech@gmail.com)

---

## 📜 License

This project is for educational and research purposes.
