import json
import  os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

import parse_tululu_category

TEMPLATE = 'template.html'
PAGE_NAME = 'index'
DIR_NAME = 'pages'


def render_page(html_template, page_name, books, dir_name, env):
    template = env.get_template(html_template)
    for i, books_chunk in enumerate(chunked(books, 20), 1):
        rendered_content = template.render({'books': chunked(books_chunk, 2)})
        filename = os.path.join(dir_name, f'{page_name}{i}.html')
        with open(filename, 'w', encoding="utf8") as file:
            file.write(rendered_content)


def main():
    os.makedirs(DIR_NAME, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open(parse_tululu_category.BOOKS_FILENAME, 'r') as f:
        books = json.load(f)

    render_page(TEMPLATE, PAGE_NAME, books, DIR_NAME, env)
    server = Server()
    server.watch(
        TEMPLATE, 
        lambda: render_page(
            TEMPLATE, PAGE_NAME, {'books': books}, DIR_NAME, env
        )
    )
    server.serve(root='.')

if __name__ == '__main__':
    main()
