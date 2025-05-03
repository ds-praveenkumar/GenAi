import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langchain_community.document_loaders import PyMuPDFLoader
from utils.logger import setup_logger
logger = setup_logger('HyDe')

class PDFDataLoader:
    def __init__(self, pdf_path) :
        self.pdf_path = pdf_path
        
    def load( self ):
        try:
            
            pdf_loader = PyMuPDFLoader(self.pdf_path)
            documents = pdf_loader.load()
            logger.info(f'file loaded from path: {self.pdf_path}')
            logger.info(f'total document loaded: {len(documents)}')
            return pdf_loader
        except Exception as e:
            logger.exception(e)

    
if __name__ == '__main__':
    pdf_path = 'rag/Principal-Sample-Life-Insurance-Policy.pdf'
    pdf_loader = PDFDataLoader(pdf_path)
    pdf_loader.load()
        
        