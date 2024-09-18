
def check(condition: bool, message: str) -> None:
    if not condition:
        print("FAILED:", message)
        exit(1)

def line(width=80):
    print("\n" + "=" * width + "\n")
