from dotenv import load_dotenv
from openai import OpenAI

# Load biến môi trường từ file .env
load_dotenv()

# Khởi tạo client OpenAI
client = OpenAI()

# Gửi yêu cầu test
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Bạn là chuyên gia thiết kế nội thất"},
        {"role": "user", "content": "Thiết kế phòng ngủ 12m2 phong cách tối giản"}
    ]
)

# In kết quả ra màn hình
print(response.choices[0].message.content)
