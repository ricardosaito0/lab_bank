from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField

class InsertDataForm(FlaskForm):
    
    lineage = SelectField('Insira a linhagem', choices=[('Balb', 'Balb'), ('Outros', 'Outros')], default='Balb')
    other_lineage = StringField('Especificar linhagem', render_kw={'placeholder': 'Especifique aqui...'})
    
    ova_or_control = SelectField('OVA ou Controle?', choices=[('OVA', 'OVA'), ('Controle', 'Controle'), ('Outros', 'Outros')], default='OVA')
    other_ova_or_control = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'})
    
    dead_or_alive = SelectField('Vivo ou morto?', choices=[('Vivo', 'Vivo'), ('Morto', 'Morto')], default='Vivo')
    
    acepromazine = SelectField('Acepromazina?', choices=[('Sim', 'Sim'), ('Não', 'Não'), ('Outros', 'Outros')], default='Sim')
    other_acepromazine = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'})
    
    weight = FloatField('Peso', default=0)
    naso_anal_length = FloatField('Comprimento naso_anal', default=0)
    
    submit = SubmitField('Confirmar inserção de dados')



