#sudo CUSTOMER=47lining CAGE=build ./install.sh
KEYSTORE=$CUSTOMER-$CAGE.keystore
jenkins_lib=/var/lib/jenkins
# run as sudo
echo Copy $KEYSTORE to $jenkins_lib secrets
cp $KEYSTORE $jenkins_lib/secrets

echo Copy cacerts to /etc/pki/java/cacerts
cp cacerts /etc/pki/java/cacerts

echo Restarting Jenkins
service jenkins restart