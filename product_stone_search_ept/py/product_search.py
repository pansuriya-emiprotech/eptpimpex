import math
import re
from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp import models, api, _

class product_search_ept(osv.osv_memory):
    _name = 'product.search'
    
    def product_shape_change(self,cr, uid, ids, check, context={}):
        shape_ids = self.pool.get('product.shape').search(cr,uid,[])
        val = {}
        if shape_ids :
            for id in shape_ids :
                key = 'product_shape%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product_color_change(self,cr, uid, ids, check, context={}):
        color_ids = self.pool.get('product.color').search(cr,uid,[])
        val = {}
        if color_ids :
            for id in color_ids :
                key = 'product_color%s'%id
                val.update({key:check})
        return {'value':val}
       
    def product_fancy_color_change(self,cr, uid, ids, check, context={}):
        fancy_color_ids = self.pool.get('product.fancy.color').search(cr,uid,[])
        val = {}
        if fancy_color_ids :
            for id in fancy_color_ids :
                key = 'product_fancy_color%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product1_fancy_color_intensity_change(self,cr, uid, ids, check, context={}):
        fancy_color_intensity_ids = self.pool.get('product.fancy.color.intensity').search(cr,uid,[])
        val = {}
        if fancy_color_intensity_ids :
            for id in fancy_color_intensity_ids :
                key = 'product1_fancy_color_intensity%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product2_fancy_color_overtone_change(self,cr, uid, ids, check, context={}):
        fancy_color_overtone_ids = self.pool.get('product.fancy.color.overtone').search(cr,uid,[])
        val = {}
        if fancy_color_overtone_ids :
            for id in fancy_color_overtone_ids :
                key = 'product2_fancy_color_overtone%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product_clarity_change(self,cr, uid, ids, check, context={}):
        clarity_ids = self.pool.get('product.clarity').search(cr,uid,[])
        val = {}
        if clarity_ids :
            for id in clarity_ids :
                key = 'product_clarity%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product_cut_change(self,cr, uid, ids, check, context={}):
        cut_ids = self.pool.get('product.cut').search(cr,uid,[])
        val = {}
        if cut_ids :
            for id in cut_ids :
                key = 'product_cut%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product_polish_change(self,cr, uid, ids, check, context={}):
        polish_ids = self.pool.get('product.polish').search(cr,uid,[])
        val = {}
        if polish_ids :
            for id in polish_ids :
                key = 'product_polish%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product_symmetry_change(self,cr, uid, ids, check, context={}):
        symmetry_ids = self.pool.get('product.symmetry').search(cr,uid,[])
        val = {}
        if symmetry_ids :
            for id in symmetry_ids :
                key = 'product_symmetry%s'%id
                val.update({key:check})
        return {'value':val}   
    
    def product_fluorescence_intensity_change(self,cr, uid, ids, check, context={}):
        fluorescence_intensity_ids = self.pool.get('product.fluorescence.intensity').search(cr,uid,[])
        val = {}
        if fluorescence_intensity_ids :
            for id in fluorescence_intensity_ids :
                key = 'product_fluorescence_intensity%s'%id
                val.update({key:check})
        return {'value':val}
      
    def product_lab_change(self, cr, uid, ids,check, context={}):
        lab_ids = self.pool.get('product.lab').search(cr,uid,[])
        val = {}
        if lab_ids :
            for id in lab_ids :
                key = 'product_lab%s'%id
                val.update({key:check})
        return {'value':val}    
    
    def default_get(self, cr, uid, fields, context=None):
        res = super(product_search_ept, self).default_get(cr, uid, fields, context=context)  
        if 'product_status_available' in fields: res['product_status_available'] = True
        if 'product_status_hold' in fields : res['product_status_hold'] = True
        if 'product_status_on_approval' in  fields: res['product_status_on_approval'] = True
        return res
            
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        result = super(product_search_ept, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar,submenu)
        if context is None:
            context={}
        self._columns = {}
        self._columns['product_ids'] = fields.text('Product IDS')
        if view_type != 'form':
            return result
        _moves_arch_lst = """
            <form string="Stone Search" version="7.0">
                  <div>
        """
        #_moves_arch_lst += """<group colspan="4" col="10">"""
        _line_fields = result['fields']
        info = [
                    #{'model':None,'_column_name':'product_name','label':'Stone ID','type':'char','name':'name','product_search_type':'char'},
                    #{'model':None,'_column_name':'product_certificate_no','label':'Certificate No.','type':'char','name':'certificate_no','product_search_type':'char'},
#                     {'model':None,'_column_name':'product_weight','label':'Weight','no':3,'type':'float','name':'weight','product_search_type':'char','range':True},
#                     {'model':None,'_column_name':'product_price_caret','label':'PPC','no':1,'type':'float','name':'price_caret','product_search_type':'char','range':True},
#                     {'model':None,'_column_name':'product_discount','label':'Back%','no':1,'type':'float','name':'discount','product_search_type':'char','range':True},
#                     {'model':'product.shape','width':'15%','_column_name':'product_shape','label':'SHP','help':'Shape','type':'many2one','name':'shape_id','product_search_type':'boolean','on_change':'product_shape_change'}, 
#                     {'model':'product.color','width':'8%','_column_name':'product_color','label':'CLR','help':'Color','type':'many2one','name':'color_id','product_search_type':'boolean','on_change':'product_color_change'},
#                     {'model':'product.clarity','width':'10%','_column_name':'product_clarity','label':'CLRTY','help':'Clarity','type':'many2one','name':'clarity_id','product_search_type':'boolean','on_change':'product_clarity_change'},
#                     {'model':'product.cut','width':'12%','_column_name':'product_cut','label':'CUT','help':'Cut','type':'many2one','name':'cut_id','product_search_type':'boolean','on_change':'product_cut_change'},
#                     {'model':'product.polish','width':'8%','_column_name':'product_polish','label':'POL','help':'Polish','type':'many2one','name':'polish_id','product_search_type':'boolean','on_change':'product_polish_change'},
#                     {'model':'product.symmetry','width':'10%','_column_name':'product_symmetry','label':'SYM','help':'Symmetry','type':'many2one','name':'symmetry_id','product_search_type':'boolean','on_change':'product_symmetry_change'},
#                     {'model':'product.fluorescence.intensity','width':'13%','_column_name':'product_fluorescence_intensity','label':'FLUR','help':'Fluorescence Intensity','type':'many2one','name':'fluorescence_intensity_id','product_search_type':'boolean','on_change':'product_fluorescence_intensity_change'},
                     {'model':'product.lab','width':'8%','_column_name':'product_lab','label':'LAB','help':'Lab','type':'many2one','name':'lab_id','product_search_type':'boolean','on_change':'product_lab_change'},
#                     {'model':'product.fancy.color','width':'15%','_column_name':'product_fancy_color','label':'FNC CLR','help':'Fancy Color','type':'many2one','name':'fancy_color_id','product_search_type':'boolean','on_change':'product_fancy_color_change'},
#                     {'model':'product.fancy.color.intensity','width':'15%','_column_name':'product1_fancy_color_intensity','label':'FNC CLR INT','help':'Fancy Color Intensity','type':'many2one','name':'fancy_color_intensity','product_search_type':'boolean','on_change':'product1_fancy_color_intensity_change'},
#                     {'model':'product.fancy.color.overtone','width':'15%','_column_name':'product2_fancy_color_overtone','label':'FNC CLR OVR','help':'Fancy Color Overtone','type':'many2one','name':'fancy_color_overtone','product_search_type':'boolean','on_change':'product2_fancy_color_overtone_change'},
#                     {'model':None,'_column_name':'product_status','width':'20%','label':'Status','type':'selection','name':'product_status','product_search_type':'boolean'
#                               ,'selection_val':[('available','Available'),
#                                                 ('hold','Hold'),
#                                                 ('sold','Sold'),
#                                                 ('on_approval','On Approval'),
#                                                 ('on_consignment','On Consignment'),
#                                                 ('offline','Offline'),
#                                                 ('repair','Repair'),
#                                                 ('web_sale','Web Sale')]},
#                     {'model':'stock.location','_column_name':'stock_location','width':'15%','help':'Location','label':'Location','type':'many2one','name':'location_id','product_search_type':'boolean'
#                                     ,'domain':[('usage','=','internal')],},
                ]

        for model_info in info :        
            if model_info['type'] == 'many2one' and model_info['product_search_type'] == 'boolean' :
                if model_info['model']:
                    ids = self.pool.get(model_info['model']).search(cr,uid,model_info.get('domain',[]))
                    if ids :
                        _moves_arch_lst += """<div style="float:left;width:%s;">"""%(model_info.get('width', '100%'))
                        if model_info.get('label', False)=='Location':
                            _moves_arch_lst += """<u><label style="color:rgb(124,123,173);font-weight:bold;" string="%s" help="%s"/></u>"""%(model_info['label'],model_info['help'])
                        if model_info.get('on_change', False):
                            ''' Check box for Select All '''
                            _moves_arch_lst += """<div><field name="%s" class="oe_inline" nolabel="1" on_change="product_lab_change(product_lab_change)" modifiers="{}"/>
                                                        """%(model_info['on_change'])
                            ''' Label for Select All '''                  
                            _moves_arch_lst += """<u><label style="color:rgb(124, 123, 173);" string="%s" for="%s" /></u></div>"""%(model_info['label'],model_info['label']) 
                            _line_fields.update({
                             '%s'%(model_info['on_change']) : {
                                 'string': 'All ?',
                                 'type' : 'boolean',
                                 'help' : '%s'%(model_info['help']),
                                 
                            },})  
                            self._columns['%s'%(model_info['on_change'])] = fields.boolean(model_info['on_change'])                
                        for obj in self.pool.get(model_info['model']).browse(cr,uid,ids,context=context):
                            name=len(obj.name) > 7 and (obj.name[:7]+'...') or obj.name[:7]
                            _line_fields.update({
                             '%s%s'%(model_info['_column_name'],obj.id) : {
                                 'string': obj.name,
                                 'type' : 'boolean',
                                 'help' : '%s'%(obj.name)
                             },})
                            self._columns['%s%s'%(model_info['_column_name'],obj.id)] = fields.boolean(obj.name)
                        
                            ''' Check box and related label '''
                            _moves_arch_lst += """
                                 <div><field name="%s%s" class="oe_inline" nolabel="1"/>
                                 <label string="%s" for="%s%s" /></div>
                                 """%(model_info['_column_name'],obj.id,name,model_info['_column_name'],obj.id)

                        _moves_arch_lst += """</div>"""           
