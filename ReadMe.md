# SlackBot

### Mô tả
SlackBot là một bot được sử dụng để trả lời các câu hỏi liên quan đến nội quy và các vấn đề khác trong công ty. Bot này được xây dựng bằng Python, sử dụng OpenAI và tích hợp với Slack.

### Tài liệu tham khảo
- **Langchain**: [Langchain Documentation](https://python.langchain.com/docs/get_started/introduction)
- **ChromaDB**: [ChromaDB Documentation](https://www.trychroma.com/)
- **Slack Bot**: 
   - [Slack API for Apps](https://api.slack.com/apps)
   - [Tạo Bot Chào Mừng Người Dùng](https://api.slack.com/tutorials/tracks/create-bot-to-welcome-users)

Bot chủ yếu sử dụng Langchain.

### Cài đặt
1. Tạo và cấu hình bot Slack, điền đầy đủ thông tin vào tệp `.env`.
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
3. Tạo các embedding từ dữ liệu:
    ```bash
    python3 embedder.py
   ```
4. Tạo các embedding từ dữ liệu:
    ```bash
    python3 slack_bot.py
   ```
### Chức năng cần bổ sung
- Thêm chức năng cho phép bot tiếp nhận và cập nhật dữ liệu trực tiếp.
### Chạy bằng Docker
1. Tạo và cấu hình bot Slack, điền đầy đủ thông tin vào tệp `.env`.
    ```bash
   docker build -t chatbot .
   ```
2. Cài đặt các thư viện cần thiết:
   ```bash
   docker run -d chatbot
   ```
### NOTE
- Mỗi khi thêm dữ liệu mới, cần build và chạy lại container Docker.