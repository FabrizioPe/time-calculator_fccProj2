# This entrypoint file to be used in development. Start by reading README.md
from time_calculator import *
from unittest import main

print(add_time("11:59 PM", "1:05", "Wednesday"))

# Run unit tests automatically
main(module='test_module', exit=False)