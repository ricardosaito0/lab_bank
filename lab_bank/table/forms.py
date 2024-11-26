from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField, FileField
from wtforms.validators import DataRequired, Optional

class InsertDataForm(FlaskForm):
    
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    
    lineage = SelectField('Insira a linhagem', choices=[('Balb', 'Balb'), ('Outros', 'Outros')], default='Balb')
    other_lineage = StringField('Especificar linhagem', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    ova_or_control = SelectField('Grupo experimental', choices=[('OVA', 'OVA'), ('Controle', 'Controle'), ('Outros', 'Outros')], default='OVA')
    other_ova_or_control = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    dead_or_alive = SelectField('Observações', choices=[('Vivo', 'Vivo'), ('Morto', 'Morto'), ('Outros', 'Outros')], default='Vivo')
    other_dead_or_alive = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    acepromazine = SelectField('Tratamento', choices=[('Acepromazina', 'Acepromazina'), ('Nenhum', 'Nenhum'), ('Outros', 'Outros')], default='Acepromazina')
    other_acepromazine = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    weight = FloatField('Peso', default=0)
    naso_anal_length = FloatField('Comprimento naso anal', default=0)
    
    project = StringField('Projeto', default = '', validators=[Optional()])
    
    excel_file = FileField()
    
    submit = SubmitField('Confirmar inserção de dados')
