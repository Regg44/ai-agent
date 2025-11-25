from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
def test():
    test_cases = [
        ["calculator", "lorem.txt", "wait, this isn't lorem ipsum"],
        ["calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
        ["calculator", "/tmp/temp.txt", "this should not be allowed"],
    ]

    for cases in test_cases:
        wd, fl, cont = cases
        print(write_file(wd, fl, cont))

if __name__ == "__main__":
    test()