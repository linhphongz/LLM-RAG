from IPython.display import Markdown
import textwrap
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv
import google.generativeai as genai
class QASystem:
    def __init__(self, google_api_key):
        self.google_api_key = google_api_key
        self.model = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=google_api_key,
            temperature=0.2,
            convert_system_message_to_human=True
        )
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.new_db = FAISS.load_local("faiss_index", self.embeddings, allow_dangerous_deserialization=True)
        self.qa_chain = None  # We'll initialize this later

    def initialize_qa_chain(self):
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.model,
            chain_type='stuff',
            retriever=self.new_db.as_retriever(search_kwargs={"k": 1}),
            return_source_documents=True
        )

    def answer_question(self, question):
        if not self.qa_chain:
            self.initialize_qa_chain()
        # Perform question answering logic here
        answer = self.qa_chain.invoke(question)["result"]
        return answer

    def format_answer(self, answer):
        formatted_answer = answer.replace('•', '  *')
        return Markdown(textwrap.indent(formatted_answer, '> ', predicate=lambda _: True))


