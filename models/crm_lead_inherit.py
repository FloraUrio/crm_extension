from odoo import api, fields, models

class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    contact_type = fields.Selection(
        [
            ('company', 'Company'),
            ('person', 'Person')
        ],
        string='Contact Type'
    )

    deal_size = fields.Selection(
        [
            ('small', 'Small_Deal'),
            ('medium', 'Normal_Deal'),
            ('large', 'Big_Deal')
        ],
        string = 'Deal Size',
        compute = '_compute_deal_size',
        store = True
    )

    lead_age_days = fields.Integer(
        compute='_compute_lead_age', store=True)



    @api.depends('create_date')
    def _compute_lead_age(self):
       for lead in self:
        if lead.create_date:
            lead.lead_age_days = (fields.Date.today() - lead.create_date.date()).days
        else:
            lead.lead_age_days = 0

    @api.onchange('partner_id')
    def _onchange_partner_id_contact_type(self):
        if self.partner_id and not self.contact_type:
            self.contact_type = 'company' if self.partner_id.is_company else 'person'
         
   # @api.depends('partner_id')
    #def _compute_contact_type(self):
       # for lead in self:
           # if lead.partner_id and lead.partner_id.is_company:
               # lead.contact_type = 'company'
           # else :
             #   lead.contact_type = 'person'

        

    @api.depends('expected_revenue')
    def _compute_deal_size(self):
        for lead in self:
            if lead.expected_revenue < 10000:
                lead.deal_size = 'small'
            elif lead.expected_revenue >= 10000 and lead.expected_revenue <= 50000:
                    lead.deal_size = 'medium'
            else:
                        lead.deal_size = 'large'