#######################            
            if model_info['type'] == 'char' and model_info['product_search_type'] == 'char':
                _moves_arch_lst += """<div style="width:%s;float:left;">""" %('50%')
                _line_fields.update({
                             '%s'%(model_info['_column_name']) : {
                                 'string': 'Name',
                                 'type' : 'char',
                                 'help' : '%s'%(model_info['_column_name']),
                             },})
                self._columns['%s'%(model_info['_column_name'])] = fields.char(model_info['label'],size=1024)
                _moves_arch_lst += """
                                <div>
                                    <label style="color:rgb(124, 123, 173);" string="%s" for="%s" />
                                    <field name="%s" style="width: 70%%"  nolabel="1"/>
                                </div>
                                </div>
                                 """%(model_info['label'],model_info['_column_name'],model_info['_column_name'])
  
################################
            if model_info['type'] == 'selection' and model_info['product_search_type'] == 'boolean' :
                if model_info['selection_val']:
                    _moves_arch_lst += """<div style="float:left;width:%s">"""%(model_info['width'])
                    _moves_arch_lst += """<u><label style="color:rgb(124, 123, 173);font-weight:bold;" string="%s" /></u><newline/>"""%(model_info['label'])
                    for value in model_info['selection_val']:
                        _line_fields.update({
                         '%s_%s'%(model_info['_column_name'],value[0]) : {
                             'string': value[1],
                             'type' : 'boolean',
                         },})
                        self._columns['%s_%s'%(model_info['_column_name'],value[0])] = fields.boolean(value[1])
                        _moves_arch_lst += """
                             <div><field name="%s_%s" nolabel="1"/>
                             <label string="%s" for="%s_%s" /></div>
                             """%(model_info['_column_name'],value[0],value[1],model_info['_column_name'],value[0])
                    _moves_arch_lst +="""</div>"""
