from celery import shared_task
import fitz  # PyMuPDF
from pdfsummarizer.utils import summarize_text, generate_pdf
import os
import logging

logger = logging.getLogger(__name__)

@shared_task
def add(x, y):
    logger.debug(f"Adding {x} + {y}")
    return x + y

@shared_task
def process_pdf(pdf_path):
    logger.info(f"Starting PDF processing for: {pdf_path}")

    if not os.path.isfile(pdf_path):
        logger.error(f"PDF file does not exist: {pdf_path}")
        return

    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            logger.info(f"Opened PDF: {pdf_path}, total pages: {doc.page_count}")
            for i, page in enumerate(doc):
                page_text = page.get_text()
                if not page_text.strip():
                    logger.warning(f"No text found on page {i + 1}")
                text += page_text
            logger.debug("Extracted text from all pages.")
    except Exception as e:
        logger.exception(f"Failed to read PDF file: {e}")
        return

    try:
        logger.info("Beginning summarization of extracted text.")
        summary = summarize_text(text)
        logger.debug("Text successfully summarized.")
    except Exception as e:
        logger.exception(f"Failed to summarize text: {e}")
        return

    out_path = pdf_path.replace(".pdf", "_summary.pdf")

    try:
        logger.info(f"Generating summary PDF at: {out_path}")
        generate_pdf(summary, out_path)
        logger.info(f"PDF successfully saved as {out_path}")
    except Exception as e:
        logger.exception(f"Failed to generate or save the summary PDF: {e}")

