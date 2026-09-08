from odoo import api, fields, models

class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    contact_type = fields.Selection(
        [
            ('company', 'Company'),
            ('person', 'Person')
        ],
        string='Contact Type',
        compute='_compute_contact_type',
        store=True,
        readonly = False
    )



    @api.depends('partner_id', 'partner_id.is_company')
    def _compute_contact_type(self):
        for lead in self:
            if lead.partner_id and lead.partner_id.is_company:
                lead.contact_type = 'company'
            else:
                lead.contact_type = 'person'