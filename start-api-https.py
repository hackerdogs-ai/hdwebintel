#!/usr/bin/env python3
"""
HTTPS-enabled startup script for Flask API
This script wraps the Flask application to enable HTTPS when certificates are available.
"""

import os
import sys
import ssl

# Get SSL certificate paths from environment
SSL_CERT_PATH = os.getenv('SSL_CERT_PATH', '/app/certs/web-cert.pem')
SSL_KEY_PATH = os.getenv('SSL_KEY_PATH', '/app/certs/web-key.pem')
HTTPS_PORT = int(os.getenv('HTTPS_PORT', '5443'))
HTTP_PORT = int(os.getenv('HTTP_PORT', '5000'))

def create_ssl_context():
    """Create SSL context if certificates exist"""
    if os.path.exists(SSL_CERT_PATH) and os.path.exists(SSL_KEY_PATH):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(SSL_CERT_PATH, SSL_KEY_PATH)
            return context
        except Exception as e:
            print(f"Error creating SSL context: {e}")
            return None
    return None

def main():
    """Start the Flask application with HTTPS support"""
    # Import the Flask app
    try:
        from onerow_nlp import app
    except ImportError:
        print("Error: Could not import onerow_nlp. Make sure onerow_nlp.py exists.")
        print("Attempting to import app directly...")
        try:
            # Try alternative import
            import onerow_nlp
            app = onerow_nlp.app
        except (ImportError, AttributeError):
            print("Error: Could not find Flask app. Please ensure onerow_nlp.py exists and defines 'app'.")
            sys.exit(1)
    
    ssl_context = create_ssl_context()
    
    if ssl_context:
        print(f"Starting Flask API with HTTPS on port {HTTPS_PORT}")
        print(f"Certificate: {SSL_CERT_PATH}")
        print(f"Key: {SSL_KEY_PATH}")
        # Run with HTTPS
        app.run(
            host='0.0.0.0',
            port=HTTPS_PORT,
            ssl_context=ssl_context,
            debug=False
        )
    else:
        print(f"SSL certificates not found. Starting Flask API with HTTP on port {HTTP_PORT}")
        print(f"Looking for cert at: {SSL_CERT_PATH}")
        print(f"Looking for key at: {SSL_KEY_PATH}")
        # Fallback to HTTP
        app.run(
            host='0.0.0.0',
            port=HTTP_PORT,
            debug=False
        )

if __name__ == '__main__':
    main()

