#!/bin/bash
# SSL/TLS Certificate Setup Script for LibraryProject
# This script helps set up SSL certificates for production deployment

set -e

echo "í´ SSL/TLS Certificate Setup for LibraryProject"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root or with sudo${NC}"
    exit 1
fi

# Create SSL directory
SSL_DIR="/etc/ssl/libraryproject"
echo -e "${YELLOW}Creating SSL directory...${NC}"
mkdir -p $SSL_DIR
chmod 700 $SSL_DIR

# Generate self-signed certificate (for testing only)
echo -e "${YELLOW}Generating self-signed certificate (for testing)...${NC}"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout $SSL_DIR/private.key \
    -out $SSL_DIR/certificate.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=example.com"

# Set proper permissions
echo -e "${YELLOW}Setting file permissions...${NC}"
chmod 600 $SSL_DIR/private.key
chmod 644 $SSL_DIR/certificate.crt

# Create certificate bundle
cat $SSL_DIR/certificate.crt > $SSL_DIR/ca-bundle.crt

echo -e "${GREEN}âœ… SSL certificates generated successfully!${NC}"
echo ""
echo -e "${YELLOW}Certificate locations:${NC}"
echo "Private Key: $SSL_DIR/private.key"
echo "Certificate: $SSL_DIR/certificate.crt"
echo "CA Bundle:   $SSL_DIR/ca-bundle.crt"
echo ""
echo -e "${YELLOW}For production, replace these with certificates from a trusted CA${NC}"
echo "Recommended CAs: Let's Encrypt, DigiCert, Comodo, etc."
