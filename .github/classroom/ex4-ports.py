import sys
from tests import check, line

result = sys.stdin.read()
print(result)

line()

check("name" in result and "services" in result, "The compose file must be valid")

check("postgres" in result, "postgres service must be defined in the compose file")
check("pgadmin" in result, "pgadmin service must be defined in the compose file")

check("ports" in result, "You must define published ports for both of the services")

check("5432" in result, "Use 5432 as the published port for the postgres service, you can use any port on the host")
check("80" in result, "Use 80 as the published port for the pgadmin service, you can use any port on the host")

print("Success!")
