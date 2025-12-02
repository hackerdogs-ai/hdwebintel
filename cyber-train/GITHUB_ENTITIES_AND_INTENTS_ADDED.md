# GitHub Entities and Intents Added - Summary

**Date:** December 2, 2025  
**Total Entity Examples Added:** 1,950  
**Total Intent Examples Added:** 1,020

---

## 📊 GitHub Entity Types Added

### **Repository & URLs:**
- **GITHUB_REPO**: 300 examples (repository names like `user/repo`)
- **GITHUB_REPO_URL**: 300 examples (full URLs like `https://github.com/user/repo`)

### **Users & Organizations:**
- **GITHUB_USER**: 200 examples (usernames like `@username` or `username`)
- **GITHUB_ORGANIZATION**: 150 examples (organization names)

### **Code & Content:**
- **GITHUB_GIST**: 150 examples (gist URLs)
- **GITHUB_ISSUE**: 200 examples (issue references like `#123`)
- **GITHUB_COMMIT**: 200 examples (commit hashes)
- **GITHUB_BRANCH**: 150 examples (branch names)
- **GITHUB_TAG**: 150 examples (version tags like `v1.0.0`)
- **GITHUB_RELEASE**: 150 examples (release names)

**Total: 1,950 entity examples**

---

## 📁 Entity Distribution by File

### **GITHUB_REPO: 300 examples** (6 files)
- `cybint_entities.jsonl` - 50 examples
- `threat_intel_entities.jsonl` - 50 examples
- `incident_response_entities.jsonl` - 50 examples
- `application_security_entities.jsonl` - 50 examples
- `vulnerability_mgmt_entities.jsonl` - 50 examples
- `ai_security_entities.jsonl` - 50 examples

### **GITHUB_REPO_URL: 300 examples** (5 files)
- `cybint_entities.jsonl` - 60 examples
- `threat_intel_entities.jsonl` - 60 examples
- `incident_response_entities.jsonl` - 60 examples
- `application_security_entities.jsonl` - 60 examples
- `vulnerability_mgmt_entities.jsonl` - 60 examples

### **GITHUB_USER: 200 examples** (5 files)
- `cybint_entities.jsonl` - 40 examples
- `threat_intel_entities.jsonl` - 40 examples
- `socmint_entities.jsonl` - 40 examples
- `humint_entities.jsonl` - 40 examples
- `incident_response_entities.jsonl` - 40 examples

### **GITHUB_ORGANIZATION: 150 examples** (4 files)
- `cybint_entities.jsonl` - 38 examples
- `threat_intel_entities.jsonl` - 38 examples
- `vulnerability_mgmt_entities.jsonl` - 37 examples
- `application_security_entities.jsonl` - 37 examples

### **GITHUB_GIST: 150 examples** (3 files)
- `cybint_entities.jsonl` - 50 examples
- `threat_intel_entities.jsonl` - 50 examples
- `incident_response_entities.jsonl` - 50 examples

### **GITHUB_ISSUE: 200 examples** (3 files)
- `vulnerability_mgmt_entities.jsonl` - 67 examples
- `application_security_entities.jsonl` - 67 examples
- `incident_response_entities.jsonl` - 66 examples

### **GITHUB_COMMIT: 200 examples** (3 files)
- `application_security_entities.jsonl` - 67 examples
- `vulnerability_mgmt_entities.jsonl` - 67 examples
- `incident_response_entities.jsonl` - 66 examples

### **GITHUB_BRANCH: 150 examples** (2 files)
- `application_security_entities.jsonl` - 75 examples
- `vulnerability_mgmt_entities.jsonl` - 75 examples

### **GITHUB_TAG: 150 examples** (2 files)
- `vulnerability_mgmt_entities.jsonl` - 75 examples
- `application_security_entities.jsonl` - 75 examples

### **GITHUB_RELEASE: 150 examples** (2 files)
- `vulnerability_mgmt_entities.jsonl` - 75 examples
- `application_security_entities.jsonl` - 75 examples

---

## 🎯 GitHub Intent Types Added

### **Repository Analysis:**
- **ANALYZE_GITHUB_REPO**: 80 examples
- **SCAN_GITHUB_REPO**: 60 examples
- **MONITOR_GITHUB_REPO**: 60 examples
- **CLONE_GITHUB_REPO**: 60 examples

### **User & Organization:**
- **INVESTIGATE_GITHUB_USER**: 80 examples
- **ANALYZE_GITHUB_ORGANIZATION**: 40 examples

### **Code Analysis:**
- **REVIEW_GITHUB_CODE**: 40 examples
- **TRACK_GITHUB_COMMITS**: 60 examples
- **ANALYZE_GITHUB_COMMITS**: 40 examples
- **REVIEW_GITHUB_PULL_REQUESTS**: 40 examples

