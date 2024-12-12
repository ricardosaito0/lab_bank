from flask import render_template, flash, request, redirect, url_for, abort, Blueprint, current_app
from flask_login import current_user, login_required
from lab_bank import db
from lab_bank.table.forms import InsertDataForm
from lab_bank.models import Subject, User
import pandas as pd
import os
import openpyxl
from werkzeug.utils import secure_filename
from datetime import datetime
import string

table = Blueprint('table', __name__)

@table.route('/table/insert_data', methods=['GET', 'POST'])
@login_required
def insert_data():
    form = InsertDataForm()

    if form.validate_on_submit():
        
        lineage = form.lineage.data
        if lineage == 'Outros' and form.other_lineage.data:
            lineage = form.other_lineage.data

        sex = form.sex.data
        if sex == 'Outros' and form.other_sex.data:
            sex = form.other_sex.data

        ova_or_control = form.ova_or_control.data
        if ova_or_control == 'Outros' and form.other_ova_or_control.data:
            ova_or_control = form.other_ova_or_control.data

        dead_or_alive = form.dead_or_alive.data
        if dead_or_alive == 'Outros' and form.other_dead_or_alive.data:
            dead_or_alive = form.other_dead_or_alive.data

        acepromazine = form.acepromazine.data
        if acepromazine == 'Outros' and form.other_acepromazine.data:
            acepromazine = form.other_acepromazine.data

        anesthesic = form.anesthesic.data
        if anesthesic == 'Outros' and form.other_anesthesic.data:
            anesthesic = form.other_anesthesic.data

        neuromuscular_blocker = form.neuromuscular_blocker.data
        if neuromuscular_blocker == 'Outros' and form.other_neuromuscular_blocker.data:
            neuromuscular_blocker = form.other_neuromuscular_blocker.data

        flexivent = form.flexivent.data
        if flexivent == 'Outros' and form.other_flexivent.data:
            flexivent = form.other_flexivent.data

        file = request.files.get('excel_file')
        excel_file_path = None
        if file and file.filename:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            original_filename = secure_filename(file.filename)
            filename = f"{timestamp}_{original_filename}"
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            excel_file_path = filepath
            flash('Arquivo salvo com sucesso', 'success')
        else:
            flash('Nenhum arquivo selecionado.', 'warning')

        try:
            subject = Subject(
                lineage=lineage,
                sex=sex,
                date=form.date.data,
                ova_or_control=ova_or_control,
                dead_or_alive=dead_or_alive,
                acepromazine=acepromazine,
                anesthesic=anesthesic,
                neuromuscular_blocker=neuromuscular_blocker,
                age=form.age.data,
                weight=form.weight.data,
                project=form.project.data if form.project.data else '',
                naso_anal_length=form.naso_anal_length.data,
                bronchoalveolar_lavage=form.bronchoalveolar_lavage.data,
                user_id=current_user.id,
                flexivent=flexivent,
                excel_file_path=excel_file_path,
                observations=form.observations.data if form.observations.data else ''
            )
            db.session.add(subject)
            db.session.commit()
            flash('Inserção bem sucedida!', 'success')
            return redirect(url_for('table.insert_data'))

        except Exception as e:
            db.session.rollback()
            flash('Erro ao inserir dados: ' + str(e), 'danger')

    return render_template('insert_data.html', title = 'Inserção de dados', legend = 'Inserção de dados', form=form)


