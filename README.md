
# DNS-Flooding

A Python-based experimental project for exploring DNS packet construction, asynchronous UDP networking, query strategies, and runtime statistics.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> [!WARNING]
> **For educational and authorized testing only.** High-volume DNS traffic can disrupt network services. Only use this project in an isolated lab or against systems you own or have explicit permission to test. Never use it to attack public DNS resolvers or third-party infrastructure.

## Overview

DNS-Flooding is an experimental Python project that explores DNS packet construction and asynchronous UDP communication.

It demonstrates different DNS query strategies, concurrent network operations, basic strategy weighting, logging, and runtime statistics.

## Features

- **DNS Packet Construction** - Builds DNS query packets using Python.
- **Multiple Query Strategies** - Includes randomized subdomain, EDNS-related, `ANY`, and `TXT` query construction.
- **Asynchronous Networking** - Uses Python's `asyncio` framework and UDP datagrams.
- **Strategy Weighting** - Uses a basic heuristic to adjust strategy weights.
- **Logging** - Records operation details and errors.
- **Runtime Statistics** - Reports execution statistics and strategy weights.
- **Configurable Parameters** - Supports target and execution configuration in the script.

## Requirements

- Python 3.10 or newer recommended
- Git
- A terminal or command-line environment
- An authorized DNS server for network testing

The project uses Python standard-library modules. No third-party package installation is expected for the current script.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mireli5656/Dns-Flooding.git
```

### 2. Navigate to the Project Directory

```bash
cd Dns-Flooding
```

### 3. Check Python

On Linux, macOS, or Termux:

```bash
python3 --version
```

On Windows:

```powershell
python --version
```

## Usage

### 1. Review the Configuration

Open `Dnsflooding.py` in a text editor and review its configuration before execution.

Only configure destinations you own or are explicitly authorized to test. Use conservative settings in a controlled environment.

### 2. Run the Script

On Linux, macOS, or Termux:

```bash
python3 Dnsflooding.py
```

On Windows:

```powershell
python Dnsflooding.py
```

### 3. Review the Output

Follow the terminal output for execution information and reported statistics.

If generated, inspect the log file:

```text
ai_dns_operations.log
```

> [!NOTE]
> Running the script does not guarantee that the destination DNS server received, processed, or answered the queries. Review the code and output to understand what the reported statistics measure.

## Project Structure

```text
Dns-Flooding/
├── Dnsflooding.py
├── README.md
└── LICENSE
```

## Logging and Statistics

The script may record operational information in `ai_dns_operations.log`, including timestamps, strategy details, packet sizes, and errors.

Successful UDP packet dispatch does not necessarily indicate successful DNS resolution. DNS responses must be validated separately to measure actual resolution success and latency.

## Limitations

- Strategy weighting is a basic heuristic, not a trained AI model.
- DNS responses are not necessarily validated.
- Comprehensive DNS response-latency measurements are not provided.
- EDNS-related packet construction requires independent protocol validation.
- High concurrency can consume resources and affect network services.
- Results from one environment do not establish general DNS server performance or reliability.

## Responsible Use

- Obtain permission before testing any DNS server.
- Prefer isolated test environments.
- Apply strict traffic and runtime limits.
- Monitor resource usage during testing.
- Stop immediately if unexpected service degradation occurs.
- Never use this project to disrupt services or overload third-party infrastructure.

The author does not encourage unauthorized activity or malicious use of this software.

## Contributing

Contributions that improve documentation, code quality, error handling, DNS protocol correctness, and safe testing practices are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your changes in an authorized environment.
5. Submit a pull request with a clear description.

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

**Mireli5656**

- GitHub: [@Mireli5656](https://github.com/Mireli5656)
- Repository: [DNS-Flooding](https://github.com/Mireli5656/Dns-Flooding)

---

If you find this project useful for learning about DNS protocols and Python networking, consider giving the repository a star.
