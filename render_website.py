import json
import  os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

import parse_tululu_category

TEMPLATE = 'template.html'
WEBSITE_DIR = 'website'
PAGES_SUBDIR = 'pages'
BOOK_CARDS_PER_PAGE = 20
COLUMNS_PER_PAGE = 2


def render_page(
        html_template,
        book_cards,
        pages_dir,
        book_cards_per_page,
        columns_per_page,
        env,
    ):
    template = env.get_template(html_template)
    chunked_book_cards = list(chunked(book_cards, book_cards_per_page))
    pages = range(1, len(chunked_book_cards) + 1)

    for page_id, book_cards_chunk in enumerate(chunked_book_cards, 1):
        rendered_content = template.render({
            'book_cards': list(chunked(book_cards_chunk, columns_per_page)),
            'pages': pages,
            'current_page': page_id,
        })
        filepath = os.path.join(pages_dir, f'index{page_id}.html')
        with open(filepath, 'w', encoding='utf8') as file:
            file.write(rendered_content)


def main():
    pages_dir = os.path.join(WEBSITE_DIR, PAGES_SUBDIR)
    os.makedirs(pages_dir, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    book_descriptions_filepath = os.path.join(
        WEBSITE_DIR, parse_tululu_category.BOOKS_FILENAME
    )
    with open(book_descriptions_filepath, 'r') as f:
        book_descriptions = json.load(f)

    run_render = lambda: render_page(
        TEMPLATE,
        book_descriptions,
        pages_dir,
        BOOK_CARDS_PER_PAGE,
        COLUMNS_PER_PAGE,
        env,
    )

    run_render()
    server = Server()
    server.watch(TEMPLATE, run_render)
    server.serve(root=WEBSITE_DIR)

if __name__ == '__main__':
    main()
