from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import time
from functools import lru_cache

app = Flask(__name__)

class BookScraper:
    BASE_URL = "https://z-library.sk/s/"

    def __init__(self, query=None, max_pages=5):
        self.query = query
        self.max_pages = max_pages

    def fetch_page_content(self, url, params=None):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Erro ao buscar a página: {e}")
            return None

    def parse_books_from_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        books = []
        tiles = soup.find_all('div', class_='book-item resItemBoxBooks exactMatch')

        if not tiles:
            return books

        for tile in tiles:
            try:
                title = tile.find('div', {'slot': 'title'}).text.strip() if tile.find('div', {'slot': 'title'}) else None
                author = tile.find('div', {'slot': 'author'}).text.strip() if tile.find('div', {'slot': 'author'}) else None

                z_bookcard_tag = tile.find('z-bookcard')
                year = z_bookcard_tag.get('year') if z_bookcard_tag else None
                language = z_bookcard_tag.get('language') if z_bookcard_tag else None
                publisher = z_bookcard_tag.get('publisher') if z_bookcard_tag else None
                book_url = f"https://z-library.sk{z_bookcard_tag.get('href')}" if z_bookcard_tag and z_bookcard_tag.get('href') else None

                book = {
                    'Título': title,
                    'Autor': author,
                    'Ano': year,
                    'Idioma': language,
                    'Editora': publisher,
                    'URL': book_url
                }
                books.append(book)
            except Exception as e:
                print(f"Erro ao processar um livro: {e}")

        return books

    @lru_cache(maxsize=128)
    def fetch_book_details(self, book_url):
        html = self.fetch_page_content(book_url)
        if not html:
            return {}

        soup = BeautifulSoup(html, 'html.parser')
        try:
            # Título Detalhado
            title = soup.find('h1', class_='book-title').text.strip() if soup.find('h1', class_='book-title') else None

            # Descrição
            description_box = soup.find('div', {'id': 'bookDescriptionBox'})
            description = description_box.text.strip() if description_box else None

            # Categoria
            category_box = soup.find('div', class_='property_value')
            category = category_box.text.strip() if category_box else None

            # Páginas - Pode aparecer com diferentes seletores ou atributos
            pages = None
            for property_div in soup.find_all('div', class_='bookProperty'):
                label = property_div.find('div', class_='property_label')
                if label and 'pages' in label.text.lower():
                    pages = property_div.find('span').text.strip()
                    break

            # Link para leitura online
            read_online_button = soup.find('a', class_='btn btn-primary dlButton reader-link')
            read_online_url = read_online_button['href'] if read_online_button else None

            return {
                'Título Detalhado': title,
                'Descrição': description,
                'Categoria': category,
                'Páginas': pages,
                'Leia Online': read_online_url
            }
        except Exception as e:
            print(f"Erro ao extrair detalhes do livro: {e}")
            return {}


    def scrape_books_basic(self):
        all_books = []

        for page in range(1, self.max_pages + 1):
            search_url = f"{self.BASE_URL}{self.query}?languages[]=portuguese&page={page}"
            html = self.fetch_page_content(search_url)

            if not html:
                break

            books = self.parse_books_from_page(html)

            if not books:
                break

            all_books.extend(books)

            if len(all_books) >= 12:
                return all_books[:12]

            time.sleep(1)

        return all_books

@app.route('/')
def home():
    return "Hello, World!"

# Nova rota: Dados básicos dos livros encontrados
@app.route('/busca', methods=['GET'])
def get_books_basic():
    query = request.args.get('query')
    if not query:
        return jsonify({"erro": "Parâmetro 'query' é obrigatório."}), 400

    scraper = BookScraper(query=query, max_pages=5)
    livros = scraper.scrape_books_basic()

    if livros:
        return jsonify(livros)
    else:
        return jsonify({"mensagem": "Nenhum livro encontrado."}), 404

# Nova rota: Captura dados detalhados de um único livro
@app.route('/livro', methods=['GET'])
def get_book_details():
    link = request.args.get('link')
    if not link:
        return jsonify({"erro": "Parâmetro 'link' é obrigatório."}), 400

    scraper = BookScraper()
    detalhes = scraper.fetch_book_details(link)

    if detalhes:
        return jsonify(detalhes)
    else:
        return jsonify({"mensagem": "Não foi possível capturar os detalhes do livro."}), 404

if __name__ == '__main__':
    app.run(debug=True)
