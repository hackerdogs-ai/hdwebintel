#!/bin/bash

# Script to generate self-signed certificates for web and mcp services
# Usage: ./generate-certificates.sh [options]
# Options:
#   --ca-name NAME          Common Name for CA certificate (default: hackerdogs inc.)
#   --web-name NAME         Common Name for web service certificate (default: text intelligence web)
#   --mcp-name NAME         Common Name for MCP service certificate (default: text intelligence mcp)
#   --org ORGANIZATION      Organization name (default: HackerDogs)
#   --country CODE           Country code (default: US)
#   --state STATE           State/Province (default: CA)
#   --city CITY             City (default: San Francisco)
#   --days DAYS             Certificate validity in days (default: 1095 = 3 years)
#   --domain DOMAIN         Additional domain for SAN (Subject Alternative Name)
#   --ip IP                 Additional IP address for SAN

set -e

# Default values
CERT_DIR="./certs"
CA_NAME="${CA_NAME:-hackerdogs inc.}"
WEB_NAME="${WEB_NAME:-text intelligence web}"
MCP_NAME="${MCP_NAME:-text intelligence mcp}"
ORG="${ORG:-HackerDogs}"
COUNTRY="${COUNTRY:-US}"
STATE="${STATE:-CA}"
CITY="${CITY:-San Francisco}"
DAYS="${DAYS:-1095}"  # 3 years (3 * 365)
ADDITIONAL_DOMAIN="${ADDITIONAL_DOMAIN:-}"
ADDITIONAL_IP="${ADDITIONAL_IP:-}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --ca-name)
            CA_NAME="$2"
            shift 2
            ;;
        --web-name)
            WEB_NAME="$2"
            shift 2
            ;;
        --mcp-name)
            MCP_NAME="$2"
            shift 2
            ;;
        --org)
            ORG="$2"
            shift 2
            ;;
        --country)
            COUNTRY="$2"
            shift 2
            ;;
        --state)
            STATE="$2"
            shift 2
            ;;
        --city)
            CITY="$2"
            shift 2
            ;;
        --days)
            DAYS="$2"
            shift 2
            ;;
        --domain)
            ADDITIONAL_DOMAIN="$2"
            shift 2
            ;;
        --ip)
            ADDITIONAL_IP="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--ca-name NAME] [--web-name NAME] [--mcp-name NAME] [--org ORG] [--country CODE] [--state STATE] [--city CITY] [--days DAYS] [--domain DOMAIN] [--ip IP]"
            exit 1
            ;;
    esac
done

mkdir -p "$CERT_DIR"

echo "Generating self-signed certificates..."
echo "CA Name: $CA_NAME"
echo "Web Service Name: $WEB_NAME"
echo "MCP Service Name: $MCP_NAME"
echo "Organization: $ORG"
echo "Validity: $DAYS days"
echo ""

# Build SAN (Subject Alternative Name) list
SAN_LIST="DNS:${WEB_NAME},DNS:localhost,IP:127.0.0.1"
if [ -n "$ADDITIONAL_DOMAIN" ]; then
    SAN_LIST="${SAN_LIST},DNS:${ADDITIONAL_DOMAIN}"
fi
if [ -n "$ADDITIONAL_IP" ]; then
    SAN_LIST="${SAN_LIST},IP:${ADDITIONAL_IP}"
fi

MCP_SAN_LIST="DNS:${MCP_NAME},DNS:localhost,IP:127.0.0.1"
if [ -n "$ADDITIONAL_DOMAIN" ]; then
    MCP_SAN_LIST="${MCP_SAN_LIST},DNS:${ADDITIONAL_DOMAIN}"
fi
if [ -n "$ADDITIONAL_IP" ]; then
    MCP_SAN_LIST="${MCP_SAN_LIST},IP:${ADDITIONAL_IP}"
fi

# Generate CA private key
echo "Generating CA private key..."
openssl genrsa -out "$CERT_DIR/ca-key.pem" 4096

# Generate CA certificate
echo "Generating CA certificate..."
openssl req -new -x509 -days "$DAYS" -key "$CERT_DIR/ca-key.pem" \
    -out "$CERT_DIR/ca-cert.pem" \
    -subj "/C=${COUNTRY}/ST=${STATE}/L=${CITY}/O=${ORG}/CN=${CA_NAME}"

# Generate web service private key
echo "Generating web service private key..."
openssl genrsa -out "$CERT_DIR/web-key.pem" 4096

# Generate web service certificate signing request
echo "Generating web service certificate signing request..."
openssl req -new -key "$CERT_DIR/web-key.pem" \
    -out "$CERT_DIR/web.csr" \
    -subj "/C=${COUNTRY}/ST=${STATE}/L=${CITY}/O=${ORG}/CN=${WEB_NAME}"

# Generate web service certificate signed by CA
echo "Generating web service certificate..."
openssl x509 -req -days "$DAYS" -in "$CERT_DIR/web.csr" \
    -CA "$CERT_DIR/ca-cert.pem" \
    -CAkey "$CERT_DIR/ca-key.pem" \
    -CAcreateserial \
    -out "$CERT_DIR/web-cert.pem" \
    -extensions v3_req \
    -extfile <(echo "[v3_req]"; echo "subjectAltName=${SAN_LIST}")

# Generate MCP service private key
echo "Generating MCP service private key..."
openssl genrsa -out "$CERT_DIR/mcp-key.pem" 4096

# Generate MCP service certificate signing request
echo "Generating MCP service certificate signing request..."
openssl req -new -key "$CERT_DIR/mcp-key.pem" \
    -out "$CERT_DIR/mcp.csr" \
    -subj "/C=${COUNTRY}/ST=${STATE}/L=${CITY}/O=${ORG}/CN=${MCP_NAME}"

# Generate MCP service certificate signed by CA
echo "Generating MCP service certificate..."
openssl x509 -req -days "$DAYS" -in "$CERT_DIR/mcp.csr" \
    -CA "$CERT_DIR/ca-cert.pem" \
    -CAkey "$CERT_DIR/ca-key.pem" \
    -CAcreateserial \
    -out "$CERT_DIR/mcp-cert.pem" \
    -extensions v3_req \
    -extfile <(echo "[v3_req]"; echo "subjectAltName=${MCP_SAN_LIST}")

# Clean up CSR files
rm -f "$CERT_DIR/web.csr" "$CERT_DIR/mcp.csr"

# Set appropriate permissions
chmod 600 "$CERT_DIR"/*.pem
chmod 644 "$CERT_DIR"/*.pem 2>/dev/null || true

echo "Certificates generated successfully in $CERT_DIR/"
echo "Files created:"
echo "  - ca-cert.pem (CA certificate)"
echo "  - ca-key.pem (CA private key)"
echo "  - web-cert.pem (Web service certificate)"
echo "  - web-key.pem (Web service private key)"
echo "  - mcp-cert.pem (MCP service certificate)"
echo "  - mcp-key.pem (MCP service private key)"

