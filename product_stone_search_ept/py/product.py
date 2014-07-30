import math
import re
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime, timedelta,date

class product_extand_ept(osv.osv):
    _inherit = 'product.product'
        
    def search(self, cr, uid, args, offset=0, limit=None, order=None,context=None, count=False):
        search_name = []
        tuple_search = []
        num=1;
        certi=1;
        if context and context.get('stone_import',False):
            return super(product_extand_ept, self).search(cr, uid, args=args, offset=offset, limit=limit, order=order,
            context=context, count=count)
        for i in args:
            if i[0] == 'name':
                search_name = i[2].split()
                if search_name:
                    while num < len(search_name):
                        num = num + 1
                        tuple_search.append('|')
                    for j in search_name:
                        tuple_search.append(('name','ilike',j))
            elif i[0] == 'certificate_no':
                certi_no = i[2].split()
                if certi_no:
                    while certi < len(certi_no):
                        certi = certi + 1
                        tuple_search.append('|')
                    for j in certi_no:
                        tuple_search.append(('certificate_no','ilike',j))
            else :
                tuple_search.append(i)
        return super(product_extand_ept, self).search(cr, uid, args=tuple_search, offset=offset, limit=limit, order=order,
            context=context, count=count)

    def _get_latest_location(self,cr,uid,ids,field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        for obj in self.browse(cr,uid,ids,context=context):
            res[obj.id] = False
            move_search_ids = move_pool.search(cr,uid,[('product_id','=',obj.id),('state','=','done')],order='id desc',limit=1)
            if move_search_ids:
                move_id = move_pool.browse(cr,uid,move_search_ids[0],context=context)
                if move_id :
                    res[obj.id] = move_id.location_dest_id.id
        return res

    def _get_product(self, cr, uid, ids, context=None):
        shape_line_data = self.pool.get('shape.line').read(cr,uid,ids,['categ_id'],context=context)
        categ_ids = [x['categ_id'][0] for x in shape_line_data if x.get('categ_id')]
        product_ids = self.pool.get('product.product').search(cr,uid,[('categ_id','in',categ_ids)],context=context)
        return product_ids

    def _get_product_ids(self, cr, uid, ids, context=None):
        result = {}
        for move_line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            if move_line.state == 'done':
                result[move_line.product_id.id] = True
        return result.keys()
    
    def _get_different_price(self,cr,uid,ids,field_name, arg, context=None):
        res = {}
        for obj in self.browse(cr,uid,ids,context=context):
            if not obj.is_fancy_color:
                res[obj.id] = {'rapnet_price': 0.0,'price_caret': 0.0,'list_price': 0.0,'price_unit':0.0}
                rapnet_price = 0.0
                price_caret = 0.0
                list_price = 0.0
                if not obj.is_certified:
                    res[obj.id]['list_price'] = obj.weight * obj.ppc_non_ceritified
                    return res
                
                config_ids = self.pool.get('ir.config_parameter').search(cr,uid,[('key','=','product_rapnet_price_multiple')]);
                if config_ids:
                    parameter_obj=self.pool.get('ir.config_parameter').browse(cr,uid,config_ids[0])
                
                    if obj.shape_id:
                        cr.execute("select sale_price from shape_line where shape_id = %s and categ_id = %s"%(obj.shape_id.id,obj.categ_id.id))
                        result = cr.fetchall()
                        if result:
                            rapnet_price = float(result[0][0]) * float(parameter_obj.value)
                else:
                    rapnet_price = obj.categ_id.sale_price

                if obj.discount:
                    price_caret = rapnet_price + (rapnet_price * (obj.discount/100))
                    list_price = price_caret * obj.weight  
                else :
                    list_price = rapnet_price * obj.weight
                
                res[obj.id]['rapnet_price'] = rapnet_price
                res[obj.id]['price_caret'] = price_caret
                res[obj.id]['list_price'] = list_price
                res[obj.id]['price_unit'] = rapnet_price * obj.weight
            else:
                res[obj.id] = {'list_price': 0.0}
                list_price = obj.price_stone or 0.0
                res[obj.id]['list_price'] = list_price
                res[obj.id]['rapnet_price'] = 0.0
                res[obj.id]['price_caret'] = 0.0
                res[obj.id]['price_unit'] = 0.0
        return res    

    def _get_main_product_supplier(self, cr, uid, product, context=None):
        """Determines the main (best) product supplier for ``product``,
        returning the corresponding ``supplierinfo`` record, or False
        if none were found. The default strategy is to select the
        supplier with the highest priority (i.e. smallest sequence).

        :param browse_record product: product to supply
        :rtype: product.supplierinfo browse_record or False
        """
        sellers = [(seller_info.sequence, seller_info)
                       for seller_info in product.seller_ids or []
                       if seller_info and isinstance(seller_info.sequence, (int, long))]
        return sellers and sellers[0][1] or False

    def _calc_seller(self, cr, uid, ids, fields, arg, context=None):
        result = {}
        for product in self.browse(cr, uid, ids, context=context):
            main_supplier = self._get_main_product_supplier(cr, uid, product, context=context)
            result[product.id] = {
                'seller_info_id': main_supplier and main_supplier.id or False,
                'seller_delay': main_supplier.delay if main_supplier else 1,
                'seller_qty': main_supplier and main_supplier.qty or 0.0,
                'seller_id': main_supplier and main_supplier.name.id or False
            }
        return result 

    _columns = {
				'auction_extension_time' : fields.char('Auction Extension Time'),
                'auction_time':fields.selection([(12,12),(24,24),(36,36),(48,48),(60,60),(72,72)], 'Auction Time'),
                'auction_date':fields.datetime('Auction Date'),   
                'browness' : fields.boolean('Browness'),
                'certificate_no' : fields.char('CERTIFICATE#', help="Certificate No."),
                'clarity_id' : fields.many2one('product.clarity', "Clarity", ondelete='restrict', help="Clarity"),
                'color_id' : fields.many2one('product.color', "CLR", ondelete='restrict', help="Color"),
                'cut_id' : fields.many2one('product.cut', "Cut", ondelete='restrict', help="Cut"),
                'culet_condition' : fields.many2one('product.culet_condition', 'Culet Condition', ondelete='restrict'),
                'culet_id' : fields.many2one('product.culet', 'Culet Size', ondelete='restrict'),
                'crown_height' : fields.float('Crown Height'),
                'crown_angle' : fields.float('Crown Angle'),                
                'cost_price_discount' : fields.float('Cost Price Discount'),
                'diameter' : fields.char('Diameter', size=128),
                'discount':fields.float('BACK', help="Discount"),
                'eye_clean' : fields.char('Eye clean', size=128),
                'fancy_color_id' : fields.many2one('product.fancy.color', 'Fancy Color', ondelete='restrict'),
                'fancy_color_intensity' : fields.many2one('product.fancy.color.intensity' ,'Fancy Color Intensity', ondelete='restrict'),
                'fancy_color_overtone' : fields.many2one('product.fancy.color.overtone', 'Fancy Color Overtone', ondelete='restrict'),                                
                'fluorescence_color_id' : fields.many2one('product.fluorescence.color', 'Fluorescence Color', ondelete='restrict',  help="Fluorescence Color"),
                'fluorescence_intensity_id' : fields.many2one('product.fluorescence.intensity', 'Fluorescence Intensity', ondelete='restrict',  help="Fluorescence Intensity"),
                #'gridle_thin_id' : fields.many2one('product.gridle_thin', 'Girdle Thin', ondelete='restrict'),
                #'gridle_thick_id' : fields.many2one('product.gridle_thick', 'Girdle Thick', ondelete='restrict'),
                'girdle_id' : fields.many2one('product.gridle','Girdle', ondelete='restrict'),
                'girdle_percentage' : fields.float('Girdle %'),
                'girdle_condition' : fields.char('Girdle Condition', size=128),
                'hna' : fields.char('HNA', size=128),                
                'insure_id' : fields.many2one('product.insure', 'Insured By', ondelete='restrict'),
                'is_certified':fields.boolean('Certified'),
                'is_export':fields.boolean('Exportable'),                 
                'is_fancy_color' : fields.boolean('Is fancy color ?'),
                'is_auction':fields.boolean('Is Auction ?'),
                'lab_id': fields.many2one('product.lab', 'Lab', ondelete='restrict', help="Lab"),
                'laser_inspection' : fields.boolean('Laser Inscription', help="Laser Inscription"),
                'lower_half':fields.char('Lower Half'),
                'milky' : fields.char('Milky', size=128),
                'natts' : fields.boolean('Natts'),                
                'ppc_non_ceritified':fields.float(digits_compute=dp.get_precision('Product Price'),string="Non Certified PPC"),
                'price_stone' : fields.float('Price',digits_compute=dp.get_precision('Product Price')),#when is_fancy True
                'polish_id' : fields.many2one('product.polish', "Polish", ondelete='restrict', help="Polish"),                
                'product_length' : fields.float('Length', help="Length"),
                'product_width' : fields.float('Width', help="Width"),
                'product_height' : fields.float('Height',  help="Height"),
                'product_table' : fields.float('Table %'),
                'pavilion_depth' : fields.float('Pavilion Depth'),
                'pavilion_height' : fields.float('Pavilion Angle'),                
                'product_status' : fields.selection([('available','Available'),
                                            ('hold','Hold'),
                                            ('sold','Sold'),
                                            ('on_approval','On Approval'),
                                            ('on_consignment','On Consignment'),
                                            ('offline','Offline'),
                                            ('repair','Repair'),
                                            ('web_sale','Web Sale')], string='Status'),
                'product_depth' : fields.float('Depth'),
                'rfid_tag' : fields.char('RFID Tag', size=128),
                'rough_origin' : fields.char('Rough Origin', size=256),
                'star_length':fields.char('Star Length'),                
                'seller_id': fields.function(_calc_seller, type='many2one', relation="res.partner", string='Main Supplier', help="Main Supplier who has highest priority in Supplier List.", multi="seller_info", store=True),                
                'shape_id' : fields.many2one('product.shape', 'Shape', ondelete='restrict', help="Shape"),
                'symmetry_id' : fields.many2one('product.symmetry', 'Symmetry', ondelete='restrict', help="Symmetry"),
                'shade' : fields.char('Shade', size=128),
                'tinge' : fields.char('Tinge', size=128),
                'treatment' : fields.char('Treatment', size=128),
                'table_inc' : fields.char('Table Inc.', size=128),
                'weight' : fields.float('CRT',digits_compute=dp.get_precision('Stock Weight'), help="Weight"),                
                
                'rapnet_price':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="RAPNET",help="This is price which is defined in product's selected category",
                                               store={
                                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','is_certified','ppc_non_ceritified','is_fancy_color'], 10),
                                                    'shape.line': (_get_product, ['sale_price'],10),},
                                               ),
                'price_caret':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="PPC",help="Price/Caret",
                                              store={
                                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','is_certified','ppc_non_ceritified','is_fancy_color'], 10), 
                                                    'shape.line': (_get_product, ['sale_price'], 10),},
                                               ),
                'list_price':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="Total Price",help="Price/Caret * Weight",
                                              store={
                                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','weight','is_certified','ppc_non_ceritified','is_fancy_color'],10),
                                                    'shape.line': (_get_product, ['sale_price'],10),},
                                               ),
                'price_unit':fields.function(_get_different_price,type='float',multi='sums',digits_compute=dp.get_precision('Product Price'),string="PRICE",
                              store={
                                    'product.product': (lambda self, cr, uid, ids, c={}: ids, ['categ_id','discount','weight','is_certified','ppc_non_ceritified','is_fancy_color'],10),
                                    'shape.line': (_get_product, ['sale_price'],10),},
                                            ),
                'location_id' : fields.function(_get_latest_location,type='many2one',string='Location',relation='stock.location',
                                store={
                                       'stock.production.lot': (lambda self, cr, uid, ids, c={}: ids, ['move_ids'],10),
                                       'stock.move':(_get_product_ids,['location_dest_id','state','product_id'],10),
                                       }                                                       
                                               ),
                }
       
    _sql_constraints = [
        ('default_code_unique', 'unique(default_code)', 'Internal Reference must be unique'),
        ('rfid_tag_unique','unique(rfid_tag)','RFID Tag must be unique!!!'),
    ]
    
    def is_certified_checked(self, cr, uid, ids, is_certified):
        '''
            Called from onchange of form view
        '''
        if is_certified:
            return {'value':{'is_export':True}}
        return {'value':{'is_export':False}}    
        
