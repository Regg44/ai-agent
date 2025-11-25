from functions.get_files_info import get_files_info

test_cases = [
    ["calculator", "."],
    ["calculator", "pkg"],
    ["calculator", "/bin"],
    ["calculator", "../"]
]

for case in test_cases:
    wd, d = case
    if d == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{d}' directory:")
    get_files_info(wd, d)