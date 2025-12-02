# Additional Entity Types Added - Summary

**Date:** December 2, 2025  
**Total New Examples Added:** 2,899

---

## 📊 New Entity Types Added

### **Network & Infrastructure:**
- **URL**: 300 examples
- **IPV6_ADDRESS**: 200 examples

### **Communication:**
- **PHONE_NUMBER** (International): 200 examples
- **EMOJI**: 199 examples

### **Social Media Usernames:**
- **INSTAGRAM_USERNAME**: 100 examples
- **FACEBOOK_USERNAME**: 100 examples
- **LINKEDIN_USERNAME**: 100 examples
- **TELEGRAM_USERNAME**: 100 examples
- **DISCORD_USERNAME**: 100 examples
- **SLACK_USERNAME**: 100 examples
- **WHATSAPP_USERNAME**: 100 examples

### **Social Media URLs:**
- **INSTAGRAM_URL**: 100 examples
- **FACEBOOK_URL**: 100 examples
- **LINKEDIN_URL**: 100 examples
- **TELEGRAM_URL**: 100 examples
- **DISCORD_URL**: 100 examples
- **SLACK_URL**: 100 examples
- **WHATSAPP_URL**: 100 examples

### **Geographic Coordinates:**
- **GEOJSON**: 200 examples
- **DMS_COORDINATES**: 200 examples (Degrees, Minutes, Seconds format)
- **CUSTOM_COORDINATES**: 200 examples (various custom formats)

---

## 📁 File Distribution

### **URL: 300 examples** (5 files)
- `network_security_entities.jsonl` - 60 examples
- `incident_response_entities.jsonl` - 60 examples
- `cybint_entities.jsonl` - 60 examples
- `comint_entities.jsonl` - 60 examples
- `threat_intel_entities.jsonl` - 60 examples

### **IPV6_ADDRESS: 200 examples** (4 files)
- `network_security_entities.jsonl` - 50 examples
- `cybint_entities.jsonl` - 50 examples
- `threat_intel_entities.jsonl` - 50 examples
- `incident_response_entities.jsonl` - 50 examples

### **PHONE_NUMBER (International): 200 examples** (4 files)
- `comint_entities.jsonl` - 50 examples
- `humint_entities.jsonl` - 50 examples
- `socmint_entities.jsonl` - 50 examples
- `data_privacy_sovereignty_entities.jsonl` - 50 examples

### **EMOJI: 199 examples** (3 files)
- `socmint_entities.jsonl` - 67 examples
- `comint_entities.jsonl` - 67 examples
- `humint_entities.jsonl` - 63 examples

### **Social Media Usernames: 700 examples** (across multiple files)
- **INSTAGRAM_USERNAME**: `socmint_entities.jsonl`, `comint_entities.jsonl`
- **FACEBOOK_USERNAME**: `socmint_entities.jsonl`, `comint_entities.jsonl`
- **LINKEDIN_USERNAME**: `socmint_entities.jsonl`, `humint_entities.jsonl`
- **TELEGRAM_USERNAME**: `comint_entities.jsonl`, `socmint_entities.jsonl`
- **DISCORD_USERNAME**: `comint_entities.jsonl`, `socmint_entities.jsonl`
- **SLACK_USERNAME**: `comint_entities.jsonl`, `cybint_entities.jsonl`
- **WHATSAPP_USERNAME**: `comint_entities.jsonl`, `socmint_entities.jsonl`

### **Social Media URLs: 700 examples** (across multiple files)
- **INSTAGRAM_URL**: `socmint_entities.jsonl`, `comint_entities.jsonl`
- **FACEBOOK_URL**: `socmint_entities.jsonl`, `comint_entities.jsonl`
- **LINKEDIN_URL**: `socmint_entities.jsonl`, `humint_entities.jsonl`
- **TELEGRAM_URL**: `comint_entities.jsonl`, `socmint_entities.jsonl`
- **DISCORD_URL**: `comint_entities.jsonl`, `socmint_entities.jsonl`
- **SLACK_URL**: `comint_entities.jsonl`, `cybint_entities.jsonl`
- **WHATSAPP_URL**: `comint_entities.jsonl`, `socmint_entities.jsonl`

### **GEOJSON: 200 examples** (3 files)
- `geoint_entities.jsonl` - 67 examples
- `imint_entities.jsonl` - 67 examples
- `ai-int_entities.jsonl` - 66 examples

### **DMS_COORDINATES: 200 examples** (2 files)
- `geoint_entities.jsonl` - 100 examples
- `imint_entities.jsonl` - 100 examples

