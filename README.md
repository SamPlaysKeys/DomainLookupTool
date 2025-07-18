# Domain Lookup Tool

## Project Description
The Domain Lookup Tool is a Python-based interactive utility designed to check the availability of domain names. It allows users to quickly verify if a domain is already registered or available for purchase, making it a valuable resource for website creators, marketers, and domain investors. The tool provides real-time feedback on domain status and generates a summary report of available domains upon completion.

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Installing Dependencies
To install the required dependencies, run the following command:

```bash
pip install python-whois requests
```

You may want to use a virtual environment for a cleaner installation:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install python-whois requests
```

## Installation from source
```bash
git clone https://github.com/SamPlaysKeys/DomainLookupTool
cd DomainLookup
pip install .
```

## Usage
```bash
domain-lookup           # interactive checker
python -m domain_lookup # alternative invocation
```

## Usage Instructions

1. Run the script using Python:
   ```bash
   python domain_lookup.py
   ```
1a. If installed with pip, then run the script with "domain-lookup"

2. When prompted, enter a domain name to check its availability (e.g., "example.com").

3. The script will validate the domain format and perform a WHOIS lookup, displaying the result.

4. Continue entering domains as needed. The tool will keep track of available domains.

5. To exit the program, press Ctrl+C or type "quit", "exit", or "q" when prompted for a domain name.
   Upon exit, the tool will display a summary of all available domains found during your session.

## How Domain Availability is Determined

The tool uses the `python-whois` library to query domain registrar databases. A domain is considered available when:

1. The WHOIS query returns no registered information
2. No "creation_date" is found in the WHOIS response
3. No registrar information is available

It's important to note that this method provides a good indication of availability but isn't 100% guaranteed. For absolute certainty, you should verify through an official domain registrar.

## Features and Functionality

- **Interactive Interface**: Simple command-line interface for checking multiple domains
- **Domain Validation**: Ensures input follows valid domain name format
- **Real-time Feedback**: Immediate results after each domain check
- **Available Domains Tracking**: Maintains a list of domains found to be available
- **Comprehensive Reporting**: Produces a summary of available domains upon exit
- **Robust Error Handling**: Gracefully handles network issues, timeouts, and invalid inputs

## Error Handling and Exit Mechanisms

The tool implements several error handling mechanisms:

- **Input Validation**: Checks domain format before attempting lookups
- **Exception Handling**: Captures and reports errors during WHOIS queries
- **Timeout Management**: Prevents hanging on slow responses
- **Graceful Exit**: Supports clean termination through keyboard interrupts (Ctrl+C) or exit commands
- **Exit Reporting**: Displays summary information upon program termination

When the program exits (either through user command or error), it will display a complete list of all available domains found during the session, allowing you to easily reference them later.

## Troubleshooting

If you encounter issues:
- Ensure you have a working internet connection
- Verify that python-whois is properly installed
- Check if your network allows WHOIS queries (some networks may block them)
- For persistent problems, try updating the python-whois library: `pip install --upgrade python-whois`

