﻿from openerp import models, fields, api
import datetime
from datetime import date

class account_analytic_account_report_methods(models.Model):
    _inherit = ['account.analytic.account']
    
    def decimal_to_hours(self, hoursDecimal):
        hours = int(hoursDecimal);
        minutesDecimal = ((hoursDecimal - hours) * 60);
        minutes = int(minutesDecimal);
        if minutes<10:
            minutes = "0"+str(minutes)
        else:
            minutes = str(minutes)
        hours = str(hours)
        return hours + ":" + minutes
     
    def check_start_end_line_date(self, lineDate):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report and contract_report.active:
                if not contract_report.start_date:
                    start_date = datetime.datetime.strptime("1980-01-01", "%Y-%m-%d").date()
                else:
                    start_date = datetime.datetime.strptime(contract_report.start_date, "%Y-%m-%d").date()
                if not contract_report.end_date:
                    end_date = date.today()
                else:
                    end_date = datetime.datetime.strptime(contract_report.end_date, "%Y-%m-%d").date()
                line_date = datetime.datetime.strptime(lineDate, "%Y-%m-%d").date()

                return start_date <= line_date <= end_date
            else:
                return True
        else:
            return True
        
    def get_report_interval(self, contract_date_start):
        cr = self.env.cr
        uid = self.env.user.id
        contract_report_obj = self.pool.get('contract.report')
        contract_report_id = contract_report_obj.search(cr, uid, [('id','=',1)])
        if not contract_date_start:
            contract_date_start = datetime.datetime.strptime("1980-01-01", "%Y-%m-%d").date()
        default_date_string = datetime.datetime.strptime(contract_date_start, "%Y-%m-%d").date().strftime('%d-%m-%Y')+" - "+date.today().strftime('%d-%m-%Y')
        if contract_report_id:
            contract_report = contract_report_obj.browse(cr, uid, contract_report_id[0])
            if contract_report.active:
                if not contract_report.start_date:
                    start_date = datetime.datetime.strptime(contract_date_start, "%Y-%m-%d").date()
                else:
                    start_date = datetime.datetime.strptime(contract_report.start_date, "%Y-%m-%d").date()
                if not contract_report.end_date:
                    end_date = date.today()
                else:
                    end_date = datetime.datetime.strptime(contract_report.end_date, "%Y-%m-%d").date()
                return start_date.strftime('%d-%m-%Y')+" - "+end_date.strftime('%d-%m-%Y')
            else:
                return default_date_string
        else:
            return default_date_string