@table.route('/table/display_table')
@login_required
def display_table():
    subjects = Subject.query.all()

    subjects_data = []
    for subject in subjects:
        file_link = None
        if subject.excel_file_path:
            filename = subject.excel_file_path.split('\\')[-1]
            file_link = url_for('table.display_excel_file', filename=filename)
        
        subjects_data.append({
            'ID do Exp.': subject.id,
            'Data do Exp.': subject.date.strftime('%d-%m-%Y') if subject.date else 'N/A',
            'Projeto/pesquisador': subject.project,
            'Espécie/linhagem': subject.lineage,
            'Sexo': subject.sex,
            'Grupo Experimental': subject.ova_or_control,
            'Pré anestésico': subject.acepromazine,
            'Anestésico': subject.anesthesic,
            'Bloqueador neuromuscular': subject.neuromuscular_blocker,
            'Estado ao final do experimento': subject.dead_or_alive,            
            'Idade (semanas)': subject.age,
            'Peso (g)': subject.weight,
            'Comprimento naso anal (cm)': subject.naso_anal_length,
            'Lavado broncoaoveolar (/ 4 x 10⁴)': subject.bronchoalveolar_lavage,
            'ID do Usuário': subject.user_id,
            'Caminho para a tabela': f'<a href="{file_link}" target="_blank">Ver Arquivo Excel</a>' if file_link else 'Nenhum arquivo',
            'Observações': subject.observations
        })

    subject_table = pd.DataFrame(subjects_data).to_html(
        classes='table table-bordered', 
        index=False, 
        escape=False,
        table_id="example_table"
    )
    subject_table = subject_table.replace('</table>', '<tfoot><tr>' +
        ''.join('<th></th>' for _ in subjects_data[0]) +
        '</tr></tfoot></table>')

    return render_template('display_table.html', title='Visualizar tabela', legend='Visualizar tabela', subject_table=subject_table)

