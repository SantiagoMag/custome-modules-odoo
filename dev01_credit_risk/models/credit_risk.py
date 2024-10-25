import requests
import driverlessai
import pandas as pd
from odoo.exceptions import UserError
from odoo import models, fields, api
import json

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
    
    """
        MODEL VIRTUAL MACHINE
    """

    loan_prediction = fields.Selection([
        ('0', 'Cumplimiento'),
        ('1', 'Incumplimiento')
    ], string='Predicción Incumplimiento')   
    loan_probability = fields.Float(string='Probabilidad de Incumplimiento', store=True)
        
    """
        MODEL H2O DRIVERLESS
    """
    
    h20_predictions = fields.Text(string='Predicción', store=True)
    h20_predictions_class = fields.Selection([
        ('0', 'Cumplimiento'),
        ('1', 'Incumplimiento')
    ], string='Predicción de Clase', compute="_compute_h20_predictions_class", store=True)
    
    def get_api_vm_url(self,env) -> str | None:
        return env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.api_vm_url')
    
    def action_model_v1_vm(self):
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
                #flask_url = 'http://192.168.68.101:5000/api/predict'
                flask_url = record.get_api_vm_url(record.env)
                response = requests.post(flask_url, json=data)

                if response.status_code == 200:
                    result = response.json()
                    # print(result, flush=True)
                    
                    if result["prediction"] :
                        record.loan_prediction = '1'
                        record.loan_probability = result["probability"]
                    else:
                        record.loan_prediction = '0'
                        record.loan_probability = result["probability"]
      
                else:
                    raise UserError('Error: Could not connect to the Flask server.')
            except Exception as e:
                raise UserError(f'An error occurred: {e}')
    
 
    @api.depends('h20_predictions')
    def _compute_h20_predictions_class(self):
        for record in self:
            if record.h20_predictions:
                result_list = json.loads(record.h20_predictions)
                for k, v in result_list[0].items():
                    if float(v) >= 0.5:
                        record.h20_predictions_class = k[-1:]
    
    def get_h2o_driverless_address(self,env) -> str | None:
        return env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_address')
    def get_h2o_driverless_username(self,env) -> str | None:
        return env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_username')
    def get_h2o_driverless_password(self,env) -> str | None:
        return env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_password')
    def get_h2o_driverless_name_experiment(self,env) -> str | None:
        return env['ir.config_parameter'].sudo().get_param('dev01_credit_risk.h2o_driverless_name_experiment')

    def action_model_v2_h2o(self):

        for record in self:
            ADDRESS=record.get_h2o_driverless_address(record.env)
            USERNAME=record.get_h2o_driverless_username(record.env)
            PASSWORD=record.get_h2o_driverless_password(record.env)
            NAME_EXPERIMENT = record.get_h2o_driverless_name_experiment(record.env)
            data = {
                'person_age': [record.person_age],
                'person_income': [record.person_income],
                'person_home_ownership': [record.person_home_ownership],
                'person_emp_length': [record.person_emp_length],
                'loan_intent': [record.loan_intent],
                'loan_grade': [record.loan_grade],
                'loan_amnt': [record.loan_amnt],
                'loan_int_rate': [record.loan_int_rate],
                'loan_percent_income': [record.loan_percent_income],
                'cb_person_default_on_file': [record.cb_person_default_on_file],
                'cb_person_cred_hist_length': [record.cb_person_cred_hist_length],
            }
            df = pd.DataFrame(data)
            
            try:
                client = driverlessai.Client(address=ADDRESS, username=USERNAME, password=PASSWORD, verify=False)
                experiment = client.experiments.get_by_name(NAME_EXPERIMENT)
                prediction = experiment.predict(df).to_pandas()
                predictions = prediction.to_json(orient='records')
                record.h20_predictions = str(predictions)
                
            except Exception as e:
                raise UserError(f'An error occurred: {e}')