import re

regex="(?:(?=.*\S)(?=.*[a-z]+)(?=.*\d+)(?=.*[A-Z]+).\S{6,})"


test_2 = "Alligarto3!"
test_3 = 'fjd3IR9'
print(bool(re.fullmatch("(?:(?=.*\S)(?=.*[a-z]+)(?=.*\d+)(?=.*[A-Z]+).\S{6,})", "dsF43")))
print(bool(re.fullmatch("(?:(?=.*\S)(?=.*[a-z]+)(?=.*\d+)(?=.*[A-Z]+).\S{6,})", "fjd3  IR9")))