@table.route('/table/update_data/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def update_data(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if subject.user_id != current_user.id:
        abort(403)

    form = InsertDataForm()

    if form.validate_on_submit():
        subject.lineage = form.lineage.data
        if subject.lineage == 'Outros' and form.other_lineage.data:
            subject.lineage = form.other_lineage.data

        subject.sex = form.sex.data
        if subject.sex == 'Outros' and form.other_sex.data:
            subject.sex = form.other_sex.data
            
        subject.ova_or_control = form.ova_or_control.data
        if subject.ova_or_control == 'Outros' and form.other_ova_or_control.data:
            subject.ova_or_control = form.other_ova_or_control.data

        subject.dead_or_alive = form.dead_or_alive.data
        if subject.dead_or_alive == 'Outros' and form.other_dead_or_alive.data:
            subject.dead_or_alive = form.other_dead_or_alive.data

        subject.acepromazine = form.acepromazine.data
        if subject.acepromazine == 'Outros' and form.other_acepromazine.data:
            subject.acepromazine = form.other_acepromazine.data

        subject.anesthesic = form.anesthesic.data
        if subject.anesthesic == 'Outros' and form.other_anesthesic.data:
            subject.anesthesic = form.other_anesthesic.data

        subject.neuromuscular_blocker = form.neuromuscular_blocker.data
        if subject.neuromuscular_blocker == 'Outros' and form.other_neuromuscular_blocker.data:
            subject.neuromuscular_blocker = form.other_neuromuscular_blocker.data

        subject.project = form.project.data if form.project.data else ''
        subject.date = form.date.data
        subject.sex = form.sex.data
        subject.age = form.age.data
        subject.weight = form.weight.data
        subject.naso_anal_length = form.naso_anal_length.data
        subject.bronchoalveolar_lavage = form.bronchoalveolar_lavage.data
        subject.observations = form.observations.data if form.observations.data else ''

        file = form.excel_file.data
        if file:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = secure_filename(f"{timestamp}_{file.filename}")
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            subject.excel_file_path = file_path  # Update the file path in the database

        db.session.commit()
        flash('Edição bem sucedida', 'success')
        return redirect(url_for('table.display_table'))

    elif request.method == 'GET':
        form.lineage.data = subject.lineage if subject.lineage in ['Camundongo/Balb C', 'Camundongo/C57', 'Rato/Wistar', 'Outros'] else 'Outros'
        form.other_lineage.data = subject.lineage if subject.lineage not in ['Camundongo/Balb C', 'Camundongo/C57', 'Rato/Wistar', 'Outros'] else ''

        form.sex.data = subject.sex if subject.sex in ['Fêmea', 'Macho', 'Desconhecido', 'Outros'] else 'Outros'
        form.other_sex.data = subject.sex if subject.sex not in ['Fêmea', 'Macho', 'Desconhecido', 'Outros'] else ''

        form.ova_or_control.data = subject.ova_or_control if subject.ova_or_control in ['OVA', 'Controle', 'Outros'] else 'Outros'
        form.other_ova_or_control.data = subject.ova_or_control if subject.ova_or_control not in ['OVA', 'Controle', 'Outros'] else ''

        form.dead_or_alive.data = subject.dead_or_alive if subject.dead_or_alive in ['Vivo', 'Morto na anestesia (antes do experimento)', 'Morto durante o experimento', 'Outros'] else 'Outros'
        form.other_dead_or_alive.data = subject.dead_or_alive if subject.dead_or_alive not in ['Vivo', 'Morto na anestesia (antes do experimento)', 'Morto durante o experimento', 'Outros'] else ''

        form.acepromazine.data = subject.acepromazine if subject.acepromazine in ['Acepromazina 2,5 mg/kg', 'Nenhum', 'Outros'] else 'Outros'
        form.other_acepromazine.data = subject.acepromazine if subject.acepromazine not in ['Acepromazina 2,5 mg/kg', 'Nenhum', 'Outros'] else ''

        form.anesthesic.data = subject.anesthesic if subject.anesthesic in ['Cetamina 100 mg/kg + Xilazina 10 mg/kg', 'Cetamina 100 mg/kg + Xilazina 10 mg/kg + Morfina', 'Nenhum', 'Outros'] else 'Outros'
        form.other_anesthesic.data = subject.anesthesic if subject.anesthesic not in ['Cetamina 100 mg/kg + Xilazina 10 mg/kg', 'Cetamina 100 mg/kg + Xilazina 10 mg/kg + Morfina', 'Nenhum', 'Outros'] else ''

        form.neuromuscular_blocker.data = subject.neuromuscular_blocker if subject.neuromuscular_blocker in ['Brometo de pancurônio 1 mg/kg', 'Brometo de rocurônio', 'Nenhum', 'Outros'] else 'Outros'
        form.other_neuromuscular_blocker.data = subject.neuromuscular_blocker if subject.neuromuscular_blocker not in ['Brometo de pancurônio 1 mg/kg', 'Brometo de rocurônio', 'Nenhum', 'Outros'] else ''

        form.flexivent.data = subject.flexivent if subject.flexivent in ['Unicompartimental', 'Fase Cte', 'Não informado', 'Outros'] else 'Outros'
        form.other_flexivent.data = subject.flexivent if subject.flexivent not in ['Unicompartimental', 'Fase Cte', 'Não informado', 'Outros'] else ''

        form.project.data = subject.project
        form.date.data = subject.date
        form.weight.data = subject.weight
        form.age.data = subject.age
        form.naso_anal_length.data = subject.naso_anal_length
        form.bronchoalveolar_lavage.data = subject.bronchoalveolar_lavage
        form.observations.data = subject.observations

    current_file = None
    if subject.excel_file_path:
        current_file = os.path.basename(subject.excel_file_path)  # Get just the filename

    return render_template('insert_data.html', title='Editar dados', form=form, legend='Editar dados', current_file=current_file)

@table.route('/table/<int:subject_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_data(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    
    if subject.user_id != current_user.id:
        abort(403)
    
    db.session.delete(subject)
    db.session.commit()
    flash('Atualização apagada', 'success')
    
    return redirect(url_for('table.user_subjects', username=current_user.username))

@table.route("/table/<string:username>")  
def user_subjects(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    subjects = Subject.query.filter_by(user_id=user.id).order_by(Subject.id.desc()).paginate(page=page, per_page=7)
    
    return render_template('user_subjects.html', user=user, title=f'Dados de {username}', subjects=subjects)

@table.route('/uploads/<filename>')
@login_required
def display_excel_file(filename):
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    file_path = os.path.join(upload_folder, filename)
    
    if not os.path.exists(file_path):
        flash("Arquivo não encontrado", "danger")
        return redirect(url_for('some_error_page'))

    df = pd.read_excel(file_path)
    num_columns = len(df.columns)
    excel_columns = list(string.ascii_uppercase)
    
    if num_columns > 26:
        extra_columns = num_columns - 26
        excel_columns += [f"{letter1}{letter2}" for letter1 in string.ascii_uppercase for letter2 in string.ascii_uppercase][:extra_columns]
    
    df.columns = excel_columns[:num_columns]
    
    df = df.fillna('')
    
    html_table = df.to_html(classes="table table-bordered table-striped", index=False)
    
    return render_template('view_excel.html', table=html_table, filename=filename)
