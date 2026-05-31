import socket

def grab_banner(ip, port):
    try:
        #creating a tcp socket connection (AF_iNET = ipv4 sock_stream = tcp)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# setting the timeout 1 sec to avoid the hanging on filtered ports/ porrts not responding        
        sock.settimeout(1)
# connect_ex insted of connect to return the error instead of raising
        result = sock.connect_ex((ip, port))
        if result != 0:
            sock.close()
            return None

        banner = ""
# http requires a request to trigger the banner, unlike FTP/SSH
        # HTTP request (port 80)
        if port == 80:
            sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")

        # try to read response of the first 4096 bytes 
        try:
            banner = sock.recv(4096).decode(errors="ignore")
        except:
            banner = ""

        sock.close()

        return banner.strip()

    except:
        return None


def extract_server_info(banner):
    info = {}

    if not banner:
        return info

    lines = banner.split("\n")

    for line in lines:
        line = line.strip()

        if line.startswith("Server:"):
            info["server"] = line.split(":", 1)[1].strip()

        if line.startswith("HTTP/"):
            info["http_status"] = line

        if "OpenSSH" in line:
            info["ssh"] = line

        if "FTP" in line or "220" in line:
            info["ftp"] = line

    return info


def scan(target, ports):
    print(f"\nScanning {target}...\n")

    results = {}

    for port in ports:
        banner = grab_banner(target, port)

        if banner:
            info = extract_server_info(banner)

            results[port] = {
                "open": True,
                "info": info,
                "raw_banner": banner.split("\n")[0]  # first line only
            }

            print(f"[+] Port {port} OPEN")
            print(f"    {info if info else 'No clear banner'}")

        else:
            print(f"[-] Port {port} CLOSED or NO RESPONSE")

    return results


if __name__ == "__main__":
    target = input("Target IP: ")

    ports = [21, 22, 25, 80, 443]

    results = scan(target, ports)

    print("\n\n===== SUMMARY =====")
    for port, data in results.items():
        print(f"Port {port}: {data['info']}") 
