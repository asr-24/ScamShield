import ssl
import socket

def check_ssl_certificate(url):
    try:
        hostname = url.split("//")[-1].split("/")[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as sslsock:
                # Certificate validation
                cert = sslsock.getpeercert()
                if cert:
                    return True
                else:
                    return False
    except Exception as e:
        print("An error occurred:", str(e))
        return False

def certificates_results(result):
    if result:
        print("SSL certificate is valid.")
    else:
        print("SSL certificate is not valid or an error occurred.")

if __name__ == "__main__":
    url = input("Enter a website URL: ")
    certificates_results(check_ssl_certificate(url))
else:
    pass

    
