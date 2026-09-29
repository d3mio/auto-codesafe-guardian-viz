# CodeSafe Guardian: Secret & Dependency Vulnerability Visualizer GUI

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Generated](https://img.shields.io/badge/AI%20Generated-Yes-brightgreen?style=for-the-badge&logo=openai)](https://openai.com/)

---

## 🛡️ Architecture Overview & Problem Statement

In today's complex software supply chain, hardcoded secrets (API keys, credentials, tokens) and vulnerable third-party dependencies represent critical attack vectors. Traditional security tools often provide fragmented views or generate overwhelming static reports, making it challenging for development and security teams to prioritize, contextualize, and remediate these risks efficiently. Manual auditing is resource-intensive and prone to human error, leading to overlooked vulnerabilities and potential breaches.

**CodeSafe Guardian** addresses this by providing an elite, enterprise-grade solution that consolidates secret and dependency vulnerability scanning within an intuitive, interactive Graphical User Interface (GUI). Built with a modular Python backend leveraging battle-tested security scanning libraries and a responsive CustomTkinter frontend, it offers a visual command center for supply chain security.

**Architectural Highlights:**
*   **Frontend (GUI):** Developed with CustomTkinter, ensuring a responsive, modern dark-mode interface for superior user experience across different operating systems.
*   **Scanning Engine (Python Core):** Leverages a pluggable architecture to integrate multiple secret detection algorithms (e.g., regex, entropy, keyword matching) and dependency analysis tools (e.g., CVE databases, package manifest parsers).
*   **Data Processing & Visualization:** Processes raw scan data into structured formats, enabling real-time filtering, sorting, and dynamic visualization through interactive tables, graphical dependency maps, and precise code context diff views.
*   **Code Context Integration:** Interfaces with underlying file systems and (optionally) Git repositories to fetch code snippets, commit information, and historical diffs, providing crucial context for remediation.

This integrated approach empowers developers and security engineers to quickly identify, understand, and mitigate supply chain risks, significantly enhancing the security posture of their applications.

---

## ✨ Features

**CodeSafe Guardian** is engineered with a suite of robust features designed for comprehensive software supply chain security analysis:

*   **Dual-Layer Vulnerability Scanning:** Simultaneously scans codebases for both hardcoded secrets (e.g., API keys, passwords, access tokens) using advanced detection algorithms, and identifies vulnerable third-party dependencies by cross-referencing against comprehensive CVE databases.
*   **Interactive Risk Visualization:** Presents scan results in highly interactive tables with advanced filtering, sorting, and search capabilities. Visualize dependency trees and their associated vulnerabilities through intuitive graphical maps, highlighting critical paths and high-risk components.
*   **Code Context & Diff Views:** Pinpoints the exact location of identified secrets or vulnerable dependency declarations within the codebase. Provides integrated code context snippets and, where applicable, a diff view against the previous version or a clean state to understand when and how the vulnerability was introduced.
*   **Dynamic Remediation Guidance:** Offers actionable insights and contextual information for each identified vulnerability, aiding developers in understanding the nature of the risk and guiding them towards effective remediation strategies, directly within the GUI.
*   **Configurable Scan Policies:** Allows users to define custom scan parameters, including file type inclusions/exclusions, directory ignore patterns, secret whitelists, and vulnerability severity thresholds, enabling tailored security assessments for diverse project requirements.
*   **Exportable Security Reports:** Generate detailed, enterprise-ready reports in various formats (e.g., CSV, JSON) summarizing scan findings, critical vulnerabilities, and remediation progress, facilitating compliance auditing and cross-team communication.

---

## 🚀 Quick Start

Get CodeSafe Guardian up and running on your system in minutes.

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/).
*   **Git**: Required to clone the repository. Download from [git-scm.com](https://git-scm.com/downloads).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/<your-username>/codesafe-guardian.git
    cd codesafe-guardian
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install project dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  **Ensure your virtual environment is active.**
2.  **Run the GUI application:**
    ```bash
    python gui_app.py
    ```
    This will launch the CodeSafe Guardian application window, ready for you to initiate a scan.

---

## 📺 Example Telemetry Output

Upon successful launch, the console will display foundational telemetry, confirming the GUI initialization and operational status:

```
Launched visual GUI application window [CustomTkinter] with dark mode interface, interactive scan functionality, and vulnerability visualization
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.