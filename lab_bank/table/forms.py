from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField, FileField
from wtforms.validators import DataRequired, Optional

class InsertDataForm(FlaskForm):
    
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    
    lineage = SelectField('Insira a linhagem', choices=[('Balb', 'Balb'), ('Outros', 'Outros')], default='Balb')
    other_lineage = StringField('Especificar linhagem', render_kw={'placeholder': 'Especifique aqui...'})
    
    ova_or_control = SelectField('Grupo experimental', choices=[('OVA', 'OVA'), ('Controle', 'Controle'), ('Outros', 'Outros')], default='OVA')
    other_ova_or_control = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'})
    
    dead_or_alive = SelectField('Vivo ou morto?', choices=[('Vivo', 'Vivo'), ('Morto', 'Morto')], default='Vivo')
    
    acepromazine = SelectField('Tratamento', choices=[('Acepromazina', 'Acepromazina'), ('Nenhum', 'Nenhum'), ('Outros', 'Outros')], default='Acepromazina')
    other_acepromazine = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'})
    
    weight = FloatField('Peso', default=0)
    naso_anal_length = FloatField('Comprimento naso anal', default=0)
    
    excel_file = FileField()
    
    submit = SubmitField('Confirmar inserção de dados')
