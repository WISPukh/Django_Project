import os

print(os.listdir('../../'))

with open('../../.env', 'r') as test:
    print(test.readlines())
