{
    'name': 'Equip',
    'version': '1.0',
'depends': [
    'stock',
    'sale_management',
],
'data': [
    'security/ir.model.access.csv',
    'views/product_template_views.xml',
    'views/stock_lot_views.xml',
    'views/installed_equipment_views.xml',
    'views/stock_picking_new_view.xml',
],
    'installable': True,
    'application': False,
}