import sys
from tests import check, line

result = sys.stdin.read()
print(result)

line()

check(len(result.splitlines()) > 2, "Save the names of the tracks in the hello-world.txt file")

check("Phoney Smile Fake Hellos" in result, "'Phoney Smile Fake Hellos' should be included in the results")
check("World Of Trouble" in result, "'World Of Trouble' should be included in the results")
check("Hello Mary Lou" in result, "'Hello Mary Lou' should be included in the results")
check("Woman Of The World" in result, "'Woman Of The World (Ao Vivo)' should be included in the results")
check("Edge Of The World" in result, "'Edge Of The World' should be included in the results")
check("My World" in result, "'My World' should be included in the results")
check("Different World" in result, "'Different World' should be included in the results")
check("Brave New World" in result, "'Brave New World' should be included in the results")
check("Say Hello 2 Heaven" in result, "'Say Hello 2 Heaven' should be included in the results")

check("Bohemian Rhapsody" not in result, "'Bohemian Rhapsody' should not be included in the results")

print("Success!")
