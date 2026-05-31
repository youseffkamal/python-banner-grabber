# Custom Python Banner Grabber

## 📌 Overview
A lightweight, manual banner grabbing tool developed to deepen understanding of **TCP socket programming** and **application-layer protocol handshakes**. 

Unlike automated scanners, this tool was built from scratch using Python’s raw `socket` library to demonstrate how different services (HTTP, FTP, SSH) behave during the initial connection phase. This project reinforces the concept that effective penetration testing requires understanding *what* is happening at the packet level, not just *which* tool to run.

## 🚀 Key Features
*   **Raw Socket Implementation:** Uses `socket.AF_INET` and `socket.SOCK_STREAM` to manually establish TCP connections without external dependencies.
*   **Protocol-Aware Logic:** 
    *   Detects **HTTP** services by sending a minimal `GET / HTTP/1.1` request to trigger server headers.
    *   Captures immediate banners from **FTP** and **SSH** services upon connection.
*   **Robust Error Handling:** Implements `sock.settimeout()` to gracefully handle filtered ports or unresponsive hosts without hanging the script.
*   **Information Extraction:** Parses raw byte streams to identify specific service versions (e.g., Apache, OpenSSH) and HTTP status codes.

## 🛠️ Technical Insights
*   **TCP Handshake:** The script performs a standard 3-way handshake (SYN → SYN-ACK → ACK) via `sock.connect_ex()`. Using `connect_ex` allows for cleaner error handling compared to `connect()`.
*   **HTTP Behavior:** Most services send a banner immediately after the handshake. HTTP servers, however, often wait for a client request. This script mimics a basic browser request to provoke a `Server:` header response.
*   **Data Parsing:** The `extract_server_info` function splits the raw response by newlines and uses string manipulation to isolate key identifiers like `Server: Apache/2.4.x`.

## 📸 Wireshark Validation
This tool was validated using **Wireshark** to ensure:
1.  The TCP 3-way handshake completes successfully.
2.  The HTTP GET request is formatted correctly (`\r\n\r\n`).
3.  The server response matches expected protocol behavior (e.g., `HTTP/1.1 200 OK`).

## 💻 Usage
1.  Clone the repository:
    ```bash
    git clone https://github.com/youseffkamal/python-banner-grabber.git
    cd python-banner-grabber
    ```
2.  Run the script:
    ```bash
    python3 banner_grabber.py
    ```
3.  Enter the target IP when prompted. The script scans common ports (21, 22, 25, 80, 443) by default.

## 🎓 Learning Outcome
This project bridged the gap between theoretical networking knowledge (CCNP Security) and practical scripting. It reinforced my ability to:
*   Analyze traffic at the **packet level**.
*   Understand **protocol-specific nuances** (e.g., why HTTP requires a request while SSH does not).
*   Write clean, functional **Python automation** for reconnaissance tasks.

## 📄 License
This project is for educational and ethical penetration testing purposes only.
