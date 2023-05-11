import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell

import parse_tululu_category

TEMPLATE = 'template.html'
PAGE_NAME = 'index'


def render_page(html_template, page, context, env):
    template = env.get_template(html_template)
    rendered_content = template.render(**context)
    with open(page, 'w', encoding="utf8") as file:
        file.write(rendered_content)


def main():

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    with open(parse_tululu_category.BOOKS_FILENAME, 'r') as f:
        books = json.load(f)

    render_page(TEMPLATE, PAGE_NAME, {'books': books}, env)
    server = Server()
    server.watch(
        TEMPLATE, 
        lambda: render_page(TEMPLATE, PAGE_NAME, {'books': books}, env),
    )

    server.serve(root='.')

if __name__ == '__main__':
    main()
