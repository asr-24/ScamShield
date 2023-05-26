import ssl
import socket
import networkx as nx
from bs4 import BeautifulSoup as BS
import requests
from urllib.parse import urlparse
import re

#if test failed (is phishing) - True
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
        #print("An error occurred:", str(e))
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
        #print(len(links))

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
    ranking = round(pagerank[url],2)
    #ranking = sum((list(pagerank.values())))
    #print(ranking)
    #return ranking
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
    pass
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
                  "url_registration_validity": 15, 
                  "active_duration": 10, 
                  "length_of_url": 10, 
                  "at_character": 5,
                  "is_redirect": 10,
                  "dashes_in_domain_name": 5,
                  "length_of_domain_name": 10,
                  "no_of_subdomains": 15}
   
    
    summation_of_test_results = 0
    
    print("Welcome to ScamShield\'s \"Fishing?\"")
    url = input("Enter a website URL: ")
    print("\nStarting Tests - \n")

    for i in range(len(tests_list)):
        print(f'Test {(i+1)}: {list(tests_list.keys())[i]}' )

        function = globals().get(list(tests_list.keys())[i])

        result = function(url)
        summation_of_test_results+= (lambda x: 1 if x else 0)(result)*(list(tests_list.values())[i])

        print("Result:", (lambda x: "Failed" if x else "Passed")(result))
        print(f'\n(Status: {int((i+1)*100/len(tests_list))}% Completed)\n\n')


    print(f"The probability that the link you have provided is malicious is {summation_of_test_results}%")        



    
if __name__=="__main__":
    main()




#http://trk.zingtoco.live/campaigns/nr8947da7fcaa/track-url/ky0812sfe4bb4/dfcdd846fa5681674ebb9bf63ab662a333e928b1