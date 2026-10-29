"""Tokenizer for mail templates (ready to use, nothing to edit).

A template mixes text with two kinds of tags, like the Odoo / Jinja templates:
  * expressions:  {{ lead.contact }}
  * statements:   {% if ... %} ... {% else %} ... {% endif %}
                  {% for ... %} ... {% endfor %}

template_tokens() keeps only what matters to check the structure, in order:
  "{{" and "}}" for the expression delimiters,
  "if", "else", "endif", "for", "endfor" (or any other keyword) for the statements.

>>> list(template_tokens("Hi {{ name }}{% if vip %}!{% endif %}"))
['{{', '}}', 'if', 'endif']
"""

import re
from collections.abc import Iterator

_TOKEN = re.compile(r"\{\{|\}\}|\{%\s*(\w+)[^%]*%\}")


def template_tokens(template: str) -> Iterator[str]:
    for match in _TOKEN.finditer(template):
        yield match.group(1) or match.group(0)
