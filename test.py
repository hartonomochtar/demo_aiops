from dotenv import load_dotenv
load_dotenv()
import os
x = os.getenv("OPENAI_API_KEY")
print(x)