import ssl
import socket
import networkx as nx
from bs4 import BeautifulSoup as BS
import requests
from urllib.parse import urlparse
import re
import whois


# if test failed (is phishing) - True

def check_ssl_certificate(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                # Certificate validation
                cert = sslsock.getpeercert()
                if cert:
                    return False
                else:
                    return True
    except Exception as e:
        # print("An error occurred:", str(e))
        return True

    # def certificates_results(result):
    #     if result:
    #         print("SSL certificate is valid.")
    #     else:
    #         print("SSL certificate is not valid or an error occurred.")


def page_ranking(url):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add a single node representing the given URL
    graph.add_node(url)

    try:
        response = requests.get(url)
        soup = BS(response.text, 'html.parser')

        links = soup.find_all('a', href=True)
        # print(len(links))

        for link in links:
            href = link['href']
            # Ignore anchor links and other non-HTTP links
            if href.startswith('#') or not href.startswith('http'):
                continue

            graph.add_edge(url, href)

    except requests.exceptions.RequestException:
        print("Error: Failed to fetch the URL or perform web scraping.")

    # Run the PageRank algorithm on the graph
    pagerank = nx.pagerank(graph)
    #print(pagerank)

    # Get the PageRank value for the given URL
    ranking = round(pagerank[url], 2)
    # ranking = sum((list(pagerank.values())))
    print(ranking)
    # return ranking
    if ranking == 1.00:
        return True
    else:
        return False


def ip_in_url(url):
    # Extract the domain name from the URL
    domain = urlparse(url).netloc

    # Use regular expressions to check if the domain name is an IP address
    result = bool(re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain))
    return result


def url_registration_validity(url):
    """
    Check the registration status of the URL using Google's WHOIS API.
    Returns True if the URL is valid/registered, False otherwise.
    """
    # Use the pythonwhois library to fetch WHOIS information for the domain
    domain = urlparse(url).netloc
    print(domain)
    whois_info = whois.whois(domain)
    #name_servers = list(whois_info.name_servers)
    #print(name_servers)

    # print(f'Info Extracted - {whois_info.name} and  {whois_info.registrar} ...')
    # print(f'Info Extracted - {whois_info.__dict__}')
    # Extract the registration status from the WHOIS info
    # registration_status = whois_info.get('status', [])

    # Check if the registration status includes 'registered' or 'active'
    # is_valid = any(status.lower() == 'registered' or status.lower() == 'active' for status in registration_status)
   # return is_valid


def active_duration(url):
    pass


def length_of_url(url):
    pass


def at_character(url):
    pass


def is_redirect(url):
    pass


def dashes_in_domain_name(url):
    pass


def length_of_domain_name(url):
    pass


def no_of_subdomains(url):
    pass


def main():
    tests_list = {"check_ssl_certificate": 10,
                  "page_ranking": 5,
                  "ip_in_url": 5,
                  "url_registration_validity": 25,
                  "length_of_url": 10,
                  "at_character": 5,
                  "is_redirect": 10,
                  "dashes_in_domain_name": 5,
                  "length_of_domain_name": 10,
                  "no_of_subdomains": 15}

    summation_of_test_results = 0

    print("\n\n\n\n\nWelcome to ScamShield\'s \"Fishing?\"")
    url = input("Enter a website URL: ")
    print("\nStarting Tests - \n")

    for i in range(len(tests_list)):
        print(f'Test {(i+1)}: {list(tests_list.keys())[i]}')

        function = globals().get(list(tests_list.keys())[i])

        result = function(url)
        summation_of_test_results += (lambda x: 1 if x else 0)(result) * \
            (list(tests_list.values())[i])

        print("Result:", (lambda x: "Failed" if x else "Passed")(result))
        print(f'\n(Status: {int((i+1)*100/len(tests_list))}% Completed)\n\n')

    print(
        f"The probability that the link you have provided is malicious is {summation_of_test_results}%")


if __name__ == "__main__":
    main()


# http://trk.zingtoco.live/campaigns/nr8947da7fcaa/track-url/ky0812sfe4bb4/dfcdd846fa5681674ebb9bf63ab662a333e928b1

