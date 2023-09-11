#!/bin/sh
#
# Run the alfresco-db-queires tool, output the PID number
# and exit

{{ alfresco_java }} --add-opens=java.base/java.lang=ALL-UNNAMED --add-opens=java.base/java.util=ALL-UNNAMED -jar alfresco-db-0.0.1-SNAPSHOT.jar &

ps -o pid,cmd -C java | awk '/alfresco-db-0.0.1-SNAPSHOT.jar/{print $1}'