###########################                        
            if model_info.get('range') and model_info['range']:
                width = '50%'
                if model_info.get('no') > 1:width = '100%'
                _moves_arch_lst += """<div style="float:left;width:%s;">"""%(width)
                _moves_arch_lst += """<div style="float:left;width:%s;"><label style="color:rgb(124, 123, 173);font-weight:bold;" string="%s" /></div>"""%('15%',model_info['label'])
                if model_info.get('no'):
                    no = model_info.get('no')
                    wid = str(85/int(no)) + '%'
                    while no != 0 :
                         
                        no = no - 1
                        _line_fields.update({'%s_from_%s'%(model_info['_column_name'],no) : {'string': model_info['label'],'type':'float'}})
                        _line_fields.update({'%s_to_%s'%(model_info['_column_name'],no) : {'string': model_info['label'],'type':'float'}})
                        self._columns['%s_from_%s'%(model_info['_column_name'],no)] = fields.float(model_info['label'],digits=(16,2))
                        self._columns['%s_to_%s'%(model_info['_column_name'],no)] = fields.float(model_info['label'],digits=(16,2))
                        _moves_arch_lst += """
                                        <div style="float:left;width:%s;"> 
                                             <div style="float:left;"><field name="%s_from_%s" placeholder="From" class="oe_inline" nolabel="1"/></div>
                                             <div style="float:left;"><b><label style="color:rgb(124, 123, 173);" string="--" /></b></div>
                                             <div style="float:left;"><field name="%s_to_%s" placeholder="To" class="oe_inline" nolabel="1"/></div>
                                        </div> 
                                     """%(wid,model_info['_column_name'],no,model_info['_column_name'],no)
                _moves_arch_lst += """</div>"""
