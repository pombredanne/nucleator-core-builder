README-ssl.md

This file describes the process for enabling ssl with a self-signed certificate and existing keys.


Creating Self-signed Certificate
--------------------------------

openssl genrsa -out server.key 2048
openssl req -new -out server.csr -key server.key
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.509
NOTE:
In the next step, make sure you put a password on the p12 file -
otherwise you'll get a null reference exception when you try to import it.
 (In case anyone else had this headache)
openssl pkcs12 -export -in server.509 -inkey server.key \
               -out server.crt -name some-alias \
               -CAfile ca.crt -caname root


Creating a Keystore
-------------------

From: http://cunning.sharp.fm/2008/06/importing_private_keys_into_a.html:

The solution is to convert your existing certificate and key into a PKCS12 file, and then use the keytool functionality to merge one keystore with another one. Java 6 can treat a PKCS12 file as a keystore.

Converting x509 cert and key to a PKCS12:

openssl pkcs12 -export -in server.crt -inkey server.key \
               -out server.p12 -name some-alias \
               -CAfile ca.crt -caname root

Converting the pkcs12 file to a Java keystore:
keytool -importkeystore \
        -deststorepass changeit -destkeypass changeit -destkeystore server.keystore \
        -srckeystore server.p12 -srcstoretype PKCS12 -srcstorepass some-password \
        -alias some-alias

The alias of 1 is required to choose the certificate in the source PKCS12 file, keytool isn't clever enough to figure out which certificate you want in a store containing one certificate.

STEPS
-----

ec2-user@nucleator-ui.build:~/.ssh$ openssl req -new -out server.csr -key 47lining.pem
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:US
State or Province Name (full name) []:Colorado
Locality Name (eg, city) [Default City]:Niwot
Organization Name (eg, company) [Default Company Ltd]:47Lining
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server's hostname) []:build.47lining.com
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:

ec2-user@nucleator-ui.build:~/.ssh$ openssl x509 -req -days 365 -in server.csr -signkey 47lining.pem -out server.crt
Signature ok
subject=/C=US/ST=Colorado/L=Niwot/O=47Lining/CN=build.47lining.com
Getting Private key


ec2-user@nucleator-ui.build:~/.ssh$ openssl pkcs12 -export -in server.crt -inkey 47lining.pem -out server.p12 -name nui-cert -CAfile ca.crt -caname root
Enter Export Password: (P@ssw0rd)
Verifying - Enter Export Password:

ec2-user@nucleator-ui.build:~/.ssh$ keytool -importkeystore -deststorepass P@ssw0rd -destkeypass P@ssw0rd -destkeystore server.keystore -srckeystore server.p12 -srcstoretype PKCS12 -srcstorepass P@ssw0rd -alias nui-cert

Yields server.keystore.

ADD TO JAVA
-----------
sudo keytool -importcert -alias nui-cert -file nucleator-ui.crt -keystore /etc/pki/java/cacerts -noprompt -keypass changeit




(nuc_venv)Marks-MacBook-Pro:certs mchance$ openssl req -new -out nucleator-ui.csr -key ../47lining-test1-us-west-2.pem
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:Colorado
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:*.build.47lining.com
Organizational Unit Name (eg, section) []:*.build.47lining.com
Common Name (e.g. server FQDN or YOUR name) []:*.build.47lining.com
Email Address []:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:47Lining
