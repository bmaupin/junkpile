- http-server-timeout.py

    Create a web server that accepts connections but never responds to test timeouts:
  
        $ python http-server-timeout.py &
        $ curl -m 5 localhost:8080
        curl: (28) Operation timed out after 5001 milliseconds with 0 bytes received
