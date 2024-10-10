from odoo import models, fields, api
import requests
from odoo.exceptions import UserError

class CreditRiskModel(models.Model):
    _name = 'credit.risk.model'
    _description = 'Credit Risk Model'

    name = fields.Char(string='Nombre', required=True, store=True)
    description = fields.Text(string='Notas', store=True)

    person_age = fields.Integer(string='Edad', store=True)
    person_income = fields.Float(string='Ingreso Anual', store=True)
    person_home_ownership = fields.Selection([
        ('RENT', 'Rent'),
        ('OWN', 'Own'),
        ('MORTGAGE', 'Mortgage'),
        ('OTHER', 'Other')
    ], string='Propiedad Vivienda', store=True)
    person_emp_length = fields.Integer(string='Años Empleo', store=True)
    loan_intent = fields.Selection([
        ('PERSONAL', 'Personal'),
        ('EDUCATION', 'Education'),
        ('MEDICAL', 'Medical'),
        ('VENTURE', 'Venture'),
        ('HOMEIMPROVEMENT', 'HomeImprovement'),
        ('DEBTCONSOLIDATION', 'DebtConsolidation'),
    ], string='Propósito Préstamo', store=True)
    loan_grade = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'), 
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
    ], string='Calíficación Préstamo', store=True)
    loan_amnt = fields.Float(string='Monto Préstamo', store=True)
    loan_int_rate = fields.Float(string='Tasa de Interés', store=True)
    
    loan_percent_income = fields.Float(string='Deuda/Ingreso',
                                       help='Porcentaje de ingreso utilizado para pagar la deuda pendiente',
                                       store=True)
    cb_person_default_on_file = fields.Selection([
        ('Y', 'Yes'),
        ('N', 'No'),
    ], string='Incumplimiento Anterior', store=True)
    cb_person_cred_hist_length = fields.Integer(string='Historial Crediticio', help = "Longitud del historial crediticio (en años)" , store=True)
    


    loan_status = fields.Selection([
        ('0', 'Cumplimiento'),
        ('1', 'Incumplimiento')
    ], string='Estado de Deuda', help = 'If the loan has defaulted or not (0 = non-default, 1 = default).', store=True)
    loan_prediction = fields.Selection([
        ('0', 'Cumplimiento'),
        ('1', 'Incumplimiento')
    ], string='Predicción Incumplimiento')   
    loan_probability = fields.Float(string='Probabilidad de Incumplimiento', store=True)
    
    
    def action_check_loan_eligibility(self):
        for record in self:
            data = {
                'person_age': record.person_age,
                'person_income': record.person_income,
                'person_home_ownership': record.person_home_ownership,
                'person_emp_length': record.person_emp_length,
                'loan_intent': record.loan_intent,
                'loan_grade': record.loan_grade,
                'loan_amnt': record.loan_amnt,
                'loan_int_rate': record.loan_int_rate,
                'loan_percent_income': record.loan_percent_income,
                'cb_person_default_on_file': record.cb_person_default_on_file,
                'cb_person_cred_hist_length': record.cb_person_cred_hist_length,
            }

            try:
                flask_url = 'http://192.168.68.104:5000/api/predict'
                response = requests.post(flask_url, json=data)

                if response.status_code == 200:
                    result = response.json()
                    print(result, flush=True)
                    if result["prediction"] :
                        message = 'The loan is non approved.'
                        record.loan_prediction = '1'
                        record.loan_probability = result["probability"]
                    else:
                        message = 'The loan is approved.'
                        record.loan_prediction = '0'
                        record.loan_probability = result["probability"]
      
                else:
                    raise UserError('Error: Could not connect to the Flask server.')
            except Exception as e:
                raise UserError(f'An error occurred: {e}')