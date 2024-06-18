# LLM-RAG

## Giới thiệu

LLM-RAG (Language Learning Model - Retrieval-Augmented Generation) là một dự án tích hợp các kỹ thuật truy vấn và tổng hợp để cải thiện hiệu quả của các mô hình ngôn ngữ lớn (LLM) trong việc trả lời câu hỏi và tìm kiếm thông tin. Dự án này tập trung vào xây dựng một chatbot du lịch với các chức năng phản hồi về địa điểm, ẩm thực, tư vấn, cẩm nang, thời tiết và giao thông. 


⚠️File gemini_rag.py: Việc xây dựng model LLM với cấu trúc RAG bằng framework Langchain vẫn có khả năng tìm kiếm và truy xuất thông tin dựa trên vector database nhưng do API Gemini hoặc một lỗi nào đó liên quan đến request time_out nên model luôn trả lời : "Tôi không biết"

## Công nghệ sử dụng

- **Langchain**: Một framework để xây dựng các ứng dụng dựa trên chuỗi ngôn ngữ.
- **FAISS**: Thư viện của Facebook AI để tìm kiếm hiệu quả trong không gian vector.
- **Streamlit**: Một công cụ mã nguồn mở để tạo giao diện web cho các ứng dụng machine learning.
- **Gemini**: Mô hình ngôn ngữ sử dụng trong dự án này.

## Cài đặt

### Yêu cầu

- Python 3.x
- Các thư viện cần thiết được liệt kê trong file `requirement.txt`

### Hướng dẫn cài đặt

1. Clone repository:
    ```bash
    git clone https://github.com/linhphongz/LLM-RAG.git
    cd LLM-RAG
    ```
2. Cài đặt các thư viện:
    ```bash
    pip install -r requirement.txt
    ```

## Sử dụng

### Chạy ứng dụng

- Chạy ứng dụng với RAG:
    ```bash
    python app_with_rag.py
    ```
- Chạy ứng dụng không dùng RAG:
    ```bash
    python app_without_rag.py
    ```

### Tạo cơ sở dữ liệu vector

- Tạo cơ sở dữ liệu vector:
    ```bash
    python create_vector_db.py
    ```

## Cấu trúc thư mục

- `data_source/`: Chứa các nguồn dữ liệu
- `faiss_index/`: Chứa các chỉ mục FAISS
- `.env`: File cấu hình môi trường
- `app_with_rag.py`: Ứng dụng dùng RAG
- `app_without_rag.py`: Ứng dụng không dùng RAG
- `create_vector_db.py`: Script tạo cơ sở dữ liệu vector
- `gemini_rag.ipynb`: Notebook minh họa
- `gemini_rag.py`: Mã nguồn cho RAG
- `requirement.txt`: Các thư viện cần thiết

## Đóng góp

Chúng tôi hoan nghênh mọi đóng góp cho dự án này. Vui lòng mở issue hoặc tạo pull request để đóng góp.

