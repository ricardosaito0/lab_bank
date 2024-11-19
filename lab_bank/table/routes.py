from flask import render_template, flash, request, redirect, url_for, abort, Blueprint, current_app
from flask_login import current_user, login_required
from lab_bank import db
from lab_bank.table.forms import InsertDataForm
from lab_bank.models import Subject, User
import pandas as pd
import os
import openpyxl
from werkzeug.utils import secure_filename
import secrets
from datetime import datetime
import string

table = Blueprint('table', __name__)

@table.route('/table/insert_data', methods=['GET', 'POST'])
@login_required
def insert_data():
    form = InsertDataForm()

    if form.validate_on_submit():
        # Handle "Outros" fields with custom input
        lineage = form.lineage.data
        if lineage == 'Outros' and form.other_lineage.data:
            lineage = form.other_lineage.data  # Use the text input value if provided

        ova_or_control = form.ova_or_control.data
        if ova_or_control == 'Outros' and form.other_ova_or_control.data:
            ova_or_control = form.other_ova_or_control.data  # Use the text input value if provided

        acepromazine = form.acepromazine.data
        if acepromazine == 'Outros' and form.other_acepromazine.data:
            acepromazine = form.other_acepromazine.data  # Use the text input value if provided

        # Handle file upload
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

        # Now create the Subject object using the updated values
        try:
            subject = Subject(
                lineage=lineage,
                date=form.date.data,
                ova_or_control=ova_or_control,
                dead_or_alive=form.dead_or_alive.data,
                acepromazine=acepromazine,
                weight=form.weight.data,
                naso_anal_length=form.naso_anal_length.data,
                user_id=current_user.id,
                excel_file_path=excel_file_path  # Store the file path
            )

            db.session.add(subject)
            db.session.commit()
            flash('Inserção bem sucedida!', 'success')
            return redirect(url_for('table.insert_data'))

        except Exception as e:
            db.session.rollback()
            flash('Erro ao inserir dados: ' + str(e), 'danger')
    
    return render_template('insert_data.html', form=form)
    
@table.route('/table/display_table')
@login_required
def display_table():
    subjects = Subject.query.all()

    subjects_data = []
    for subject in subjects:
        file_link = None
        if subject.excel_file_path:
            # Assuming the file is stored in the 'static/uploads' directory
            filename = subject.excel_file_path.split('\\')[-1]  # Get the filename/uploads/<filename>
            file_link = url_for('table.display_excel_file', filename=filename)
        
        subjects_data.append({
            'ID do Exp.': subject.id,
            'Data do Exp.': subject.date.strftime('%d-%m-%Y') if subject.date else 'N/A',
            'Linhagem': subject.lineage,
            'Grupo Experimental': subject.ova_or_control,
            'Vivo/Morto': subject.dead_or_alive,
            'Tratamento': subject.acepromazine,
            'Peso': subject.weight,
            'CNA': subject.naso_anal_length,
            'ID do Usuário': subject.user_id,
            'Caminho para a tabela': f'<a href="{file_link}" target="_blank">Ver Arquivo Excel</a>' if file_link else 'Nenhum arquivo'
        })

    #subject_table = pd.DataFrame(subjects_data).to_html(classes='table table-bordered', index=False, escape=False)
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
        subject.date = form.date.data
        subject.ova_or_control = form.ova_or_control.data
        subject.dead_or_alive = form.dead_or_alive.data
        subject.acepromazine = form.acepromazine.data
        subject.weight = form.weight.data
        subject.naso_anal_length = form.naso_anal_length.data

        file = form.excel_file.data
        if file:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            filename = secure_filename(f"{timestamp}_{file.filename}")
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            subject.excel_file_path = file_path
        else:
            subject.excel_file_path = subject.excel_file_path

        db.session.commit()
        flash('Edição bem sucedida', 'success')
        return redirect(url_for('table.display_table'))

    elif request.method == 'GET':

        form.lineage.data = subject.lineage
        form.date.data = subject.date
        form.ova_or_control.data = subject.ova_or_control
        form.dead_or_alive.data = subject.dead_or_alive
        form.acepromazine.data = subject.acepromazine
        form.weight.data = subject.weight
        form.naso_anal_length.data = subject.naso_anal_length

    return render_template('insert_data.html', title='Editar dados', form=form, legend='Editar dados')
    

@table.route('/table/<int:subject_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_data(subject_id):
    
    subject = Subject.query.get_or_404(subject_id)
    
    if subject.user_id != current_user.id:
        
        abort(403)
        
    db.session.delete(subject)
    db.session.commit()
    flash('Atualização apagada', 'success')
    
    return redirect(url_for('table.user_subjects', username = current_user.username))
    
@table.route("/table/<string:username>")  
def user_subjects(username):

    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    subjects = Subject.query.filter_by(owner = user).order_by(Subject.id.desc()).paginate(page = page, per_page = 7)
    
    return render_template('user_subjects.html', user = user, title = f'Dados de {username}', subjects = subjects)
    
@table.route('/uploads/<filename>')
@login_required
def display_excel_file(filename):
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    file_path = os.path.join(upload_folder, filename)
    
    if not os.path.exists(file_path):
        flash("File not found", "danger")
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