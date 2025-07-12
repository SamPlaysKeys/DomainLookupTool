#!/usr/bin/env python3
"""
Domain Lookup Tool

This script provides functionality to check the availability of domain names
using WHOIS lookups. It validates domain syntax, tracks available domains,
and provides real-time feedback.
"""

import sys
import re
import time
import whois
from datetime import datetime

def validate_domain(domain):
    # Regular expression pattern for domain validation
    # Matches standard domain names with valid TLDs (2-63 characters for names, 2-10 for TLDs)
    pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,10}$'
    return bool(re.match(pattern, domain))

def check_domain_availability(domain):
    try:
        domain_info = whois.whois(domain)
        
        # 1. Explicit check for domain_name presence in WHOIS data
        if domain_info.domain_name is None:
            return True, f"Domain {domain} appears to be available (No domain record found)"
        
        # Format registration details for output
        registration_details = []
        
        # 2. Parse and check creation date (when the domain was first registered)
        creation_date = None
        if domain_info.creation_date:
            if isinstance(domain_info.creation_date, list):
                creation_date = domain_info.creation_date[0]
            else:
                creation_date = domain_info.creation_date
                
            if isinstance(creation_date, datetime):
                registration_details.append(f"Created: {creation_date.strftime('%Y-%m-%d')}")
        
        # 3. Improved expiration date parsing and comparison
        expiration_date = None
        if domain_info.expiration_date:
            if isinstance(domain_info.expiration_date, list):
                expiration_date = domain_info.expiration_date[0]
            else:
                expiration_date = domain_info.expiration_date
                
            if isinstance(expiration_date, datetime):
                registration_details.append(f"Expires: {expiration_date.strftime('%Y-%m-%d')}")
                
                # Check if domain has expired
                if expiration_date < datetime.now():
                    return True, f"Domain {domain} expired on {expiration_date.strftime('%Y-%m-%d')} and may be available for registration"
        
        # 4. Get and include registrar information
        registrar = "Unknown registrar"
        if domain_info.registrar:
            registrar = domain_info.registrar
            registration_details.append(f"Registrar: {registrar}")
        
        # 5. Check for nameservers as another indication of active registration
        if domain_info.name_servers:
            ns_count = len(domain_info.name_servers) if isinstance(domain_info.name_servers, list) else 1
            registration_details.append(f"Nameservers: {ns_count} configured")
        
        # 6. Check registration status if available
        if hasattr(domain_info, 'status') and domain_info.status:
            if isinstance(domain_info.status, list):
                statuses = ", ".join(domain_info.status[:2])  # Limit to first 2 statuses to avoid long messages
                if len(domain_info.status) > 2:
                    statuses += f" and {len(domain_info.status)-2} more"
            else:
                statuses = domain_info.status
            registration_details.append(f"Status: {statuses}")
        
        # 7. Build detailed registration message
        if registration_details:
            details = " | ".join(registration_details)
            return False, f"Domain {domain} is registered ({details})"
        else:
            # If we have domain_name but no other details, still mark as registered
            return False, f"Domain {domain} appears to be registered, but limited details are available"
        
    except whois.parser.PywhoisError as e:
        error_msg = str(e)
        
        # 8. Enhanced error message checking for available domains
        if any(phrase in error_msg.lower() for phrase in [
            "no match for", 
            "no entries found", 
            "not found", 
            "no data found",
            "no match",
            "domain not found",
            "domain available"
        ]):
            return True, f"Domain {domain} appears to be available (WHOIS response: {error_msg.split('.')[0]})"
        
        # 9. Check for registration privacy or protected domains
        if any(phrase in error_msg.lower() for phrase in [
            "redacted for privacy", 
            "registration private", 
            "data protected"
        ]):
            return False, f"Domain {domain} is registered with privacy protection"
        
        # 10. Enhanced error handling with more descriptive messages
        return False, f"Error checking {domain}: {error_msg}"
        
    except Exception as e:
        # 11. More detailed error classification
        error_type = type(e).__name__
        return False, f"Error checking {domain}: {error_type} - {str(e)}"

def print_colored(text, color_code):
    """
    Print colored text to the console.
    
    Args:
        text (str): Text to print
        color_code (str): ANSI color code
    """
    print(f"\033[{color_code}m{text}\033[0m")

def main():
    """
    Main function to run the domain lookup tool.
    """
    print_colored("\n=== Domain Availability Checker ===", "1;36")
    print("Enter domain names to check (type 'quit' or 'exit' to finish)")
    print("Press Ctrl+C to exit at any time\n")
    
    available_domains = []
    checked_domains = 0
    
    try:
        while True:
            # Get domain from user
            domain = input("\nEnter domain to check (e.g., example.com): ").strip().lower()
            
            # Check for exit command
            if domain.lower() in ('quit', 'exit', 'q'):
                break
                
            # Skip empty input
            if not domain:
                print("Please enter a domain name")
                continue
                
            # Validate domain format
            if not validate_domain(domain):
                print_colored(f"Invalid domain format: {domain}", "1;31")
                print("Domain should match pattern: example.com, sub.example.net, etc.")
                continue
                
            # Perform the check with visual feedback
            print_colored(f"Checking {domain}...", "1;33")
            checked_domains += 1
            
            # Add small delay to prevent abuse of WHOIS servers
            time.sleep(0.5)
            
            # Check availability
            is_available, message = check_domain_availability(domain)
            
            if is_available:
                print_colored(f"✓ {message}", "1;32")
                available_domains.append(domain)
            else:
                print_colored(f"✗ {message}", "1;31")
                
    except KeyboardInterrupt:
        print_colored("\n\nSearch interrupted by user.", "1;33")
    
    # Print final report
    print_colored("\n=== Domain Lookup Summary ===", "1;36")
    print(f"Domains checked: {checked_domains}")
    print(f"Available domains found: {len(available_domains)}")
    
    if available_domains:
        print_colored("\nAvailable Domains:", "1;32")
        for domain in available_domains:
            print(f"  - {domain}")
    
    print_colored("\nThank you for using the Domain Availability Checker!", "1;36")

if __name__ == "__main__":
    main()

