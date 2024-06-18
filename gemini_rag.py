import os
import io
from dotenv import load_dotenv
import PyPDF2
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

class QaProcessor:
    def __init__(self, pdf_path="./data_source/dulieudulich.pdf"):
        self.pdf_path = pdf_path
        self.user_question = None  # Khởi tạo user_question là None ban đầu
        self.google_api_key = None
        self.context = None
        self.docs = None
        self.chain = None

        self.load_environment_variables()
        self.check_api_key()
        self.read_pdf()
        self.create_context()
        self.split_text()
        self.create_vector_index()
        self.define_prompt_template()
        self.create_prompt()
        self.load_qa_chain_model()

    def load_environment_variables(self):
        load_dotenv()
        self.google_api_key = os.getenv("GOOGLE_API_KEY")

    def check_api_key(self):
        if self.google_api_key is None:
            print("API key not found. Please set the google_api_key environment variable.")
            exit()

    def read_pdf(self):
        with open(self.pdf_path, "rb") as f:
            pdf_data = f.read()
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
            self.pdf_pages = pdf_reader.pages

    def create_context(self):
        self.context = "\n\n".join(page.extract_text() for page in self.pdf_pages)

    def split_text(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=200)
        self.texts = text_splitter.split_text(self.context)

    def create_vector_index(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vector_index = Chroma.from_texts(self.texts, embeddings).as_retriever()

    def get_documents(self):
        self.docs = self.vector_index.get_relevant_documents(self.user_question)

    def define_prompt_template(self):
        self.prompt_template = """
        Answer the question as detailed as possible from the provided context,
        make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context",
        don't provide the wrong answer\n\n
        Context:\n {context}?\n
        Question: \n{question}\n
        Answer:
        """

    def create_prompt(self):
        self.prompt = PromptTemplate(template=self.prompt_template, input_variables=['context', 'question'])

    def load_qa_chain_model(self):
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, api_key=self.google_api_key)
        self.chain = load_qa_chain(model, chain_type="stuff", prompt=self.prompt)

    def get_response(self):
        response = self.chain({"input_documents": self.docs, "question": self.user_question}, return_only_outputs=True)
        return response['output_text']

    def process_qa(self, user_question):
        self.user_question = user_question  # Cập nhật câu hỏi mới
        self.get_documents()  # Lấy lại tài liệu liên quan dựa trên câu hỏi mới
        return self.get_response()

# Example usage:
if __name__ == "__main__":
    pdf_path = "./data_source/dulieudulich.pdf"  # Đường dẫn tới file PDF
    initial_question = "Ẩm thực Hà Nội"  # Câu hỏi ban đầu

    processor = QaProcessor(pdf_path)
    answer = processor.process_qa(initial_question)

    print("Answer:")
    print(answer)
