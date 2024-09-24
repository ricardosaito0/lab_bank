from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField

class InsertDataForm(FlaskForm):
    
    lineage = StringField('Insira a linhagem', default = 'Balb')
    ova_or_control = StringField('OVA ou Controle?', default = 'OVA')
    dead_or_alive = StringField('Vivo ou morto?', default = 'Vivo')
    acepromazine = StringField('Com ou sem acepromazina?', default = 'Com')
    weight = FloatField('Peso', default = 0.0)
    naso_anal_length = FloatField('Comprimento naso_anal', default = 0.0)
    
    submit = SubmitField('Confirmar inserção de dados')