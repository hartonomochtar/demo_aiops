from agent_dispatcher import *
from agent_trace import *
from agent_esb import *
from agent_co import *
from agent_ufo import *
from agent_c2p import *
from agent_reviewer import *
from query_data import *
import json

def main():
    while True:
        user_input = input("Inquiry:")
        if "bye" in user_input:
            print("Bye-bye")
            break
        else:
            response = agent_dispatcher(user_input)
            print("\n")

if __name__ == "__main__":
    main()