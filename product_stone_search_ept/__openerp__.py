
{
    'name': 'Product Extended',
    'version': '1.0',
    'category': 'Product Extension',
    'sequence': 14,
    'complexity': "normal",
    'description': """
    Product Screen extended and product advance search filter added
    """,
    'author': 'Emipro Technologies',
    'website': 'http://www.emiprotechnologies.com',
    'images': [],
    'depends': ['stock','sale_stock'],
    'init_xml': [],
    'update_xml': [
                   'view/misc_view.xml',
                   'view/misc_menu_view.xml',
                   'security/ir.model.access.csv',
                   'view/product_extended.xml',
                   'view/product_search_view.xml',
                   'view/shape_line_view.xml',
                   'wizard/auction_view_ept.xml',
                   #'view/product_category_view.xml',
                   #'view/config_parameter_ept.xml',
                   ],
    'demo_xml': [],
    'data' : [
              'data/misc_data.xml',
               ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
