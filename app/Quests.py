from flask import Blueprint, render_template, request, redirect, g, url_for
from app.authentication import login_required
from .dataBase import Quest
from app import db

bp = Blueprint('Quests', __name__, url_prefix='/Quests')

@bp.route('/list', methods=['GET','POST'])
@login_required
def list():
    if request.method == 'POST':
        user_quest = g.user.id
        quest_title = request.form['quest-title']
        quest_description = request.form['quest-description']
        quest__state = False
        newQuest = Quest(user_quest, quest_title, quest_description,quest__state)
        db.session.add(newQuest)
        db.session.commit()
        return redirect(url_for('Quests.list'))
        
    quests = Quest.query.filter_by(userQuest=g.user.id).order_by(Quest.id.desc()).all()
    return render_template('Quests/list.html', questslist=quests)

#editar
@bp.route('/edit', methods=['POST'])
@login_required
def edit():
    quest_id = request.form['quest-id']
    new_title = request.form['quest-title']
    new_description = request.form['quest-description']
    
    quest_to_edit = Quest.query.get_or_404(quest_id)
    
    if quest_to_edit.userQuest == g.user.id:
        quest_to_edit.title = new_title
        quest_to_edit.description = new_description
        
        db.session.commit()
        
    return redirect(url_for('Quests.list'))


#eliminar
@bp.route('/delete', methods=['POST'])
@login_required
def delete():
    quest_id = request.form['quest-id']
    
    quest_to_delete = Quest.query.get_or_404(quest_id)
    
    if quest_to_delete.userQuest == g.user.id:
        db.session.delete(quest_to_delete)
        db.session.commit()
        
    return redirect(url_for('Quests.list'))

#Check
@bp.route('/toggle', methods=['POST'])
@login_required
def toggle():
    quest_id = request.form['quest-id']
    
    quest_to_toggle = Quest.query.get_or_404(quest_id)
    
    if quest_to_toggle.userQuest == g.user.id:
        quest_to_toggle.state = not quest_to_toggle.state
        db.session.commit()
        
    return redirect(url_for('Quests.list'))