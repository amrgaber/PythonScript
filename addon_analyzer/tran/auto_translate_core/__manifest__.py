{
    'name': 'Auto Translate Core',
    'version': '1.0',
    'category': 'Localization',
    'summary': 'Core translation services',
    'description': """
        This module provides core functionality for automatic translation services.
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['base'],
    'data': [
        'views/res_config_settings.xml',
    ],
    'external_dependencies': {
        'python': ['polib', 'deep_translator'],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}