import sys
from tests import check, line

result = sys.stdin.read()
print(result)

line()

check("name" in result and "services" in result, "The compose file must be valid")

check("postgres" in result, "postgres service must be defined in the compose file")
check("pgadmin" in result, "pgadmin service must be defined in the compose file")

check("volumes" in result, "You must define required environment variables for both of the services")

check("/var/lib/postgresql" in result, "Use /var/lib/postgresql/data as the volume for the postgres service")
check("/docker-entrypoint-initdb.d" in result, "Use /docker-entrypoint-initdb.d/ as the volume for the postgres service")

print("Success!")
