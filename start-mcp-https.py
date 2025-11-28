#!/usr/bin/env python3
"""
HTTPS-enabled startup script for MCP Server
This script wraps the MCP server to enable HTTPS when certificates are available.
"""

import os
import sys
import argparse
import subprocess

# Get SSL certificate paths from environment
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH', '/app/certs/mcp-cert.pem')
SSL_KEY_PATH = os.getenv('SSL_KEY_PATH', '/app/certs/mcp-key.pem')
MCP_TRANSPORT = os.getenv('MCP_TRANSPORT', 'https')
MCP_HOST = os.getenv('MCP_HOST', '0.0.0.0')
MCP_PORT = int(os.getenv('MCP_PORT', '8443'))

def check_certificates():
    """Check if SSL certificates exist"""
    cert_exists = os.path.exists(SSL_CERT_PATH)
    key_exists = os.path.exists(SSL_KEY_PATH)
    return cert_exists and key_exists

def main():
    """Start the MCP server with HTTPS support"""
    parser = argparse.ArgumentParser(description='Start MCP server with HTTPS support')
    parser.add_argument('--transport', default=MCP_TRANSPORT, help='Transport protocol (http/https)')
    parser.add_argument('--host', default=MCP_HOST, help='Host to bind to')
    parser.add_argument('--port', type=int, default=MCP_PORT, help='Port to bind to')
    args = parser.parse_args()
    
    # Check if we should use HTTPS
    use_https = args.transport.lower() == 'https'
    has_certs = check_certificates()
    
    if use_https and has_certs:
        print(f"Starting MCP server with HTTPS on {args.host}:{args.port}")
        print(f"Certificate: {SSL_CERT_PATH}")
        print(f"Key: {SSL_KEY_PATH}")
        
        # Set environment variables for HTTPS
        os.environ['MCP_TRANSPORT'] = 'https'
        os.environ['SSL_CERT_PATH'] = SSL_CERT_PATH
        os.environ['SSL_KEY_PATH'] = SSL_KEY_PATH
        
        # Try to use uvicorn with SSL if server.py exports an ASGI app
        try:
            import uvicorn
            # Try to import the app from server.py
            try:
                from server import app
                # Run with HTTPS using uvicorn
                uvicorn.run(
                    app,
                    host=args.host,
                    port=args.port,
                    ssl_keyfile=SSL_KEY_PATH,
                    ssl_certfile=SSL_CERT_PATH,
                    log_level="info"
                )
                return
            except (ImportError, AttributeError):
                # server.py doesn't export 'app', try running it directly
                pass
        except ImportError:
            pass
        
        # Fallback: run server.py directly with HTTPS environment
        # The server.py should handle HTTPS based on environment variables
        subprocess.run([sys.executable, 'server.py', '--transport', 'https', '--host', args.host, '--port', str(args.port)])
        
    elif use_https and not has_certs:
        print(f"Warning: HTTPS requested but certificates not found!")
        print(f"  Certificate: {SSL_CERT_PATH}")
        print(f"  Key: {SSL_KEY_PATH}")
        print(f"Falling back to HTTP on port 8004")
        args.transport = 'http'
        args.port = 8004
    
    if args.transport.lower() == 'http':
        print(f"Starting MCP server with HTTP on {args.host}:{args.port}")
        
        # Set environment for HTTP
        os.environ['MCP_TRANSPORT'] = 'http'
        
        # Try uvicorn first
        try:
            import uvicorn
            try:
                from server import app
                uvicorn.run(
                    app,
                    host=args.host,
                    port=args.port,
                    log_level="info"
                )
                return
            except (ImportError, AttributeError):
                pass
        except ImportError:
            pass
        
        # Fallback: run server.py directly
        subprocess.run([sys.executable, 'server.py', '--transport', 'http', '--host', args.host, '--port', str(args.port)])

if __name__ == '__main__':
    main()

