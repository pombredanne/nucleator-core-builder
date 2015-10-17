Builder Stackset SSL Setup
==========================

This README describes the process for enabling ssl for jenkins and
artifactory through a user-provided certificate, private key, and
Certificate-Authority-provided bundle of certificates required to
establish chain-of-trust.

You can provide a certificate that you have procured that is signed by
a trusted Certificate Authority (CA), or a certificate that you have
signed yourself.

Required Certificate-Related Files and Passwords
------------------------------------------------

The builder stackset expects the following files to be in place:

    ~/.nucleator/siteconfig/<customer>-<cage>.pkcs12

`<customer>-<cage>.pkcs12` is a pkcs12-format certificate bundle that
is expected to include the X-509 certificate signed by yourself or
your chosen CA, the private key used to generate the certificate, and
a CA.crt bundle of certificates used to validate chain-of-trust, if
provided by your certificate authority.

The stackset expects to find the certificate bundle within the
siteconfig for your nucleator installation.

This stackset uses the following passwords, specified in
`~/.nucleator/<customer>-credentials.yml`

    #
    # This is the password that will be used by the builder stackset
    # to access the provided pkcs12-format bundle of SSL certificates
    # and private keys, and to set up application-specific keystores
    # (e.g. for Jenkins and Artifactory).
    # 
    # You can set this to whatever you would like, provided that the
    # <customer>-<cage>.pkcs12 certificate bundle that you provide in
    # your siteconfig was generated and is accessible using this password.
    #
    pkcs12_bundle_password: add_password_here
    
    #
    # This is the password used to maintain java's cacert keystore.
    # The default as shipped for most java distributions is 'changeit'
    # You shouldn't need to change this unless you have taken explicit action
    # to change from this default.
    #
    java_cacert_keystore_password: changeit
    
Generating Required Certificate-Related Files
---------------------------------------------

You can procure an SSL Certificate from a Certificate Authority (CA) of your
choice, in which case the Certificate will be signed by your chosen CA.

Alternatively, you can act as your own Certificate Authority and, and create
a Self-Signed Certificate.

If you wish to create a self-signed certificate, you can do so using the
make-certificate-bundle script.  The script can be found in the
nucleator-core-siteconfig repository at

    ansible/roles/siteconfig/vars/make-certificate-bundle

It's usage is:

    make-certificate-bundle <customer> <cage> <customer-domain> <password>

For example:

    make-certificate-bundle example build example.yourdomain.com Arb1trary!

To ensure that downstream nucleator stacksets will be able to access
the certificate bundle that you are providing, be sure the password you
use here matches the password value entered for pkcs12_bundle_password
in the corresponding customer credentials file at
`~/.nucleator/<customer>-credentials.yml`.

Once you have generated all of the required `.pkcs12` bundles, commit them
to your personal siteconfig.  Be sure to then run `nucleator update` so that
your change become available to nucleator.

Appendix - Useful opensll information
-------------------------------------

The remainder of this document is retained here solely for reference and historic purposes.

```
openssl genrsa -out server.key 2048
openssl req -new -out server.csr -key server.key
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.509
```

NOTE:
In the next step, make sure you put a password on the p12 file -
otherwise you'll get a null reference exception when you try to import it.
 (In case anyone else had this headache)
```
openssl pkcs12 -export -in server.509 -inkey server.key \
               -out server.crt -name some-alias \
               -CAfile ca.crt -caname root
```

Password: P@ssw0rd
Alias: 47lining-build-cert

#### Creating a Keystore

From: http://cunning.sharp.fm/2008/06/importing_private_keys_into_a.html:

The solution is to convert your existing certificate and key into a PKCS12 file, and then use the keytool functionality to merge one keystore with another one. Java 6 can treat a PKCS12 file as a keystore.

Converting x509 cert and key to a PKCS12:

```
openssl pkcs12 -export -in server.crt -inkey server.key \
               -out server.p12 -name some-alias \
               -CAfile ca.crt -caname root
```

Converting the pkcs12 file to a Java keystore:
```
keytool -importkeystore \
        -deststorepass changeit -destkeypass changeit -destkeystore server.keystore \
        -srckeystore server.p12 -srcstoretype PKCS12 -srcstorepass some-password \
        -alias some-alias
```

The alias of 1 is required to choose the certificate in the source PKCS12 file, keytool isn't clever enough to figure out which certificate you want in a store containing one certificate.

#### STEPS

```
ec2-user@nucleator-ui.build:~/.ssh$ openssl req -new -out server.csr -key 47lining.pem
```
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
```
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
```

```
ec2-user@nucleator-ui.build:~/.ssh$ openssl x509 -req -days 365 -in server.csr -signkey 47lining.pem -out server.crt

Signature ok
subject=/C=US/ST=Colorado/L=Niwot/O=47Lining/CN=build.47lining.com
Getting Private key
```

```
ec2-user@nucleator-ui.build:~/.ssh$ openssl pkcs12 -export -in server.crt -inkey 47lining.pem -out server.p12 -name nui-cert -CAfile ca.crt -caname root
Enter Export Password: (P@ssw0rd)
Verifying - Enter Export Password:
```

```
ec2-user@nucleator-ui.build:~/.ssh$ keytool -importkeystore -deststorepass P@ssw0rd -destkeypass P@ssw0rd -destkeystore server.keystore -srckeystore server.p12 -srcstoretype PKCS12 -srcstorepass P@ssw0rd -alias nui-cert
```

Yields server.keystore.

#### ADD TO JAVA

```
sudo keytool -importcert -alias nui-cert -file nucleator-ui.crt -keystore /etc/pki/java/cacerts -noprompt -keypass changeit
```




```
(nuc_venv)Marks-MacBook-Pro:certs mchance$ openssl req -new -out nucleator-ui.csr -key ../47lining-test1-us-west-2.pem
```

```
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
```
