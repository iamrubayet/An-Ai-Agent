
import sys
from agent.agent import Agent


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your question here\"")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    agent = Agent()
    result = agent.answer(query)
    print(result)


if __name__ == "__main__":
    main()