from odoo import api, fields, models, tools, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError


class PartnerConsumer(models.Model):
    _name = 'consumer.partner'

    name = 'Solicitante'


