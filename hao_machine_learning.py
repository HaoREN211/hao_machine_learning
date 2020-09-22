# -*- coding: UTF-8 -*-
# 作者：hao.ren3
# 时间：2019/12/21 8:22
# IDE：PyCharm

from flask import send_from_directory
from app import create_app, db
from os.path import join

app = create_app()

# 为网站添加图标
def favicon():
    return send_from_directory(join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
app.add_url_rule('/favicon.ico',view_func=favicon)

@app.shell_context_processor
def make_shell_context():
    return {'db': db}

@app.template_filter('md')
def markdown_html(txt):
    from markdown import markdown
    post_content_html = markdown(txt, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.fenced_code',
        'markdown.extensions.admonition',
        'markdown.extensions.codehilite',
        'markdown.extensions.meta',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.smarty',
        'markdown.extensions.toc',
        'markdown.extensions.wikilinks',
        'markdown.extensions.tables'
    ])
    return post_content_html

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003, debug = True)