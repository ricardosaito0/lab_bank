from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, DateField, FileField
from wtforms.validators import DataRequired, Optional

class CustomFloatField(FloatField):
    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = float(valuelist[0].replace(',', '.'))
            except ValueError:
                self.data = None
                raise ValidationError('Valor inválido. Use números e um separador decimal válido (., ,).')

class InsertDataForm(FlaskForm):
    
    project = StringField('Projeto/pesquisador', default = '', validators=[Optional()])

    name_number = StringField('Nome/número do animal', default = '', validators=[Optional()])

    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    
    lineage = SelectField('Espécie/linhagem', choices=[('Camundongo/Balb C', 'Camundongo/Balb C'), ('Camundongo/C57', 'Camundongo/C57'), ('Rato/Wistar', 'Rato/Wistar'), ('Outros', 'Outros')], default='Balb')
    other_lineage = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    sex = SelectField('Sexo', choices=[('Fêmea', 'Fêmea'), ('Macho', 'Macho'), ('Desconhecido', 'Desconhecido'), ('Outros', 'Outros')], default='Fêmea')
    other_sex = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    ova_or_control = SelectField('Grupo experimental', choices=[('OVA', 'OVA'), ('Controle', 'Controle'), ('Outros', 'Outros')], default='OVA')
    other_ova_or_control = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
   
    acepromazine = SelectField('Pré anestésico', choices=[('Acepromazina 2,5 mg/kg', 'Acepromazina 2,5 mg/kg'), ('Nenhum', 'Nenhum'), ('Outros', 'Outros')], default='Acepromazina')
    other_acepromazine = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
   
    anesthesic = SelectField('Anestésico', choices=[('Cetamina 100 mg/kg + Xilazina 10 mg/kg', 'Cetamina 100 mg/kg + Xilazina 10 mg/kg'), ('Cetamina 100 mg/kg + Xilazina 10 mg/kg + Morfina', 'Cetamina 100 mg/kg + Xilazina 10 mg/kg + Morfina'),('Nenhum', 'Nenhum'), ('Outros', 'Outros')], default='Acepromazina')
    other_anesthesic = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])   
   
    neuromuscular_blocker = SelectField('Bloqueador neuromuscular', choices=[('Brometo de pancurônio 1 mg/kg', 'Brometo de pancurônio 1 mg/kg'), ('Brometo de rocurônio', 'Brometo de rocurônio'), ('Nenhum', 'Nenhum'), ('Outros', 'Outros')], default='Acepromazina')
    other_neuromuscular_blocker = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
   
    dead_or_alive = SelectField('Estado ao final do experimento', choices=[('Vivo', 'Vivo'), ('Morto na anestesia (antes do experimento)', 'Morto na anestesia (antes do experimento)'), ('Morto durante o experimento', 'Morto durante o experimento'), ('Outros', 'Outros')], default='Vivo')
    other_dead_or_alive = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    age = CustomFloatField('Idade (semanas) (zero se não foi medido)', default=0)

    weight = CustomFloatField('Peso (g) (zero se não foi medido)', default=0)
    
    naso_anal_length = CustomFloatField('Comprimento naso anal (cm) (zero se não foi medido)', default=0)
    
    bronchoalveolar_lavage = CustomFloatField('Lavado broncoaoveolar (/ 4 x 10⁴) (zero se não foi medido)', default=0)

    flexivent = SelectField('FlexiVent', choices=[('Unicompartimental', 'Unicompartimental'), ('Fase Cte', 'Fase Cte'), ('Não informado', 'Não informado'), ('Outros', 'Outros')], default='Não informado')
    other_flexivent = StringField('Especificar', render_kw={'placeholder': 'Especifique aqui...'}, validators=[Optional()])
    
    excel_file = FileField()

    observations = StringField('Observações', default = '', validators=[Optional()])

    submit = SubmitField('Confirmar inserção de dados')
