from bs4 import BeautifulSoup

from docx import Document

import requests

def fetch_and_translate(url):

  # Baixar e traduzir conteúdo de uma página web

  response = requests.get(url)

  soup = BeautifulSoup(response.text, 'html.parser')

  text = "\n".join([p.get_text() for p in soup.find_all('p')])

  translated_text = translator_text(text, language_destination)

  doc = Document()

  doc.add_paragraph(translated_text)

  doc.save("translated_webpage.docx")
