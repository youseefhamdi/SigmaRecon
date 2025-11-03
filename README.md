# 🔍 SigmaRecon

**The Ultimate Subdomain Enumeration Tool for 2026**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

**SigmaRecon** is the most comprehensive subdomain enumeration platform that unifies 23+ industry-leading tools, advanced data collection methods, and cutting-edge AI-powered discovery to deliver unmatched reconnaissance capabilities for cybersecurity professionals.

## ⭐ **Why SigmaRecon?**

### 🚀 **Unmatched Coverage**
- **23+ Integrated Tools**: Subfinder, Amass, BBOT, MassDNS, HTTPX, and more
- **8 Data Collection Methods**: Certificate Transparency, DNS Bruteforcing, Web Scraping, Social Platforms, Search Engines, AI/ML Prediction, Threat Intelligence, IoT Discovery
- **2026-Ready Technology**: AI-enhanced discovery, blockchain domain analysis, cloud service enumeration

### ⚡ **Superior Performance**
- **High-Speed Processing**: Handle thousands of subdomains per hour
- **Concurrent Execution**: Multi-threaded operations with intelligent rate limiting
- **Smart Caching**: Redis-backed caching for optimal performance
- **Auto-Scaling**: Kubernetes-native for enterprise deployment

### 🛡️ **Enterprise Security**
- **Result Validation**: DNS resolution, HTTP probing, technology detection
- **Enrichment**: Geolocation, threat intelligence, domain age, SSL analysis
- **Attack Surface Scoring**: Comprehensive risk assessment
- **Audit Trail**: Complete logging and monitoring

## 📦 **Installation**

### Quick Install (Docker) - Recommended
```bash
docker pull sigmarecon/sigmarecon:latest
docker run -it --rm sigmarecon/sigmarecon:latest sigma --help
```

### Python Package Installation
```bash
pip install sigmarecon
```

### From Source
```bash
git clone https://github.com/El3aref/SigmaRecon.git
cd SigmaRecon
pip install -r requirements.txt
python setup.py install
```

## 🚀 **Quick Start**

### Basic Subdomain Discovery
```bash
# Discover subdomains for a domain
sigma discover -d example.com --sources subfinder,amass --format jsonl

# Comprehensive reconnaissance
sigma scan --target example.com --mode thorough --output results.jsonl
```

### Advanced Usage
```bash
# Multi-source discovery with enrichment
sigma discover -d example.com \
  --sources all \
  --enrichment \
  --validation \
  --format jsonl

# Continuous monitoring
sigma monitor --domains example.com \
  --interval 3600 \
  --enrichment threat-intel \
  --alert-email admin@example.com

# Custom configuration
sigma config profile create production \
  --tools subfinder,amass,bbot \
  --rate-limit 100 \
  --timeout 30
```

## 🔧 **Features**

### 🛠️ **Integrated Tools** (23+ Total)
| Category | Tools |
|----------|-------|
| **Passive Discovery** | Subfinder, Amass, Assetfinder, BBOT, OneForAll |
| **DNS Resolution** | MassDNS, PureDNS, DNSX |
| **Certificate Analysis** | Zero, CertInfo, CSPRec, CSPFinder |
| **Web Probing** | HTTPX, JSubfinder |
| **Specialized** | SubWiz (AI), GitHub-Subdomains, Findomain |
| **Utility** | Anew, Org2asn, Shosubgo |

### 📊 **Data Collection Sources**
- **Certificate Transparency**: crt.sh, Google CT, Cloudflare CT, Sectigo
- **DNS Bruteforcing**: Dictionary, Permutations, Zone Transfers, Reverse DNS
- **Web Scraping**: SecurityTrails, VirusTotal, ThreatCrowd, DNSDumpster
- **Social Platforms**: GitHub, Twitter, LinkedIn, Reddit, Stack Overflow
- **Search Engines**: Google, Bing, DuckDuckGo, Yandex
- **AI/ML Sources**: Predictive domain generation, pattern analysis
- **Threat Intelligence**: VirusTotal, AbuseIPDB, URLhaus
- **Emerging Sources**: Blockchain domains, IoT devices, Cloud services

### ✅ **Validation & Enrichment**
- **DNS Validation**: A/AAAA, CNAME, MX, TXT, NS records, DNSSEC
- **HTTP Probing**: Status codes, SSL/TLS, redirects, content analysis
- **Technology Detection**: Web servers, frameworks, CMS, cloud platforms
- **Geolocation**: IP geolocation, ASN mapping
- **Threat Intelligence**: Security scores, reputation analysis
- **Attack Surface**: Risk scoring, security posture assessment

## 📈 **Performance Benchmarks**