# http://tas4.benkartz.in/tracking/track-url/Q09NUD01JkNPTVBVSUQ9NWUzYTYyZTc1YzUyYSZDVVNUPTUmQ0FNUD04MDE4NCZMSVNUPTE3MzYmU1VCUz0xNzY2Mzg5ODg1NTc3NDYxNzYxJk1BSUw9MTBhcnVzaGkucmFpQGdtYWlsLmNvbSZTSUQ9MTY4NTA3NzI2MiZET009c2hvcGF0YmVzdC5jb20mUlVSTD1odHRwOi8vcDFlLmluL3QvNTE3OGRlZDdlYTUxNjI0MTA4NDdlZjcwMDRjNzNjNTMmVVJJRD00OTgzMDUmQ0FUPTYzJkNBVE49QnVzaW5lc3MgTG9hbg


# {'name': 'stackoverflow.com', 'tld': 'com', 'registrar': 'CSC Corporate Domains, Inc.', 'registrant_country': 'US',      'creation_date': datetime.datetime(2003, 12, 26, 19, 18, 7), 'expiration_date': datetime.datetime(2024, 2, 2, 11, 59, 59), 'last_updated': datetime.datetime(2022, 8, 17, 4, 32, 10), 'status': 'clientTransferProhibited https://icann.org/epp#clientTransferProhibited', 'statuses': ['clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited', 'clientTransferProhibited https://icann.org/epp#clientTransferProhibited'], 'dnssec': False, 'name_servers': ['ns-1033.awsdns-01.org', 'ns-358.awsdns-44.com', 'ns-cloud-e1.googledomains.com', 'ns-cloud-e2.googledomains.com'], 'registrant': 'Stack Exchange, Inc.', 'emails': ['domainabuse@cscglobal.com', 'sysadmin-team@stackoverflow.com']}

# {'name': 'live', 'tld': 'live', 'registrar': 'Dog Beach, LLC', 'registrant_country': '',                                 'creation_date': datetime.datetime(2015, 6, 25, 0, 0), 'expiration_date': None, 'last_updated': None,                                                                                 'status': '', 'statuses': [''],                                                                                                                                                    'dnssec': False, 'name_servers': [], 'registrant': '', 'emails': ['cctld.co@mintic.gov.co', 'gonzalo@cointernet.com.co', 'tldadmin@donuts.emai', 'tldtech@donuts.emai']}
# {'name': 'benkartz.in', 'tld': 'in', 'registrar': 'Endurance Digital Domain Technology LLP', 'registrant_country': 'IN', 'creation_date': datetime.datetime(2019, 8, 14, 9, 32, 49), 'expiration_date': datetime.datetime(2023, 8, 14, 9, 32, 49), 'last_updated': datetime.datetime(2022, 8, 19, 10, 1, 28), 'status': 'clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited', 'statuses': ['clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited'], 'dnssec': False, 'name_servers': ['athena.ns.cloudflare.com', 'todd.ns.cloudflare.com'], 'registrant': 'N/A', 'emails': ['abuse@publicdomainregistry.com']}
# {'name': 'bossover.in', 'tld': 'in', 'registrar': 'GoDaddy.com, LLC', 'registrant_country': 'IN',                        'creation_date': datetime.datetime(2021, 3, 31, 11, 15, 30), 'expiration_date': datetime.datetime(2024, 3, 31, 11, 15, 30), 'last_updated': datetime.datetime(2023, 3, 9, 8, 21, 43), 'status': 'clientRenewProhibited http://www.icann.org/epp#clientRenewProhibited', 'statuses': ['clientDeleteProhibited http://www.icann.org/epp#clientDeleteProhibited', 'clientRenewProhibited http://www.icann.org/epp#clientRenewProhibited', 'clientTransferProhibited http://www.icann.org/epp#clientTransferProhibited', 'clientUpdateProhibited http://www.icann.org/epp#clientUpdateProhibited'], 'dnssec': False, 'name_servers': ['athena.ns.cloudflare.com', 'todd.ns.cloudflare.com'], 'registrant': 'nexolt', 'emails': ['']}