#<div style="float:left;font-size:20px;margin-right:3px"><b><label style="color:rgb(124, 123, 173);" string="[" /></b></div>
#<div style="float:left;font-size:20px;margin-left:3px;"><b><label style="color:rgb(124, 123, 173);" string="]" /></b></div>                         
        _moves_arch_lst += """ 
                            </div>
                          <footer>
                          <button name="get_product" string="Search" type="object" colspan="2" class="oe_highlight"/>
                             or
                         <button string="Cancel" class="oe_link" special="cancel"/>
                          </footer>
                          </form>
                 """

        result['arch'] = _moves_arch_lst
        result['arch'] = result['arch'].replace('&','&amp;')
        result['fields'] = _line_fields
        return result       
    
    _columns = {
                'product_ids' : fields.text('Product IDS'),
                }
    def create(self, cr, uid, vals, context=None):
        search_domain = []
        
        def make_search(model,column,inner_type,model_type,no=1,range=False, single=False):
            if inner_type == 'selection' and model_type == 'boolean' :
                fields = [x for x in self._columns.keys() if x.find(model) >= 0]
                v = []
                for f in fields :
                    if vals[f] :
                        v.append(f.replace(str(column)+'_',''))
                if v :
                    search_domain.append((column, 'in', v))                
            if inner_type == 'many2one' and model_type == 'boolean':
                fields = [x for x in self._columns.keys() if x.find(model) >= 0 and not '_change' in x]
                ids = []
                for f in fields :
                    if vals[f]:
                        id = f.replace(model,'')
                        ids.append(int(id))
                if ids:
                    search_domain.append((column, 'in', ids)) 
            if inner_type == 'char' and model_type == 'char':
                fields = [x for x in self._columns.keys() if x.find(model) >= 0]
                for f in fields:
                    if vals[f]:
                        search_domain.append((column, 'ilike', vals[f]))
            if inner_type == 'many2one' and model_type == 'selection':
                fields = [x for x in self._columns.keys() if x.find(model) >= 0]
                for f in fields :
                    if vals[f]:
                        search_domain.append((column, '=', vals[f]))
            if single:
                from_val = 0.0
                to_val = 0.0
                fields = [x for x in self._columns.keys() if x.find(model) >= 0]
                for f in fields :
                    if f == model + '_from' and vals[f] > 0.0 :
                        from_val = vals[f]
                        search_domain.append((column, '>=', vals[f]))
                    if f == model + '_to' and vals[f] > 0.0 :
                        to_val = vals[f] 
                        search_domain.append((column, '<=', vals[f]))
                if from_val > to_val :
                    raise osv.except_osv(_('Error!'), _('%s From value always be less then To Value !!')%(column.capitalize()))
            
            if range :
                orr = 0
                fields = [x for x in self._columns.keys() if x.find(model) >= 0]
                #for f in fields:
