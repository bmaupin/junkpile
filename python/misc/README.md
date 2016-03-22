- http-server-timeout.py

    Create a web server that accepts connections but never responds to test timeouts:
  
        $ python http-server-timeout.py &
        
        $ curl -m 5 localhost:8080
        curl: (28) Operation timed out after 5001 milliseconds with 0 bytes received
        
        $ groovysh
        groovy:000> new URL('http://localhost:8080').getText(readTimeout:5000)
        ERROR java.net.SocketTimeoutException:
        Read timed out
