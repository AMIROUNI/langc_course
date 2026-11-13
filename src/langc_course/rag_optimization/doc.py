
from langchain_core.documents import Document

document = Document(
    page_content="""
    Company: TechNova Solutions
    Department: IT Infrastructure
    Document Title: Network Infrastructure and Troubleshooting Guide
    Version: 1.0

    1. Network Infrastructure

    TechNova Solutions uses a centralized network infrastructure
    to connect employees, servers, databases, and internal applications.

    The company uses enterprise routers with high-speed Ethernet
    connectivity and managed switches to distribute network traffic.

    The main router supports VLAN segmentation, firewall rules,
    Quality of Service (QoS), and VPN connectivity.

    2. DNS Configuration

    DNS (Domain Name System) translates domain names into IP addresses.

    If employees cannot access websites but their internet connection
    is working, the IT team should investigate DNS configuration.

    Recommended troubleshooting steps:
    - Check the configured DNS server.
    - Test domain resolution using nslookup.
    - Verify network connectivity.
    - Check whether the DNS service is available.

    3. Common Network Errors

    Error: E_CONN_REFUSED

    This error occurs when a client attempts to connect to a server
    but the destination server refuses the connection.

    Possible causes:
    - The server application is not running.
    - The destination port is incorrect.
    - A firewall is blocking the connection.

    Resolution:
    Verify the server status, inspect the destination port,
    and review firewall configuration.

    4. Network Security

    The company protects its internal infrastructure using
    firewalls, VPN connections, network segmentation,
    and multi-factor authentication (MFA).

    Employees must use secure authentication methods when
    accessing internal company resources.

    5. Backup and Disaster Recovery

    Critical infrastructure configurations and databases
    must be backed up regularly.

    Backups help restore services after accidental deletion,
    hardware failures, or unexpected system interruptions.

    The IT department should periodically test backup restoration
    procedures to verify data integrity.
    """,

    metadata={
        "company": "TechNova Solutions",
        "department": "IT Infrastructure",
        "document_type": "technical_guide",
        "category": "networking",
        "version": "1.0",
        "source": "internal_it_documentation"
    }
)
