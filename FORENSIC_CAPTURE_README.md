# Forensic Capture Tool

Advanced web data capture and analysis tool for forensic investigations, built with Python and Playwright.

## Overview

This forensic capture tool performs comprehensive web data collection with forensic-grade integrity controls including:
- Full HTML content capture and archival
- Full-page screenshot capture
- Network traffic logging
- Cryptographic hash verification (MD5, SHA-256)
- Structured metadata collection
- Session-based forensic reporting

## Features

- **Multi-label Processing**: Process multiple investigation labels simultaneously
- **Comprehensive Data Collection**: 
  - HTML source code capture
  - Full-page screenshots
  - Network request logging
  - Page metadata extraction
- **Forensic Integrity**: 
  - Cryptographic hashing of captured content
  - Chain of custody tracking
  - Timestamp verification
- **Configurable Thresholds**: Filter captures by minimum content size
- **Structured Output**: Organized file system with clear naming conventions
- **Session Management**: Complete session tracking and reporting

## Installation

### Prerequisites

Ensure you have Python 3.7+ installed on your system.

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browser

```bash
python -m playwright install chromium
```

### 3. Install System Dependencies

On Ubuntu/Debian:
```bash
sudo apt-get install libnss3 libnspr4 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxcb1 libxkbcommon0 libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2
```

On Amazon Linux/RHEL/CentOS:
```bash
sudo dnf install -y nss nspr dbus-libs atk at-spi2-atk cups-libs libdrm libxcb libxkbcommon at-spi2-core libX11 libXcomposite libXdamage libXext libXfixes libXrandr mesa-libgbm pango cairo alsa-lib
```

## Usage

### Basic Command

```bash
python capture.py --labels RHO-TECH PIPETECH DIKA SWAN --out ./output --min-bytes 1000000
```

### Command Line Options

- `--labels`: Space-separated list of investigation labels (required)
- `--out`: Output directory for captured data (required)  
- `--min-bytes`: Minimum bytes threshold for captures (default: 1000000)
- `--verbose`, `-v`: Enable verbose output for debugging

### Examples

#### Basic capture with multiple labels:
```bash
python capture.py --labels TARGET1 TARGET2 --out ./investigation_2024 --min-bytes 500000
```

#### Verbose capture with lower threshold:
```bash
python capture.py --labels COMPANY-ALPHA --out ./captures --min-bytes 1000 --verbose
```

## Output Structure

The tool creates an organized directory structure:

```
output/
├── forensic_report_[session-id].txt     # Main forensic report
├── html_dumps/                          # HTML source captures
│   ├── [capture-id]_[label].html
│   └── ...
├── screenshots/                         # Full-page screenshots
│   ├── [capture-id]_[label].png
│   └── ...
├── network_logs/                        # Network traffic logs
│   ├── [capture-id]_[label]_network.json
│   └── ...
└── metadata/                            # Session metadata
    └── session_[session-id].json
```

## Key Files

### Forensic Report
Primary forensic analysis report containing:
- Session details and timestamps
- Capture summaries with integrity hashes
- File locations and metadata
- Investigation timeline

### Session Metadata
JSON file with complete session information:
- All capture details
- Cryptographic hashes
- File paths and sizes
- Network activity summaries

### HTML Dumps
Complete HTML source code from captured pages with original formatting preserved.

### Screenshots
Full-page PNG screenshots showing visual state of captured pages.

### Network Logs
JSON files containing network request information during capture sessions.

## Forensic Features

### Data Integrity
- **MD5 Hashing**: Quick integrity verification
- **SHA-256 Hashing**: Cryptographic integrity validation
- **Timestamp Tracking**: Precise capture timing
- **Chain of Custody**: Complete session tracking

### Evidence Organization
- **Unique IDs**: Each capture has unique identifier
- **Structured Naming**: Consistent file naming convention
- **Metadata Preservation**: Complete capture context
- **Session Tracking**: Full investigation session records

## Configuration

### Target URL Configuration
Currently configured with test endpoints. For real forensic investigations, modify the `target_urls` list in the `search_and_capture` method:

```python
target_urls = [
    f"https://target-site.com/search?q={label}",
    f"https://backup-source.com/{label}",
    # Add your target URLs here
]
```

### Browser Settings
The tool uses forensic-grade browser settings optimized for evidence collection:
- Headless operation
- Disabled caching
- Single-process mode
- Enhanced security settings

## Security Considerations

1. **Network Isolation**: Run in isolated network environment when possible
2. **Data Encryption**: Consider encrypting output directory for sensitive investigations
3. **Access Controls**: Implement proper file system permissions
4. **Chain of Custody**: Document all access to captured data
5. **Secure Deletion**: Use secure deletion methods when disposing of data

## Troubleshooting

### Common Issues

1. **Browser Dependencies**: Ensure all system dependencies are installed
2. **Network Timeouts**: Adjust timeout settings for slow connections
3. **Memory Usage**: Monitor memory usage for large capture sessions
4. **Disk Space**: Ensure adequate disk space for capture output

### Debug Mode
Use `--verbose` flag for detailed logging:
```bash
python capture.py --labels TARGET --out ./debug --verbose
```

## Legal Considerations

- Ensure proper authorization before capturing data
- Comply with applicable laws and regulations
- Document investigation scope and authorization
- Maintain proper chain of custody procedures
- Consider privacy implications of captured data

## Technical Requirements

- Python 3.7+
- Playwright browser automation library
- Chrome/Chromium browser engine
- Sufficient disk space for captures
- Network connectivity to target sites

## Version History

- v1.0: Initial forensic capture implementation
- Features: Multi-label processing, comprehensive data collection, forensic integrity controls

## Contributing

This tool is designed for forensic investigations. Contributions should maintain evidence integrity standards and follow forensic best practices.

## License

This tool is provided for legitimate forensic investigation purposes. Users are responsible for compliance with applicable laws and regulations.