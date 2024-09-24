from flask import render_template, flash, request, redirect, url_for, abort, Blueprint
from flask_login import current_user, login_required
from lab_bank import db
from lab_bank.table.forms import InsertDataForm
from lab_bank.models import Subject
import pandas as pd

table = Blueprint('table', __name__)

@table.route('/table/insert_data', methods=['GET', 'POST'])
def insert_data():
    
    form = InsertDataForm()
    
    if form.validate_on_submit():

        subject = Subject(lineage = form.lineage.data, ova_or_control = form.ova_or_control.data, dead_or_alive = form.dead_or_alive.data, acepromazine = form.acepromazine.data, weight = form.weight.data, naso_anal_length = form.naso_anal_length.data, user_id = current_user.id)

        db.session.add(subject)
        db.session.commit()

        flash(f'Inserção bem sucedida!', 'success')
    
    return render_template('insert_data.html', title = 'Inserir dados', form = form)
    
@table.route('/table/display_table')
def display_table():
    
    subjects = Subject.query.all()
    
    subjects_data = [
        {
            'id': subject.id,
            'lineage': subject.lineage,
            'ova_or_control': subject.ova_or_control,
            'dead_or_alive': subject.dead_or_alive,
            'acepromazine': subject.acepromazine,
            'weight': subject.weight,
            'naso_anal_length': subject.naso_anal_length,
            'user_id': subject.user_id
        }
        for subject in subjects
    ]
    
    subject_table = pd.DataFrame(subjects_data).to_html()
    
    return render_template('display_table.html', title = 'Visualizar tabela', subject_table = subject_table)
    
@table.route('/table/<int:subject_id>/update/', methods=['GET', 'POST'])
@login_required
def update_post(subject_id):
    
    subject = Subject.query.get_or_404(subject_id)
    
    if subject.user_id != current_user.id:
        
        abort(403)
        
    form = InsertDataForm()
    
    if form.validate_on_submit():
        
        subject.lineage = form.lineage.data
        subject.ova_or_control = form.ova_or_control.data
        subject.dead_or_alive = form.dead_or_alive.data
        subject.acepromazine = form.acepromazine.data
        subject.weight = form.weight.data
        subject.naso_anal_length = form.naso_anal_length.data
        db.session.commit()
        
        flash('Edição bem sucedida', 'success')
        
        return redirect(url_for('table.display_table'))
        
    elif request.method == 'GET':
        
        form.lineage.data = subject.lineage
        form.ova_or_control.data = subject.ova_or_control
        form.dead_or_alive.data = subject.dead_or_alive
        form.acepromazine.data = subject.acepromazine
        form.weight.data = subject.weight
        form.naso_anal_length.data = subject.naso_anal_length
    
    return render_template('insert_data.html', title='Editar tabela', form = form, legend = 'Editar tabela')
    
@table.route('/table/<int:subject_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_post(subject_id):
    
    subject = Subject.query.get_or_404(subject_id)
    
    if subject.user_id != current_user.id:
        
        abort(403)
        
    db.session.delete(subject)
    db.session.commit()
    flash('Atualização apagada', 'success')
    
    return redirect(url_for('table.display_table'))
    
@table.route('/table/user_subjects/', methods=['GET', 'POST'])
@login_required
def user_subjects():
    
    subjects = Subject.query.get_or_404(subject_id)
    
    if subject.user_id != current_user.id:
        
        abort(403)
    
    return render_template('user_subjects.html', subjects = subjects)