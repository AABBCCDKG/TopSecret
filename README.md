# 配置环境

## **1. 创建 Google Cloud 项目**
1. **打开** [Google Cloud Console](https://cloud.google.com/) 并 **创建新项目**。
2. 进入 **"API 和服务"** > **"启用 API 和服务"**。
3. 搜索并启用：
   - [Google Docs API](https://developers.google.com/docs/api/how-tos/overview)
4. **创建服务账号**：
   - 进入 **"API 和服务"** > **"凭据"** > **"创建凭据"** > **"服务账号"**。
   - 赋予 **"编辑者（Editor）"** 和 **"Google Docs API 用户"** 权限。
   - 进入 **"密钥"** > **"添加密钥"** > **"JSON"**，下载 **`.json` 凭证文件**。

---

## **2. 配置 Google Docs**
1. **打开 Google Docs**。
2. **获取文档 ID**：
   - 复制 **Google Docs 链接**：
     ```
     https://docs.google.com/document/d/YOUR_DOC_ID/edit
     ```
   - 其中 `YOUR_DOC_ID` 即为 **文档 ID**。
3. **共享权限**：
   - 点击 **"共享"** 按钮。
   - 添加 **服务账号邮箱**（在 `.json` 文件内）。
   - 设置为 **"编辑者"**，以允许写入。

---

## **3. 设置 API 密钥**
### **替换 `main.py` 变量**
- **Google 凭证**：下载的 `.json` 文件路径
- **Google Docs ID**：文档的 ID
- **OpenAI API Key**：[获取 API Key](https://platform.openai.com/api-keys)

```python
CREDENTIALS_FILE = "your_google_credentials.json"  # 替换为你的 JSON 凭证文件路径
DOC_ID = "your_google_doc_id"  # 替换为你的 Google Docs ID
API_KEY = "your_openai_api_key"  # 替换为你的 OpenAI API Key
```

## How to use

```sh
git clone https://github.com/AABBCCDKG/TopSecret.git
pip install -r requirements.txt
python main.py

