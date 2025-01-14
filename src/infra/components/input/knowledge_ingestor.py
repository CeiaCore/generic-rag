import mammoth
import markdownify
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

# pip install mammoth markdownify pdfplumber langchain

class KnowledgeIngestor:
    def __init__(self):
        print("KnowledgeIngestor initialized")

    @staticmethod
    def get_pages_pdfplumber(pdf_path):
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    pages.append({
                        "text": text,
                        "page": i,
                        "source": pdf_path
                    })
        return pages
    
    @staticmethod
    def get_text_mammoth(doc_path):
        """
        Retorna o texto de um arquivo DOCX utilizando a biblioteca Mammoth.
        """
        try:
            with open(doc_path, "rb") as doc_file:
                result = mammoth.convert_to_html(doc_file)

                html = result.value
                md = markdownify.markdownify(html, heading_style="ATX")

                return md
        except Exception as e:
            print(f"Erro ao ler o arquivo {doc_path}: {e}")
            return ""
        
    @staticmethod
    def recursively_split(text, chunk_size=1024, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        texts = text_splitter.split_text(text)

        return texts
    
    def get_chunks_pdf(self, file_path, chunk_size = 1024, chunk_overlap = 200):
        pages = self.get_pages_pdfplumber(file_path)
        chunks = []
        for page in pages:
            page_chunks = self.recursively_split(page["text"], chunk_size, chunk_overlap)
            for chunk in page_chunks:
                chunks.append({
                    "content": chunk,
                    "page": page["page"],
                    "source": file_path,
                    "source_type": "pdf"
                })
        return chunks
    
    @staticmethod
    def get_chunk_context(chunks_content, i, n):
        """
            Retorna o contexto, sendo n chunks anteriores, o próprio chunk, n chunks posteriores.
        """
        if not chunks_content or i < 0 or i >= len(chunks_content):
            return []
        
        start = max(0, i - n)
        end = min(len(chunks_content), i + n + 1)

        chunks_list = chunks_content[start:end]

        context = "\n".join(chunks_list)
        
        return context


    def get_chunks_docx(self, file_path, chunk_size = 1024, chunk_overlap = 200):
        text = self.get_text_mammoth(file_path)
        chunks_content = self.recursively_split(text, chunk_size, chunk_overlap)
        chunks_to_get_context = self.recursively_split(text, chunk_size, 0)
        chunks = []

        for idx, chunk in enumerate(chunks_content):
            context = self.get_chunk_context(chunks_to_get_context, idx, 3)

            chunks.append({
                "content": chunk,
                "context": context,
                "source": file_path,
                "source_type": "docx",
            })
        
        return chunks