### **CUSTOM_COORDINATES: 200 examples** (3 files)
- `geoint_entities.jsonl` - 67 examples
- `imint_entities.jsonl` - 67 examples
- `ai-int_entities.jsonl` - 66 examples

---

## 📋 Entity Type Formats

### **URL**
- Format: `https://domain.com/path` or `http://domain.com/path`
- Examples: `https://example.com/page`, `http://malicious.io/api/v1/data`

### **IPV6_ADDRESS**
- Format: `xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx` or compressed `::1`
- Examples: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`, `fe80::1`

### **PHONE_NUMBER (International)**
- Formats: `+1-555-123-4567`, `+44 20 7946 0958`, `+33 1 23 45 67 89`
- Supports various international formats

### **EMOJI**
- Unicode emoji characters
- Examples: 😀, 😃, 😄, ⚠️, 🚨, 🔒, 💻, 📱

### **Social Media Usernames**
- **INSTAGRAM_USERNAME**: `@username`
- **FACEBOOK_USERNAME**: `facebook.com/username`
- **LINKEDIN_USERNAME**: `linkedin.com/in/username`
- **TELEGRAM_USERNAME**: `@username`
- **DISCORD_USERNAME**: `username#1234`
- **SLACK_USERNAME**: `@username`
- **WHATSAPP_USERNAME**: `wa.me/1234567890`

### **Social Media URLs**
- **INSTAGRAM_URL**: `https://instagram.com/username`
- **FACEBOOK_URL**: `https://facebook.com/username`
- **LINKEDIN_URL**: `https://linkedin.com/in/username`
- **TELEGRAM_URL**: `https://t.me/username`
- **DISCORD_URL**: `https://discord.com/invite/code`
- **SLACK_URL**: `https://workspace.slack.com`
- **WHATSAPP_URL**: `https://wa.me/1234567890`

### **GEOJSON**
- Format: `{"type": "Point", "coordinates": [longitude, latitude]}`
- Example: `{"type": "Point", "coordinates": [13.38492, 52.53076]}`

### **DMS_COORDINATES** (Degrees, Minutes, Seconds)
- Format: `52°31'44.7"N 13°23'05.7"E`
- Traditional coordinate format with degrees, minutes, seconds

### **CUSTOM_COORDINATES**
- Various custom formats:
  - `{"location": {"latitude": 52.53076, "longitude": 13.38492}}`
  - `{"lat": 52.53076, "lng": 13.38492}`
  - `lat:52.53076,lon:13.38492`
  - `latitude=52.53076&longitude=13.38492`

---

## ✅ Entity Types Updated

The following entity types have been added to `entity_types.txt`:
- `URL`
- `IPV6_ADDRESS`
- `EMOJI`
- `INSTAGRAM_USERNAME`
- `FACEBOOK_USERNAME`
- `LINKEDIN_USERNAME`
- `TELEGRAM_USERNAME`
- `DISCORD_USERNAME`
- `SLACK_USERNAME`
- `WHATSAPP_USERNAME`
- `INSTAGRAM_URL`
- `FACEBOOK_URL`
- `LINKEDIN_URL`
- `TELEGRAM_URL`
- `DISCORD_URL`
- `SLACK_URL`
- `WHATSAPP_URL`
- `TWITTER_URL`
- `TIKTOK_URL`
- `YOUTUBE_URL`
- `REDDIT_URL`
- `SNAPCHAT_URL`
- `GEOJSON`
- `DMS_COORDINATES`
- `CUSTOM_COORDINATES`

---

## 📊 Total Examples Added

**Previous Critical Entities:** 3,085 examples  
**Additional Entities:** 2,899 examples  
**Grand Total:** **5,984 new examples** added to training data

---

## 🎯 Coverage Summary

### **Network & Infrastructure:**
- ✅ URLs (300 examples)
- ✅ IPv6 addresses (200 examples)
- ✅ IPv4 addresses (already had 620 examples)

### **Communication:**
- ✅ International phone numbers (200 examples)
- ✅ Emojis (199 examples)
- ✅ Email addresses (already had 466 examples)

### **Social Media:**
- ✅ 7 platform usernames (700 examples)
- ✅ 7 platform URLs (700 examples)

### **Geographic Data:**
- ✅ GeoJSON format (200 examples)
- ✅ DMS coordinates (200 examples)
- ✅ Custom coordinate formats (200 examples)
- ✅ Latitude/Longitude (already had 400 each)

---

**All requested entity types have been successfully added with accurate boundaries and realistic examples!** ✅

