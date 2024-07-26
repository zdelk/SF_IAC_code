import re

# Assuming sheet_list is your list of strings
sheet_list = ["example1", "example2", "test1", "test2"]

# The variable you're searching for
name = "test"

# List comprehension to find matching titles
matching_titles = [title for title in sheet_list if re.search(name + r".*", title)]

print(matching_titles)
