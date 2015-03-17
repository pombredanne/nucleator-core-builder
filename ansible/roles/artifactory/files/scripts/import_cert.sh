#CUSTOMER=47lining CAGE=build ./import_cert.sh
KEYSTORE=$CUSTOMER-$CAGE.keystore
CERT=$CUSTOMER-$CAGE.crt
ALIAS=$CUSTOMER-$CAGE-cert
X509=$CUSTOMER-$CAGE.509
keystore_password=P@ssw0rd
java_keystore_password=changeit
artifactory_tomcat_home=/usr/share/artifactory-3.4.2
CACERTS=cacerts

echo KS is $KEYSTORE
echo CERT is $CERT
echo ALIAS is $ALIAS
echo X509 is $X509

rm -f $KEYSTORE
rm -f $X509
rm -f $CACERTS
cp /etc/pki/java/cacerts ./cacerts

echo Creating $KEYSTORE
keytool -importkeystore \
 -deststorepass $keystore_password \
 -destkeypass $keystore_password \
 -destkeystore $KEYSTORE \
 -srckeystore $CERT \
 -srcstoretype PKCS12 \
 -srcstorepass $keystore_password \
 -alias $ALIAS

echo Generate x509 for importing
openssl pkcs12 \
  -in $CERT \
  -clcerts -nokeys \
  -passin pass:$keystore_password | openssl x509 > $X509

echo Deleting alias from /etc/pki/java/cacerts
keytool -delete \
  -storepass $java_keystore_password \
  -alias $ALIAS \
  -keystore $CACERTS -noprompt

echo Updating /etc/pki/java/cacerts
keytool -importcert \
  -alias $ALIAS \
  -file $X509 \
  -storepass $java_keystore_password \
  -keystore $CACERTS -noprompt