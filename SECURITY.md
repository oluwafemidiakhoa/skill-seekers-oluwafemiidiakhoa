# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of Skill Seekers seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Publicly Disclose

Please do not open a public GitHub issue for security vulnerabilities. This could put users at risk.

### 2. Email Us Privately

Send details to: **oluwafemidiakhoa@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information

### 3. What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 5 business days
- **Regular updates**: Every 7 days until resolved
- **Resolution**: We aim to patch critical vulnerabilities within 30 days

### 4. Disclosure Timeline

Once a fix is ready:
1. We'll release a patch
2. We'll publish a security advisory
3. We'll credit you (unless you prefer to remain anonymous)

## Security Considerations

### When Using Skill Seekers

**Web Scraping Security:**
- Only scrape documentation from trusted sources
- Be aware of rate limiting and ToS
- Use authentication tokens securely (environment variables)

**Configuration Files:**
- Don't commit API keys to Git
- Use `.env` files for secrets (add to `.gitignore`)
- Validate URLs before scraping

**Generated Skills:**
- Review generated content before uploading
- Don't include sensitive information in skills
- Be cautious with private repository scraping

**Dependencies:**
- Keep dependencies updated
- Run `safety check` regularly
- Monitor security advisories

### Code Security Practices

**Input Validation:**
- All URLs are validated before fetching
- Config files are validated against schema
- User input is sanitized

**Safe File Operations:**
- Files are written to designated output directories only
- No arbitrary file system access
- Path traversal prevention

**Network Security:**
- HTTPS enforced where possible
- Rate limiting to prevent abuse
- Timeout configurations for requests

**API Security:**
- API keys stored in environment variables
- Anthropic API communication over HTTPS
- No logging of sensitive data

## Known Security Considerations

### 1. Web Scraping Risks

Scraping untrusted websites could expose you to:
- Malicious content injection
- Large file downloads
- Server-side attacks (if scraping APIs)

**Mitigation**: Only scrape from trusted documentation sources.

### 2. Generated Content

AI-generated content could potentially:
- Include outdated or incorrect information
- Expose implementation details

**Mitigation**: Review generated skills before use.

### 3. GitHub Repository Scraping

Scraping repositories could expose:
- Sensitive information in code
- API keys in source files
- Private implementation details

**Mitigation**:
- Only scrape public repositories
- Review generated content
- Use `.gitignore` patterns to exclude sensitive files

### 4. PDF Processing

PDF files could contain:
- Malicious embedded scripts
- Large file size attacks

**Mitigation**:
- Only process trusted PDFs
- File size limits enforced
- Sandboxed processing

## Security Best Practices for Contributors

### Code Review

All code changes undergo security review:
- Input validation checks
- Authentication/authorization review
- Dependency vulnerability checks
- Static analysis (Bandit)

### Automated Security Checks

Our CI/CD pipeline includes:
- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner
- **Dependabot**: Automated dependency updates
- **CodeQL**: Code scanning (planned)

### Secure Development

Contributors should:
- Never commit secrets or API keys
- Use parameterized queries (if using databases)
- Validate all user input
- Handle errors securely (no sensitive info in logs)
- Keep dependencies updated

## Security Tools We Use

- **Bandit**: Static analysis for Python security issues
- **Safety**: Checks dependencies for known vulnerabilities
- **GitHub Dependabot**: Automated dependency updates
- **GitHub Secret Scanning**: Detects committed secrets
- **Ruff**: Linting with security rules enabled

## Security-Related Configuration

### Environment Variables

Secure ways to store credentials:

```bash
# .env file (add to .gitignore!)
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...

# Load in Python
from dotenv import load_dotenv
load_dotenv()
```

### API Key Management

```python
# Good ✅
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("API key not found")

# Bad ❌
api_key = "sk-ant-hardcoded-key"  # Never do this!
```

## Vulnerability Disclosure Policy

We follow coordinated disclosure:

1. **Report received**: We acknowledge and assess
2. **Validation**: We reproduce and confirm the issue
3. **Fix development**: We create and test a patch
4. **Release**: We publish the fix and advisory
5. **Credit**: We acknowledge the reporter (with permission)

## Bug Bounty

We currently do not have a formal bug bounty program. However, we deeply appreciate security researchers and will:
- Publicly acknowledge your contribution
- Give you credit in our security advisories
- Consider sponsorship/donations for significant findings

## Security Hall of Fame

Contributors who have helped improve our security:

*(None yet - be the first!)*

## Questions?

For security-related questions that are not vulnerabilities, you can:
- Open a GitHub Discussion
- Email: oluwafemidiakhoa@gmail.com

---

**Thank you for helping keep Skill Seekers and our users safe!** 🔒
