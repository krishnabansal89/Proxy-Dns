from dnslib import DNSRecord
import socket
import threading

# Define the IP and port for your DNS proxy server
proxy_host = '0.0.0.0'  # Listen on all available network interfaces
proxy_port = 53

# Define the DNS server you want to forward requests to
dns_server = ('8.8.8.8', 53)

def dns_proxy(query_data, client_address):
    try:
        q = DNSRecord.parse(query_data)
        query_name = q.q.qname.idna()
        print("Received DNS query for:", query_name)
        
        response = forward_dns_query(query_data, dns_server)
        server_socket.sendto(response, client_address)
    except Exception as e:
        print("Error handling DNS request:", e)

def forward_dns_query(query_data, server_address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(query_data, server_address)
        response, _ = sock.recvfrom(1024)
        return response

# Create a socket to listen for DNS queries
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((proxy_host, proxy_port))
    print("DNS proxy server listening on", proxy_host, "port", proxy_port)
    
    while True:
        try:
            query_data, client_address = server_socket.recvfrom(1024)
            thread = threading.Thread(target=dns_proxy, args=(query_data, client_address))
            thread.setDaemon(True)  # Set the thread as a daemon
            thread.start()
        except Exception as e:
            print("Error receiving DNS query:", e)