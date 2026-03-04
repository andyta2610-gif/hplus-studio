import os
import base64
import uuid
from openai import OpenAI
from dotenv import load_dotenv
from config import OPENAI_API_KEY

load_dotenv()

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_customer_design(area, room_type, style, budget, user_type, description=""):

    prompt = f"""
Bạn là chuyên gia thiết kế nội thất phong cách {style} cao cấp.

Thông tin khách hàng:
- Yêu cầu thêm: {description}
- Diện tích: {area} m2
- Loại phòng: {room_type}
- Ngân sách: {budget}
- Đối tượng: {user_type}

Trả về nội dung theo cấu trúc rõ ràng:

1. CONCEPT TỔNG THỂ
2. BỐ TRÍ KHÔNG GIAN
3. VẬT LIỆU ĐỀ XUẤT
4. BẢNG MÀU CHỦ ĐẠO
5. ƯỚC TÍNH CHI PHÍ
6. ĐIỂM NHẤN THIẾT KẾ
"""

    # 🔥 Tạo nội dung AI
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia thiết kế nội thất."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    design_text = response.choices[0].message.content

    # 🎨 Tạo ảnh AI
    image_prompt = f"{style} {room_type} interior design, {area}m2, high quality, realistic, 4k render"

    image = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024"
    )

    # Lấy dữ liệu base64
    image_base64 = image.data[0].b64_json

    # Giải mã base64 thành bytes
    image_bytes = base64.b64decode(image_base64)

    # Tạo thư mục static nếu chưa có
    if not os.path.exists("static"):
        os.makedirs("static")

    # Tạo tên file ngẫu nhiên
    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join("static", filename)

    # Lưu file ảnh
    with open(filepath, "wb") as f:
        f.write(image_bytes)

    # Đường dẫn để hiển thị trên web
    image_url = f"/static/{filename}"

    return {
        "design_text": design_text,
        "image_url": image_url
    }
