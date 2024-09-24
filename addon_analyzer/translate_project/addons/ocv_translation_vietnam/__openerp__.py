{
    'name': 'Vietnam Translation for Odoo 9',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': '',
    'description': """
Translate to Vietnamese
    """,
    'author': 'ducthangict.dhtn@gmail.com',
    'price': '0',
    'currency': 'USD',
    'depends': ['sale', 'purchase', 'stock'],
    'data': [
        'translate_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
