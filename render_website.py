import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import parse_tululu_category


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

    render_page('template.html', 'index.html', {'books': books}, env)

    server = HTTPServer(('127.0.0.1', 8080), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
