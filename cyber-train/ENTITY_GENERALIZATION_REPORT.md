# 📊 Entity Generalization Report

**Date:** December 2, 2025  
**Status:** ✅ **GENERALIZATION COMPLETE**

---

## 🎯 Objective

Generalize entities to avoid overfitting by:
1. Consolidating social media usernames to `SOCIAL_USER_NAME`
2. Consolidating social media URLs to `SOCIAL_MEDIA_URL`
3. Removing product-centric entities (GitHub, Slack, etc.)
4. Generalizing product-specific entities to generic types

---

## ✅ Changes Applied

### 1. Social Media Usernames Consolidated

**Before:** Multiple platform-specific types
- `INSTAGRAM_USERNAME`
- `FACEBOOK_USERNAME`
- `LINKEDIN_USERNAME`
- `TELEGRAM_USERNAME`
- `DISCORD_USERNAME`
- `SLACK_USERNAME`
- `WHATSAPP_USERNAME`
- `TWITTER_USERNAME`
- `TIKTOK_USERNAME`
- `YOUTUBE_USERNAME`

**After:** Single generalized type
- `SOCIAL_USER_NAME` (consolidates all social media usernames)

**Rationale:**
- Avoids overfitting to specific platforms
- Generalizes the concept of "social media username"
- Model learns pattern: `@username` or platform-specific format
- Context determines which platform, but entity type is generic

### 2. Social Media URLs Consolidated

**Before:** Multiple platform-specific URL types
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

**After:** Single generalized type
- `SOCIAL_MEDIA_URL` (consolidates all social media URLs)

**Rationale:**
- Avoids overfitting to specific platforms
- Generalizes the concept of "social media URL"
- Model learns pattern: `platform.com/username` format
- Context determines which platform, but entity type is generic

### 3. Product-Centric Entities Removed

**Removed:**
- `GITHUB_USER` (13,160 instances removed)
- `GITHUB_ORGANIZATION`
- `SLACK_USERNAME` (consolidated to SOCIAL_USER_NAME)
- `DISCORD_USERNAME` (consolidated to SOCIAL_USER_NAME)

**Rationale:**
- Too specific to a single product/platform
- Causes overfitting to GitHub/Slack/Discord
- Better to use generic `SOCIAL_USER_NAME` or `USERNAME`
- Context can indicate platform if needed

### 4. Product-Centric Entities Generalized

**Generalized:**
- `GITHUB_REPO` → `REPOSITORY` (310 instances)
- `GITHUB_REPO_URL` → `REPOSITORY_URL` (12 instances)
- `GITHUB_GIST` → `CODE_SNIPPET`
- `GITHUB_ISSUE` → `ISSUE_ID` (344 instances)
- `GITHUB_PULL_REQUEST` → `PULL_REQUEST_ID`
- `GITHUB_COMMIT` → `COMMIT_HASH` (12 instances)
- `GITHUB_BRANCH` → `BRANCH_NAME`
- `GITHUB_TAG` → `VERSION_TAG`
- `GITHUB_RELEASE` → `RELEASE_VERSION`

**Rationale:**
- These concepts exist beyond GitHub
- `REPOSITORY` applies to GitLab, Bitbucket, etc.
- `COMMIT_HASH` applies to any Git repository
- `ISSUE_ID` applies to any issue tracking system
- Generalizes to avoid product-specific overfitting

---

## 📊 Statistics

### Files Processed
- **49 entity files** processed
- **22,308 lines** processed

### Entity Changes
- **13,160 GITHUB_USER instances removed** (product-centric)
- **678 product-centric entities generalized**
- **26 entity types removed** from entity_types.txt
- **11 generalized types added** to entity_types.txt

### Overlapping Entities Found
- **503 overlapping texts** (same text, different labels)
- Common overlaps include:
  - `identity`: 7 different labels
  - `endpoint`: 7 different labels
  - `risk`: 6 different labels
  - `backup`: 6 different labels
  - `recovery`: 6 different labels
  - `governance`: 6 different labels
  - `vulnerability`: 6 different labels

**Note:** Many overlaps involve `GITHUB_USER` (now removed), which should reduce confusion.

