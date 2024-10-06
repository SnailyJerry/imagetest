import streamlit as st
import requests
import json
import base64
from PIL import Image

# 上传图片和提示词，然后调用 GLM4v Plus API 的函数
def connect_glm4vplus_api(prompt, image_path):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "Bearer b82d3934ce31e2339617905d0022ce19.1rxFSnsPkbuRAMbG",  # 替换为实际的 API Key
        "Content-Type": "application/json"
    }
    
    # 读取图像并转换为 Base64 编码
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    
    data = {
        "model": "glm-4v-plus",  # 模型名称
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": 0.8,
        "max_tokens": 1024,
        "stream": False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return response_data.get("choices", [{}])[0].get("message", {}).get("content", "没有返回结果")
    else:
        return f"请求失败，状态码: {response.status_code}, 信息: {response.text}"

# Streamlit 应用程序
def main():
    st.title("GLM-4v Plus API 调用 Web 应用")

    # 上传图片
    uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"])

    # 提示词输入
    prompt = st.text_area("请输入提示词：")

    # 发送请求按钮
    if st.button("发送请求"):
        if uploaded_file is None or not prompt:
            st.warning("请上传图片并输入提示词！")
        else:
            # 保存上传的图片到临时文件
            with open("temp_image.png", "wb") as f:
                f.write(uploaded_file.read())
            
            # 调用 API
            result = connect_glm4vplus_api(prompt, "temp_image.png")
            st.text_area("API 返回结果：", value=result, height=200)

if __name__ == "__main__":
    main()
