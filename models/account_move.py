from odoo import fields,models,api
import convert_numbers
# from deep_translator import GoogleTranslator
from uuid import uuid4
import qrcode
from odoo.exceptions import UserError

import base64
import logging

from lxml import etree

logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'
    _order = "invoice_date desc"

    def action_post(self):
        res = super(AccountMove, self).action_post()
        configuration = self.env['einvoice.config'].search([])
        if self.move_type == 'out_invoice':
            if configuration:
                if self.partner_id.type_of_customer == 'b_b':
                    # For Sending Email After Sheduling Interview
                    if configuration.invoice_email == True:
                        if self.env['einvoice.admin'].search([]):
                            self.admin_mail = self.env['einvoice.admin'].search([])[-1].name.id
                            template_id = self.env['mail.template'].sudo().search(
                                [('name', '=', 'Invoice: Send by email B2B')]).id
                            if template_id:
                                template = self.env['mail.template'].browse(template_id)
                                template.send_mail(self.id, force_send=True)
                            else:
                                raise UserError(
                                    'Please Create an Email Template In the name "Invoice: Send by email B2B" by giving PDF as Default B2B Formate')
                        else:
                            raise UserError('Please Configure the Admin Details to whom the mail need to be sended')
                    if configuration.invoice_print == True:
                        return self.env.ref('natcom_einvoice_report.natcom_einvoice_report').report_action(self)
                if self.partner_id.type_of_customer == 'b_c':
                    if configuration.invoice_email == True:
                        if self.env['einvoice.admin'].search([]):
                            self.admin_mail = self.env['einvoice.admin'].search([])[-1].name.id
                            template_id = self.env['mail.template'].sudo().search(
                                [('name', '=', 'Invoice: Send by email B2C')]).id
                            if template_id:
                                template = self.env['mail.template'].browse(template_id)
                                template.send_mail(self.id, force_send=True)
                            else:
                                raise UserError(
                                    'Please Create an Email Template In the name "Invoice: Send by email B2C" by giving PDF as Default B2C Formate')
                        else:
                            raise UserError('Please Configure the Admin Details to whom the mail need to be sended')
                    if configuration.invoice_print == True:
                        # return self.env.ref('account_invoice_ubl.account_invoices_b2c').report_action(self)
                        return self.env.ref('natcom_einvoice_report.natcom_einvoice_report').report_action(self)
        else:
            ''
        return res



