import requests
import logging
from decouple import config
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

logger = logging.getLogger(__name__)
GROQ_API_KEY = config('GROQ_API_KEY')

def summarize_text(text):
    endpoint = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Summarize the following text clearly and concisely:\n\n{text[:4000]}"  # Limit for safety

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert in document summarization. Your task is to extract all relevant information from the provided text and generate a concise, accurate summary. The output should be brief, clear, and formatted as follows:\n\nTitle: <Insert the title of the document>\nSummary: <Insert a concise summary capturing the key points of the document>\n\nEnsure the summary reflects the main purpose, key arguments, and essential details without unnecessary elaboration."
            },
            {   "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.8,
        "max_tokens": 3000
    }

    logger.info("Sending request to Groq completion API for text summarization...")
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        logger.info(f"Received response from Groq API. Status: {response.status_code}")
    except requests.exceptions.Timeout:
        logger.error("Request to Groq API timed out.")
        raise
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}; Response Text: {response.text}")
        raise
    except Exception as err:
        logger.exception(f"Unexpected error during Groq API call: {err}")
        raise

    try:
        data = response.json()
        summary_text = data['choices'][0]['message']['content']
        logger.debug("Successfully extracted summary from Groq API response.")
        return summary_text
    except (KeyError, ValueError) as e:
        logger.error(f"Malformed response from Groq API: {e} | Response: {response.text}")
        raise


def generate_pdf(text, output_path):
    logger.info("Starting PDF generation: %s", output_path)
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    margin = 0.5 * inch
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin
    y = height - margin

    font_name = "Helvetica"
    font_size = 12
    c.setFont(font_name, font_size)
    line_spacing = font_size + 4

    # Draw border
    c.rect(margin, margin, usable_width, usable_height)
    logger.debug("Border drawn on first page.")

    words = text.split()
    line = ""

    page_number = 1
    lines_written = 0

    for word in words:
        test_line = line + word + " "
        if c.stringWidth(test_line, font_name, font_size) < usable_width:
            line = test_line
        else:
            y -= line_spacing
            if y < margin + line_spacing:
                c.showPage()
                c.rect(margin, margin, usable_width, usable_height)
                c.setFont(font_name, font_size)
                y = height - margin - line_spacing
                page_number += 1
                logger.info("Started new page %d.", page_number)
            c.drawString(margin + 5, y, line.strip())
            lines_written += 1
            line = word + " "
    if line:
        y -= line_spacing
        if y < margin + line_spacing:
            c.showPage()
            c.rect(margin, margin, usable_width, usable_height)
            c.setFont(font_name, font_size)
            y = height - margin - line_spacing
            page_number += 1
            logger.info("Started new page %d.", page_number)
        c.drawString(margin + 5, y, line.strip())
        lines_written += 1

    c.save()
    logger.info("PDF generation complete. Total lines: %d. Total pages: %d.", lines_written, page_number)
    logger.debug("Saved PDF to %s", output_path)

