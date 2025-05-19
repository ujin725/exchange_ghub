import streamlit as st
from PIL import Image
import base64
import random
from datetime import datetime
import io
import os
import json
import shutil

# 페이지 설정
st.set_page_config(
    page_title="생일 축하 메시지 생성기",
    page_icon="🎂",
    layout="wide"
)

# 저장된 설정과 이미지를 위한 디렉토리 생성
SAVE_DIR = "saved_birthday_data"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)
if not os.path.exists(os.path.join(SAVE_DIR, "images")):
    os.makedirs(os.path.join(SAVE_DIR, "images"))

# 설정 파일 경로
CONFIG_FILE = os.path.join(SAVE_DIR, "config.json")

def save_uploaded_image(uploaded_file):
    """업로드된 이미지를 저장하고 파일 경로를 반환"""
    if uploaded_file is not None:
        file_path = os.path.join(SAVE_DIR, "images", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        return file_path
    return None

def load_saved_config():
    """저장된 설정을 불러옴"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding='utf-8') as f:
            return json.load(f)
    return None

def save_config(config):
    """설정을 파일에 저장"""
    with open(CONFIG_FILE, "w", encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# 저장된 설정 불러오기
saved_config = load_saved_config()

# 배경 이미지 선택 옵션
BACKGROUND_IMAGES = {
    "꽃밭": "https://images.unsplash.com/photo-1490750967868-88aa4486c946",
    "벚꽃": "https://images.unsplash.com/photo-1522383225653-ed111181a951",
    "장미": "https://images.unsplash.com/photo-1494972308805-463bc619d34e",
    "풍선": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d",
    "반짝이": "https://images.unsplash.com/photo-1527524816188-6c7c27d61adb"
}

def get_image_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# 사이드바에서 설정
with st.sidebar:
    st.title("🎉 메시지 설정")
    
    # 텍스트 설정
    recipient_name = st.text_input("받는 사람 이름", 
                                 value=saved_config.get("recipient_name", "안미영") if saved_config else "안미영")
    age = st.number_input("나이", min_value=1, 
                         value=saved_config.get("age", 59) if saved_config else 59)
    sender = st.text_input("보내는 사람", 
                          value=saved_config.get("sender", "가족일동") if saved_config else "가족일동")
    
    # 색상 설정
    text_color = st.color_picker("텍스트 색상", 
                                value=saved_config.get("text_color", "#FF69B4") if saved_config else "#FF69B4")
    text_color2 = st.color_picker("보내는 사람 색상", 
                                 value=saved_config.get("text_color2", "#4B0082") if saved_config else "#4B0082")
    
    # 글자 크기 설정
    font_size = st.slider("글자 크기", 40, 100, 
                         value=saved_config.get("font_size", 72) if saved_config else 72)
    
    st.markdown("---")
    st.subheader("🖼 배경 설정")
    
    # 배경 선택 방식
    background_type = st.radio("배경 선택 방식", ["기본 배경", "직접 업로드"])
    
    if background_type == "기본 배경":
        background = st.selectbox("배경 이미지 선택", list(BACKGROUND_IMAGES.keys()))
        background_url = BACKGROUND_IMAGES[background]
    else:
        uploaded_bg = st.file_uploader("배경 이미지 업로드", type=['png', 'jpg', 'jpeg'])
        if uploaded_bg:
            background_image = Image.open(uploaded_bg)
            background_url = f"data:image/png;base64,{get_image_base64(background_image)}"
        else:
            background_url = BACKGROUND_IMAGES["꽃밭"]
    
    st.markdown("---")
    st.subheader("📸 추가 이미지")
    
    # 추가 이미지 업로드
    uploaded_images = st.file_uploader("추가할 이미지 선택 (최대 3개)", 
                                     type=['png', 'jpg', 'jpeg'], 
                                     accept_multiple_files=True)
    
    # 이미지 저장 및 경로 저장
    image_paths = []
    if uploaded_images:
        for img in uploaded_images[:3]:
            path = save_uploaded_image(img)
            if path:
                image_paths.append(path)

    # 이미지 크기 설정
    image_size = st.slider("추가 이미지 크기", 100, 300, 
                          value=saved_config.get("image_size", 200) if saved_config else 200)
    
    # 애니메이션 설정
    st.markdown("---")
    st.subheader("✨ 효과 설정")
    animation_speed = st.slider("색상 변화 속도(초)", 1, 10, 3)
    flower_count = st.slider("꽃잎 수", 5, 50, 20)

# CSS 스타일 정의
st.markdown(f"""
    <style>
    .main {{
        background-color: rgba(255,255,255,0.7);
    }}
    .birthday-text {{
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        color: {text_color};
        text-align: center;
        padding: 10px;
        margin: 10px;
        animation: colorChange {animation_speed}s infinite;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        max-width: 100%;
    }}
    .birthday-line {{
        font-size: {int(font_size * 0.8)}px;  # 글자 크기를 약간 줄임
        display: block;
        margin: 10px 0;
        word-break: keep-all;
        line-height: 1.2;
        padding: 0 10px;
    }}
    .family-text {{
        font-family: 'Arial', sans-serif;
        font-size: {max(24, font_size//2)}px;
        color: {text_color2};
        text-align: center;
        margin-top: 20px;
    }}
    @keyframes colorChange {{
        0% {{ color: {text_color}; }}
        50% {{ color: {text_color2}; }}
        100% {{ color: {text_color}; }}
    }}
    .flower {{
    
        font-size: 30px;
        position: fixed;
        animation: falling 10s infinite linear;
        z-index: 1;
    }}
    @keyframes falling {{
        0% {{ transform: translateY(-100vh) rotate(0deg); }}
        100% {{ transform: translateY(100vh) rotate(360deg); }}
    }}
    .stApp {{
        background-image: url("{background_url}");
        background-attachment: fixed;
        background-size: cover;
        background-position: center;
    }}
    .custom-image {{
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 10px;
        transition: transform 0.3s;
    }}
    .custom-image:hover {{
        transform: scale(1.05);
    }}
    .image-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 떨어지는 꽃 효과
flowers = ['🌸', '🌺', '🌹', '🌷', '💐']
for i in range(flower_count):
    left = random.randint(0, 100)
    delay = random.randint(0, 10)
    flower = random.choice(flowers)
    st.markdown(f"""
        <div class="flower" style="left: {left}vw; animation-delay: {delay}s">
            {flower}
        </div>
    """, unsafe_allow_html=True)

# 중앙 컨테이너
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True)
    st.markdown(
        f'''<div class="birthday-text">
            <div class="birthday-line">세상에서 제일 마음씨 착하고</div>
            <div class="birthday-line">앤공주 같은</div>
            <div class="birthday-line">{recipient_name}의</div>
            <div class="birthday-line">{age}번째</div>
            <div class="birthday-line">생일을</div>
            <div class="birthday-line">축하해!!!</div>
        </div>''',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="family-text">- {sender} -</div>',
        unsafe_allow_html=True
    )
    
    # 추가 이미지 표시
    if saved_config and "image_paths" in saved_config:
        st.markdown(f'<div class="image-container">', unsafe_allow_html=True)
        for img_path in saved_config["image_paths"]:
            if os.path.exists(img_path):
                image = Image.open(img_path)
                # 이미지 크기 조정
                aspect_ratio = image.width / image.height
                new_width = image_size
                new_height = int(image_size / aspect_ratio)
                image = image.resize((new_width, new_height))
                img_base64 = get_image_base64(image)
                st.markdown(f"""
                    <img src="data:image/png;base64,{img_base64}" 
                         width="{new_width}" 
                         height="{new_height}"
                         class="custom-image">
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    elif uploaded_images:
        st.markdown(f'<div class="image-container">', unsafe_allow_html=True)
        for img in uploaded_images[:3]:
            image = Image.open(img)
            aspect_ratio = image.width / image.height
            new_width = image_size
            new_height = int(image_size / aspect_ratio)
            image = image.resize((new_width, new_height))
            img_base64 = get_image_base64(image)
            st.markdown(f"""
                <img src="data:image/png;base64,{img_base64}" 
                     width="{new_width}" 
                     height="{new_height}"
                     class="custom-image">
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 현재 날짜 표시
st.markdown(
    f'<div style="position: fixed; bottom: 20px; right: 20px; color: white;">{datetime.now().strftime("%Y-%m-%d")}</div>',
    unsafe_allow_html=True
)

# 저장 버튼
if st.button("현재 설정 저장"):
    config = {
        "recipient_name": recipient_name,
        "age": age,
        "sender": sender,
        "text_color": text_color,
        "text_color2": text_color2,
        "font_size": font_size,
        "background_type": background_type,
        "background": background if background_type == "기본 배경" else "사용자 지정",
        "animation_speed": animation_speed,
        "flower_count": flower_count,
        "image_size": image_size,
        "image_paths": image_paths  # 이미지 경로 저장
    }
    save_config(config)
    st.success("설정이 저장되었습니다!")