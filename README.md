# NLP Web Service

Comprehensive NLP and web content analysis service with OpenAPI documentation and MCP server support.

## Features

- **NLP Analysis**: Language detection, entity extraction, text analysis
- **Web Content Analysis**: Webpage scraping, metadata extraction, link analysis
- **Sensitive Data Detection**: Credit cards, SSN, IPs, emails, phones
- **Geographic Analysis**: IP geolocation, distance calculations
- **OpenAPI Documentation**: Full API documentation with Swagger UI
- **MCP Server**: Model Context Protocol server for AI integration

## Architecture

- **API Service** (`onerow_nlp.py`): Flask-based REST API with OpenAPI documentation
- **MCP Server** (`server.py`): FastMCP server that directly calls functions from `onerow_nlp.py`

## Installation

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This will start both services:
- API: http://localhost:5000
- MCP Server: http://localhost:8004

### Manual Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
pip install flask-restx fastmcp uvicorn python-dotenv
```

2. Download GeoIP databases to `data/` directory:
   - GeoLite2-City.mmdb
   - GeoLite2-Country.mmdb
   - GeoLite2-ASN.mmdb

3. Run API service:
```bash
python onerow_nlp.py
```

4. Run MCP server:
```bash
python server.py --transport http --host 0.0.0.0 --port 8004
```

## API Documentation

Once the API is running, access the OpenAPI documentation at:
- Swagger UI: http://localhost:5000/webc/api/docs/

## MCP Server

The MCP server provides the same functionality as the API but through the Model Context Protocol, allowing direct integration with AI assistants.

### Available Tools

- `detect_language`: Detect language of text
- `extract_entities`: Extract named entities
- `extract_emails`: Extract email addresses
- `extract_phones`: Extract phone numbers
- `find_sensitive_data`: Find sensitive data (SSN, credit cards, etc.)
- `get_readability_stats`: Get readability statistics
- `get_keyterms`: Extract key terms
- `calculate_similarity`: Calculate text similarity
- `analyze_webpage`: Comprehensive webpage analysis
- `get_geo_distance`: Calculate geographic distance
- `get_geo_ip_distance`: Calculate distance between IPs
- `resolve_domain_ips`: Resolve domain to IPs
- `get_whois_info`: Get WHOIS information
- `remove_stopwords`: Remove stopwords from text
- `clean_text`: Clean and normalize text
- `translate_text`: Translate text

## Memory Management

The code includes proper memory management:
- GeoIP database readers are properly closed on exit
- Resource cleanup via `atexit` handlers
- Proper logging instead of print statements
- Cache management with TTL

## Development

### Code Quality

- All functions use proper logging (`logger.info`, `logger.error`)
- Resource cleanup on exit
- Error handling with proper exceptions
- OpenAPI documentation for all endpoints

### Testing

Test the API:
```bash
curl http://localhost:5000/webc/api/version
```

Test the MCP server:
```bash
curl http://localhost:8004/health
```

## License

See LICENSE file for details.

