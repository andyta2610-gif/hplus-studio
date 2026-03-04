from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Hãy mô tả ngắn gọn một phòng ngủ phong cách Zen."
)

print(response.output_text)