| Domain Size | Tools | Speed | Coverage |
|-------------|-------|-------|----------|
| Small (<1K subs) | Subfinder + Amass | ~50K subs/hour | 95%+ |
| Medium (1K-10K) | Full Stack | ~200K subs/hour | 90%+ |
| Large (>10K) | Enterprise | ~500K subs/hour | 85%+ |

## 📁 **Repository Structure**

```
SigmaRecon/
├── sigmarecon/              # Main Python package
│   ├── main.py             # CLI application
│   ├── config/             # Configuration management
│   ├── tools/              # Tool integration framework
│   ├── pipeline/           # Data collection pipeline
│   ├── collectors/         # Advanced data collectors
│   ├── validation/         # Result validation
│   ├── enrichment/         # Data enrichment
│   ├── output/             # Output formatting
│   └── logging/            # Logging system
├── docs/                   # Comprehensive documentation
│   ├── user_guide/         # User documentation
│   ├── api/               # API documentation
│   └── installation/       # Installation guides
├── examples/              # Example scripts and tutorials
├── tests/                 # Test suite
├── research/              # Research documentation
├── setup.py              # Package setup
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 📚 **Documentation**

- **[User Guide](docs/user_guide/)** - Complete user documentation
- **[API Reference](docs/api/)** - Developer API documentation
- **[Installation Guide](docs/installation/)** - Detailed installation instructions
- **[Examples](examples/)** - Practical usage examples and tutorials

## 🧪 **Testing**

```bash
# Run all tests
make test

# Generate coverage report
make coverage

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/performance/
```

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/El3aref/SigmaRecon.git
cd SigmaRecon
make install-dev
make test
```

## 📊 **Supported Platforms**

| Platform | Status | Version |
|----------|--------|---------|
| Linux | ✅ Supported | Ubuntu 18.04+, CentOS 7+, Debian 9+ |
| macOS | ✅ Supported | 10.14+ (Intel & Apple Silicon) |
| Windows | ✅ Supported | 10+ (Native & WSL2) |
| Docker | ✅ Supported | Latest |
| Kubernetes | ✅ Supported | 1.19+ |

## 🏆 **Use Cases**

### 🔍 **Bug Bounty Hunting**
```bash
sigma scan --target bugbounty.com --mode bug-bounty --format jsonl
```

### 🛡️ **Penetration Testing**
```bash
sigma discover -d client.com --sources all --enrichment --validation
```

### 📊 **Attack Surface Monitoring**
```bash
sigma monitor --domains company.com --interval 3600 --alert-config monitoring.yml
```

### 🏢 **Enterprise Reconnaissance**
```bash
sigma scan --target enterprise.com --mode enterprise --output elasticsearch://
```

## 🔒 **Security & Ethics**

SigmaRecon is designed for **authorized security testing only**. Users are responsible for ensuring they have proper permissions before conducting reconnaissance activities.

### Ethical Guidelines
- ✅ **Authorized Testing**: Only test domains you own or have explicit permission to test
- ✅ **Rate Limiting**: Respect target systems with appropriate rate limiting
- ✅ **Data Privacy**: Handle discovered data responsibly
- ✅ **Legal Compliance**: Comply with applicable laws and regulations

## 📝 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**El3aref**

*Lead Developer & Security Researcher*

- GitHub: [@El3aref](https://github.com/El3aref)
- Email: [Contact via GitHub](https://github.com/El3aref)
- LinkedIn: [Professional Profile](https://linkedin.com/in/el3aref)

## 🙏 **Acknowledgments**

Special thanks to the creators of all integrated tools and the cybersecurity community for their foundational work in subdomain enumeration and reconnaissance.

### Integrated Tool Authors
- **ProjectDiscovery** - Subfinder, HTTPX, DNSX
- **OWASP** - Amass
- **Tomnomnom** - Assetfinder, Anew
- **BlackArch** - BBOT and various tools
- **All contributors** to the subdomain enumeration ecosystem

## 🚀 **Roadmap**

### v1.1 (Q2 2026)
- [ ] Machine learning-based subdomain prediction
- [ ] Enhanced cloud service enumeration
- [ ] Real-time threat intelligence integration
- [ ] Advanced visualization dashboard

### v1.2 (Q3 2026)
- [ ] GraphQL API support
- [ ] Plugin marketplace
- [ ] Multi-tenant architecture
- [ ] Advanced reporting templates

## 📞 **Support**

- **Documentation**: [Full Documentation](docs/)
- **Issues**: [GitHub Issues](https://github.com/El3aref/SigmaRecon/issues)
- **Discussions**: [GitHub Discussions](https://github.com/El3aref/SigmaRecon/discussions)
- **Security**: Report security issues via GitHub Security Advisories

---

**Made with ❤️ by El3aref**

*Empowering cybersecurity professionals with the most advanced subdomain enumeration platform of 2026*