### **Security & Threats:**
- **DETECT_GITHUB_VULNERABILITIES**: 60 examples
- **DETECT_GITHUB_EXPLOITS**: 60 examples
- **ANALYZE_GITHUB_ISSUES**: 40 examples

### **Monitoring & Intelligence:**
- **MONITOR_GITHUB_ACTIVITY**: 60 examples
- **EXTRACT_GITHUB_INTELLIGENCE**: 40 examples
- **SEARCH_GITHUB_REPOS**: 40 examples

### **Version Control:**
- **TRACK_GITHUB_RELEASES**: 40 examples
- **MONITOR_GITHUB_BRANCHES**: 40 examples
- **TRACK_GITHUB_TAGS**: 40 examples

### **Content Analysis:**
- **ANALYZE_GITHUB_GISTS**: 40 examples

**Total: 1,020 intent examples**

---

## 📋 Entity Format Examples

### **GITHUB_REPO**
- Format: `username/repository-name`
- Examples: `octocat/awesome-project`, `microsoft/vscode`, `torvalds/linux`

### **GITHUB_REPO_URL**
- Format: `https://github.com/username/repo` or `https://github.com/username/repo/path`
- Examples: 
  - `https://github.com/octocat/awesome-project`
  - `https://github.com/microsoft/vscode/tree/main`
  - `https://github.com/torvalds/linux/blob/main/README.md`

### **GITHUB_USER**
- Format: `@username` or `username`
- Examples: `@octocat`, `torvalds`, `gaearon`

### **GITHUB_ORGANIZATION**
- Format: Organization name
- Examples: `microsoft`, `google`, `facebook`, `github`

### **GITHUB_GIST**
- Format: `https://gist.github.com/username/gist-id`
- Examples: `https://gist.github.com/octocat/abc123def456...`

### **GITHUB_ISSUE**
- Format: `#issue-number`
- Examples: `#123`, `#4567`, `#9999`

### **GITHUB_COMMIT**
- Format: Commit hash (7-40 hex characters)
- Examples: `abc1234`, `def5678`, `a1b2c3d4e5f6...`

### **GITHUB_BRANCH**
- Format: Branch name
- Examples: `main`, `master`, `develop`, `feature/security`, `hotfix/vuln`

### **GITHUB_TAG**
- Format: Version tag
- Examples: `v1.0.0`, `v2.1.3`, `1.0.0`, `v1.0.0-beta`, `v2.0.0-rc1`

### **GITHUB_RELEASE**
- Format: Release name
- Examples: `v1.0.0`, `Security Update`, `Critical Patch`, `v2.1.3`

---

## 🎯 Intent Examples

### **ANALYZE_GITHUB_REPO**
- "Analyze the GitHub repository for security vulnerabilities"
- "Review the repository code for potential threats"
- "Examine the GitHub repo for malicious code"

### **SCAN_GITHUB_REPO**
- "Scan the GitHub repository for security vulnerabilities"
- "Perform security scan on the repository"
- "Run vulnerability scan on GitHub repo"

### **MONITOR_GITHUB_REPO**
- "Monitor the GitHub repository for changes"
- "Track repository activity and updates"
- "Watch for new commits in the repository"

### **INVESTIGATE_GITHUB_USER**
- "Investigate the GitHub user's repositories"
- "Analyze user's GitHub activity"
- "Review user's GitHub profile"

### **DETECT_GITHUB_VULNERABILITIES**
- "Detect vulnerabilities in GitHub repository"
- "Find security issues in repo"
- "Identify vulnerabilities in code"

### **EXTRACT_GITHUB_INTELLIGENCE**
- "Extract threat intelligence from GitHub"
- "Gather OSINT from GitHub repositories"
- "Collect intelligence from GitHub"

---

## ✅ Files Updated

### **Entity Types:**
- `entity_types.txt` - Added 11 new GitHub entity types

### **Intent Types:**
- `intent_types.txt` - Added 20 new GitHub intent types

### **Entity Training Files:**
- Multiple cybersecurity and OSINT pillar files updated

### **Intent Training Files:**
- Multiple cybersecurity and OSINT pillar files updated

---

## 📊 Total GitHub Coverage

**Entity Examples:** 1,950  
**Intent Examples:** 1,020  
**Entity Types:** 11  
**Intent Types:** 20

---

## 🎯 Use Cases Covered

### **Cybersecurity:**
- ✅ Repository vulnerability scanning
- ✅ Code security analysis
- ✅ Threat actor investigation
- ✅ Exploit detection
- ✅ Security issue tracking

### **OSINT:**
- ✅ Threat intelligence extraction
- ✅ User profile investigation
- ✅ Organization analysis
- ✅ Repository monitoring
- ✅ Activity tracking

### **Application Security:**
- ✅ Code review
- ✅ Commit analysis
- ✅ Pull request review
- ✅ Branch monitoring
- ✅ Release tracking

---

**All GitHub entities and intents have been successfully added with accurate boundaries and realistic examples!** ✅

