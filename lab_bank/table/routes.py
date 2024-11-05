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

table = Blueprint('table', __name__)

@table.route('/table/insert_data', methods=['GET', 'POST'])
@login_required
def insert_data():
    form = InsertDataForm()
    
    if form.validate_on_submit():
        if form.excel_file.data:  # Check if a file has been uploaded
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form.excel_file.data)  # Get the file extension from the filename
            sheet_fn = random_hex + f_ext  # Generate a unique filename
            sheet_path = os.path.join(current_app.root_path, 'static', 'uploaded_spreadsheets', sheet_fn)

            # Save the uploaded file directly
            file = request.files['file']

            # Create the Subject object
            subject = Subject(
                lineage=form.lineage.data,
                date=form.date.data,
                ova_or_control=form.ova_or_control.data,
                dead_or_alive=form.dead_or_alive.data,
                acepromazine=form.acepromazine.data,
                weight=form.weight.data,
                naso_anal_length=form.naso_anal_length.data,
                user_id=current_user.id,
                excel_file_path=sheet_fn  # Save the filename in the database
            )

            # Add the object to the database session and commit
            db.session.add(subject)
            db.session.commit()

            flash('Inserção bem sucedida!', 'success')
            return redirect(url_for('insert_data'))  # Redirect after successful submission
        else:
            flash('Erro: Nenhum arquivo foi carregado.', 'danger')
    
    return render_template('insert_data.html', title='Inserir dados', legend='Inserir dados', form=form)

    
@table.route('/table/display_table')
@login_required
def display_table():
    subjects = Subject.query.all()
    
    subjects_data = []
    for subject in subjects:
        excel_link = 'N/A'
        if subject.excel_file_path:
            # Verifica se o arquivo existe no diretório uploads
            file_path = os.path.join(current_app.root_path, 'static', 'uploads', subject.excel_file_path)
            if os.path.exists(file_path):
                excel_link = f'<a href="{url_for("static", filename="uploads/" + subject.excel_file_path)}">Download</a>'

        # Adiciona os dados do sujeito com o link (se houver)
        subjects_data.append({
            'ID do Exp.': subject.id,
            'Data do Exp.': subject.date.strftime('%d-%m-%Y') if subject.date else 'N/A',
            'Linhagem': subject.lineage,
            'OVA/Controle': subject.ova_or_control,
            'Vivo/Morto': subject.dead_or_alive,
            'Acepromazina?': subject.acepromazine,
            'Peso': subject.weight,
            'CNA': subject.naso_anal_length,
            'ID do Usuário': subject.user_id,
            'Arquivo Excel': excel_link
        })
    
    # Gera o HTML da tabela com pandas
    subject_table = pd.DataFrame(subjects_data).to_html(classes='table table-bordered', index=False, escape=False)
    
    return render_template('display_table.html', title='Visualizar tabela', legend='Visualizar tabela', subject_table=subject_table)


    
@table.route('/table/<int:subject_id>/update/', methods=['GET', 'POST'])
@login_required
def update_data(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    # Verifica se o usuário atual é o proprietário dos dados
    if subject.user_id != current_user.id:
        abort(403)

    form = InsertDataForm()

    if form.validate_on_submit():
        # Atualiza os campos do objeto 'subject'
        subject.lineage = form.lineage.data
        subject.date = form.date.data
        subject.ova_or_control = form.ova_or_control.data
        subject.dead_or_alive = form.dead_or_alive.data
        subject.acepromazine = form.acepromazine.data
        subject.weight = form.weight.data
        subject.naso_anal_length = form.naso_anal_length.data

        # Atualiza o arquivo Excel, se um novo arquivo for enviado
        file = request.files.get('excel_file')
        if file and file.filename != '':
            # Remove o arquivo antigo, se houver
            if subject.excel_file_path:
                old_file_path = os.path.join(current_app.root_path, 'static', 'uploads', subject.excel_file_path)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            
            # Salva o novo arquivo
            filename = secure_filename(file.filename)
            uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            file_path = os.path.join(uploads_dir, filename)
            file.save(file_path)

            # Atualiza o caminho do arquivo no banco de dados
            subject.excel_file_path = filename

        db.session.commit()
        flash('Edição bem sucedida', 'success')
        return redirect(url_for('table.display_table'))

    elif request.method == 'GET':
        # Preenche o formulário com os dados atuais do objeto 'subject'
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