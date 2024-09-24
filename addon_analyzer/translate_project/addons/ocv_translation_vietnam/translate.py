import logging

from openerp import tools
import openerp.modules
import subprocess
from openerp import models, fields, api
from collections import defaultdict
from difflib import get_close_matches
import logging

from openerp import api, tools
import openerp.modules
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.exceptions import AccessError, UserError, ValidationError

_logger = logging.getLogger(__name__)

TRANSLATION_TYPE = [
    ('field', 'Field'),                         # deprecated
    ('model', 'Object'),
    ('report', 'Report/Template'),
    ('selection', 'Selection'),
    ('view', 'View'),                           # deprecated
    ('help', 'Help'),                           # deprecated
    ('code', 'Code'),
    ('constraint', 'Constraint'),
    ('sql_constraint', 'SQL Constraint')
]


_logger = logging.getLogger(__name__)


class ocv_vietnam_translate(models.TransientModel):
    _name = "ocv.vietnam.translate"

    def act_translate(self, cr, uid, ids, context=None):
        _logger.info('act_translate() BEGIN')
        cr.execute("delete from ir_translation")
        cr.commit
        module_ids = self.pool['ir.module.module'].search(cr, uid, [])
        module_rcs = self.pool['ir.module.module'].browse(cr, uid, module_ids)
        modules = [m.name for m in module_rcs if m.state in ('installed', 'to install', 'to upgrade')]
        for module_name in modules:
            trans_file = openerp.modules.get_module_resource('ocv_translation_vietnam', 'i18n', module_name + '.po')
            if trans_file:
                _logger.info('module %s: loading translation file (%s) for language %s', module_name, 'vi_VN', 'vi_VN')
                tools.trans_load(cr, trans_file, 'vi_VN', verbose=False, module_name=module_name)
        return True