# ####                    
                  #  if 'from' in f:
                  #      if vals.get(f,False):
                   #          orr = orr + 1
####            
                orr=no            
                if orr > 1:
                    while orr != 0:
                        orr-=1
                        search_domain.append(('|'))
                tmp = no    
                while tmp != 0:
                    tmp-=1
                    from_val = 0.0
                    to_val = 0.0
                    for f in fields:
                        if str(tmp) in f:
                            if model + '_from' in f:
                                search_domain.append(('&'))
                                search_domain.append((column, '>=', vals[f]))
                                from_val = vals[f]
                                break;
                    for f in fields:
                        if str(tmp) in f:
                            if model + '_to' in f:
                                search_domain.append((column, '<=', vals[f]))
                                to_val = vals[f]
                                break;
                    if from_val > to_val :
                        raise osv.except_osv(_('Error!'), _('%s From value always be less then To Value !!')%(column.capitalize()))
            return True
        info = [
                {'model':None,'_column_name':'product_name','label':'Stone ID','type':'char','name':'name','product_search_type':'char'},
                {'model':None,'_column_name':'product_certificate_no','label':'Certificate No.','type':'char','name':'certificate_no','product_search_type':'char'},
                {'model':None,'_column_name':'product_weight','no':3,'label':'Weight','type':'float','name':'weight','product_search_type':'char','range':True},
                {'model':None,'_column_name':'product_price_caret','label':'PPC','no':1,'type':'float','name':'price_caret','product_search_type':'char','single':True},
                {'model':None,'_column_name':'product_discount','label':'Discount','no':1,'type':'float','name':'discount','product_search_type':'char','single':True},
                {'model':'product.shape','_column_name':'product_shape','label':'Shape','type':'many2one','name':'shape_id','product_search_type':'boolean'},
                {'model':'product.color','_column_name':'product_color','label':'Color','type':'many2one','name':'color_id','product_search_type':'boolean'},
                {'model':'product.fancy.color','_column_name':'product_fancy_color','label':'Fancy Color','type':'many2one','name':'fancy_color_id','product_search_type':'boolean'},
                {'model':'product.fancy.color.intensity','_column_name':'product1_fancy_color_intensity','label':'Fancy Color Intensity','type':'many2one','name':'fancy_color_intensity','product_search_type':'boolean'},
                {'model':'product.fancy.color.overtone','_column_name':'product2_fancy_color_overtone','label':'Fancy Color Overtone','type':'many2one','name':'fancy_color_overtone','product_search_type':'boolean'},
                {'model':'product.clarity','_column_name':'product_clarity','label':'Clarity','type':'many2one','name':'clarity_id','product_search_type':'boolean'},
                {'model':'product.cut','_column_name':'product_cut','label':'Cut','type':'many2one','name':'cut_id','product_search_type':'boolean'},
                {'model':'product.polish','_column_name':'product_polish','label':'Polish','type':'many2one','name':'polish_id','product_search_type':'boolean'},
                {'model':'product.symmetry','_column_name':'product_symmetry','label':'Symmetry','type':'many2one','name':'symmetry_id','product_search_type':'boolean'},
                {'model':'product.fluorescence.intensity','_column_name':'product_fluorescence_intensity','label':'Fluorescence Intensity','type':'many2one','name':'fluorescence_intensity_id','product_search_type':'boolean'},
                {'model':'product.lab','_column_name':'product_lab','label':'Lab','type':'many2one','name':'lab_id','product_search_type':'boolean'},
                {'model':'stock.location','_column_name':'stock_location','label':'Location','type':'many2one','name':'location_id','product_search_type':'boolean','domain':[('usage','=','internal')]},
                {'model':None,'_column_name':'product_status','label':'Status','type':'selection','name':'product_status','product_search_type':'boolean','selection_val':[('available','Available'),
                                            ('hold','Hold'),
                                            ('sold','Sold'),
                                            ('on_approval','On Approval'),
                                            ('on_consignment','On Consignment'),
                                            ('offline','Offline'),
                                            ('repair','Repair'),
                                            ('web_sale','Web Sale'),],},
                ] 
        
        for model_info in info :
            make_search(model_info['_column_name'],model_info['name'],model_info['type'],model_info['product_search_type'], no=model_info.get('no') or 1, range=model_info.get('range') or False,single=model_info.get('single') or False)
            
        search_domain.append(('is_certified', '=', True)) 
        print "Domain : ",search_domain
        p = self.pool.get('product.product').search(cr, uid, search_domain,context=context)
        product_ids = ''
        if p :
            product_ids = str(p).strip('[]')
        self._columns = {}
        self._columns['product_ids'] = fields.text('Product IDS')
        result = super(product_search_ept, self).create(cr, uid, {'product_ids':product_ids}, context=context)
        return result
    
    def get_product(self, cr, uid, ids, context=None):
        self_obj = self.browse(cr, uid, ids, context=context)[0]
        product_ids = []
        if self_obj.product_ids:
            product_ids = [ int(x) for x in self_obj.product_ids.split(', ')]
        data_obj = self.pool.get('ir.model.data')
        data_id = data_obj._get_id(cr, uid, 'product', 'stone_tree_view_ept')
        view_id = False
        if data_id:
            view_id = data_obj.browse(cr, uid, data_id, context=context).res_id
        form_data_id = data_obj._get_id(cr, uid, 'product', 'stone_form_view_ept')
        if form_data_id:
            form_view_id = data_obj.browse(cr, uid, form_data_id, context=context).res_id
        
        context.update({'active_ids': [],'no_complete_name':1})
        return {
                   'name': _('Stones'),
                   'view_type': 'form',
                   'res_model': 'product.product',
                   'view_id': False,
                   'domain':"[('id', 'in',%s)]" %(product_ids),
                   'context': context,
                   'views': [(view_id, 'tree'), (form_view_id, 'form')],
                   'type': 'ir.actions.act_window',
                   'target': 'current',
                   'nodestroy': True
               }

product_search_ept()
#             if model_info['type'] == 'many2one' and model_info['product_search_type'] == 'selection':
#                 _moves_arch_lst += """<div style="float:left;">"""%(model_info['label'])
#                 _line_fields.update({
#                              '%s'%(model_info['_column_name']) : {
#                                  'string': 'Name',
#                                  'type' : 'many2one',
#                                  'relation':model_info['model'],
#                              },})
#                 self._columns['%s'%(model_info['_column_name'])] = fields.many2one(model_info['model'],model_info['label'])
#                 _moves_arch_lst += """
#                                 <label string="%s" for="%s" />
#                                 <field name="%s" class="oe_inline" nolabel="1" col="7" /> 
#                                  """%(model_info['label'],model_info['_column_name'],model_info['_column_name']) 