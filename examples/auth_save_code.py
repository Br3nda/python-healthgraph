import argparse
from healthgraph import User

parser = argparse.ArgumentParser()
parser.add_argument("code")
args = parser.parse_args()

user = User()
user.auth(args.code)

