#sudo CUSTOMER=47lining CAGE=build ./install.sh
KEYSTORE=$CUSTOMER-$CAGE.keystore
artifactory_tomcat_home=/usr/share/artifactory-3.4.2/tomcat
# run as sudo
echo Copy $KEYSTORE to $artifactory_tomcat_home/conf/ssl
cp $KEYSTORE $artifactory_tomcat_home/conf/ssl

echo Copy cacerts to /etc/pki/java/cacerts
cp cacerts /etc/pki/java/cacerts

echo Restarting Artifactory
service artifactory restart