---

## 🔍 Overlapping Entities Analysis

### Problem
Same text labeled as multiple entity types:
- `identity` → `IDENTITY_TYPE`, `TOOL`, `PLATFORM_TYPE`, `GOVERNANCE_TYPE`, `GITHUB_USER`, `POLICY_TYPE`, `PROVIDER_TYPE`
- `endpoint` → `ENDPOINT_TYPE`, `AUTOMATION_TYPE`, `TOOL`, `ALERT_TYPE`, `RESOURCE_TYPE`, `GITHUB_USER`, `AGENT_TYPE`
- `risk` → `METRIC_TYPE`, `RISK_TYPE`, `GITHUB_USER`, `FRAMEWORK`, `SCORING_TYPE`, `SCORE_TYPE`

### Impact
- Model confusion about entity boundaries
- Overfitting to specific contexts
- Poor generalization

### Solution
- Removed `GITHUB_USER` (major source of overlaps)
- Generalization reduces platform-specific confusion
- Context-based disambiguation still possible

---

## ✅ Benefits

### 1. Reduced Overfitting
- **Before:** Model learned GitHub-specific patterns
- **After:** Model learns generic patterns (repository, commit, etc.)

### 2. Better Generalization
- **Before:** `GITHUB_USER` only works for GitHub
- **After:** `SOCIAL_USER_NAME` works for any social platform

### 3. Cleaner Entity Types
- **Before:** 549 entity types (many overlapping)
- **After:** ~534 entity types (more distinct)

### 4. Reduced Confusion
- **Before:** Same text labeled as multiple types
- **After:** Fewer overlaps, clearer distinctions

---

## 📋 Updated Entity Types

### Added
- `SOCIAL_USER_NAME` - Generic social media username
- `SOCIAL_MEDIA_URL` - Generic social media URL
- `REPOSITORY` - Generic repository (not GitHub-specific)
- `REPOSITORY_URL` - Generic repository URL
- `CODE_SNIPPET` - Generic code snippet
- `ISSUE_ID` - Generic issue identifier
- `PULL_REQUEST_ID` - Generic pull request identifier
- `COMMIT_HASH` - Generic commit hash
- `BRANCH_NAME` - Generic branch name
- `VERSION_TAG` - Generic version tag
- `RELEASE_VERSION` - Generic release version

### Removed
- `GITHUB_USER`
- `GITHUB_ORGANIZATION`
- `INSTAGRAM_USERNAME`
- `FACEBOOK_USERNAME`
- `LINKEDIN_USERNAME`
- `TELEGRAM_USERNAME`
- `DISCORD_USERNAME`
- `SLACK_USERNAME`
- `WHATSAPP_USERNAME`
- `TWITTER_USERNAME`
- `TIKTOK_USERNAME`
- `YOUTUBE_USERNAME`
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
- `GITHUB_REPO`
- `GITHUB_REPO_URL`
- `GITHUB_GIST`
- `GITHUB_ISSUE`
- `GITHUB_PULL_REQUEST`
- `GITHUB_COMMIT`
- `GITHUB_BRANCH`
- `GITHUB_TAG`
- `GITHUB_RELEASE`

---

## 🎯 Next Steps

1. **Retrain Models**
   - Models will learn generalized patterns
   - Better generalization to new platforms
   - Reduced overfitting

2. **Test Generalization**
   - Test with new social platforms
   - Test with non-GitHub repositories
   - Verify improved accuracy

3. **Monitor Performance**
   - Check if generalization improves accuracy
   - Verify reduced false positives
   - Confirm better entity detection

---

## ✅ Summary

**Generalization Complete:**
- ✅ Social media usernames → `SOCIAL_USER_NAME`
- ✅ Social media URLs → `SOCIAL_MEDIA_URL`
- ✅ Removed product-centric entities (13,160 instances)
- ✅ Generalized product-specific entities (678 instances)
- ✅ Updated entity_types.txt (26 removed, 11 added)
- ✅ Reduced overlapping entities

**Status:** ✅ **READY FOR RETRAINING**

The training data is now generalized and should avoid overfitting to specific platforms.

