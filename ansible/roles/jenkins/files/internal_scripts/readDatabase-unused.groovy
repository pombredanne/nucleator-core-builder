/*
# Copyright 2015 47Lining LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
*/
def jc = this.getClass().getClassLoader().rootLoader
def furl = new File("sqlite-jdbc-3.8.7.jar").toURL()
jc.addURL(furl)
import groovy.sql.Sql
def sql = Sql.newInstance( 'jdbc:sqlite:databasefile.sqlite',   'org.sqlite.JDBC' )
def metadata = sql.connection.getMetaData()
def tables = metadata.getTables(null, null, "CAGES", null)
if (!tables.next()) {
	println "Creating table"
    // table does not exist
    sql.execute("create table CAGES (Name varchar(128));")
    println "None"
    return ["none defined"];
} else {
	println "Querying table"
	def cages = []
    sql.rows("select Name from CAGES order by Name ASC").each{
    	println it.get('Name')
 		cages.add(it.get('Name'))
	}
	return cages;
}

return ["A"]



import groovy.sql.Sql
//def jc = jenkins.getPluginManager().uberClassLoader;
def jc = this.getClass().getClassLoader()
def furl = new File("/vagrant/lib/sqlite-jdbc-3.8.7.jar").toURL()
jc.addURL(furl)
def cc = Class.forName('org.sqlite.JDBC', true, jc)
java.sql.DriverManager.registerDriver(cc.newInstance())
def sql = Sql.newInstance( 'jdbc:sqlite:databasefile.sqlite',   'org.sqlite.JDBC' )
def metadata = sql.connection.getMetaData()
def tables = metadata.getTables(null, null, "CAGES", null)
if (!tables.next()) {
    println "Creating table"
    // table does not exist
    sql.execute("create table CAGES (Name varchar(128));")
    println "None"
    return ["none defined"];
} else {
    println "Querying table"
    def cages = []
    sql.rows("select Name from CAGES order by Name ASC").each{
        println it.get('Name')
        cages.add(it.get('Name'))
    }
    return cages;
}

return [furl.toString(), "A", "B", "C"];