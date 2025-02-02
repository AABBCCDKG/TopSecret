import os
import base64
import logging
from datetime import datetime
from dotenv import load_dotenv
import openai
from googleapiclient.discovery import build
from google.oauth2 import service_account
import time

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

SCOPES = ["https://www.googleapis.com/auth/documents"]
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS")  
DOC_ID = os.getenv("GOOGLE_DOC_ID") 

try:
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    docs_service = build("docs", "v1", credentials=credentials)
    logging.info("✅ Google Docs API 认证成功")
except Exception as e:
    logging.error(f"❌ Google Docs API 认证失败: {e}")
    exit(1)

API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=API_KEY)

def capture_screenshot():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    command = f"screencapture -x {filename}"  

    try:
        os.system(command)
        if os.path.exists(filename):
            logging.info(f"✅ 截图成功: {filename}")
            return filename
        else:
            logging.error(f"❌ 截图失败: {filename}")
            return None
    except Exception as e:
        logging.error(f"❌ 截图命令执行失败: {e}")
        return None

def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        logging.error(f"❌ 图片编码失败: {e}")
        return None

def analyze_image(image_path):
    if not image_path:
        return
    
    try:
        base64_image = encode_image(image_path)
        if not base64_image:
            return

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "I will upload some question. I need you give me the answer"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                    ],
                }
            ],
        )
        
        analysis_result = response.choices[0].message.content
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        requests = [{
            "insertText": {
                "location": {"index": 1},
                "text": f"\n{timestamp}: {analysis_result}\n"
            }
        }]
        docs_service.documents().batchUpdate(documentId=DOC_ID, body={"requests": requests}).execute()
        logging.info(f"✅ 结果已添加至 Google Docs: {analysis_result}")
    
    except Exception as e:
        logging.error(f"❌ 处理图片失败: {e}")
    
    finally:
        try:
            os.remove(image_path)
            if not os.path.exists(image_path):
                logging.info(f"✅ 文件已删除: {image_path}")
            else:
                logging.warning(f"❌ 文件删除失败: {image_path}")
        except Exception as e:
            logging.error(f"❌ 删除文件时出错: {e}")

while True:
    '''
    # Issue: 至少对于macbook来说，ssh只能截取默认桌面，无法截取当前GUI，所以暂时还无法远程操作
    command = input("输入 'a' 进行截图，或输入 'q' 退出: ")
    if command.lower() == 'a':
        screenshot_path = capture_screenshot()
        if screenshot_path:
            analyze_image(screenshot_path)
    elif command.lower() == 'q':
        logging.info("🔚 退出程序")
        break
    '''
    screenshot_path = capture_screenshot()
    analyze_image(screenshot_path)
    time.sleep(3)  # 每 3 秒截屏一次