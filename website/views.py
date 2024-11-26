from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user #this is why I need UserMixin in models.py
from .models import Note
from . import db


from utils.playerGameLog import get_player_game_log, rec_per_game_bar_graph
from utils.playerListAPI import get_player_info


import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET']) # home page and what ever is / will run 
@login_required # cant get to home page unless logged in
def home():
    return render_template("home.html", user=current_user) 

@views.route('/notes', methods=['GET', 'POST']) # home page and what ever is / will run 
@login_required # cant get to home page unless logged in
def note():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category= 'error ')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')
    return render_template("notes.html", user=current_user) 


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #if the user who is signed in owns the note then...
            db.session.delete(note)
            db.session.commit()
                    
    return jsonify({})


# change the route to match the method
@views.route('/nfl_research_tool', methods=['GET','POST'])
@login_required
def nfl_research_tool():
    
    #when submit happens
    if request.method == 'POST':
        
        #player name = whatever is in text field
        player_name = request.form.get('player_name', '').strip()
        
        if not player_name:
            flash("Player name cannot be empty!", category='error')
            return redirect(url_for('views.nfl_research_tool'))
        
        #var is the function that passes in the inputed name
        #use player_data for logic to display game log info
        player_data = get_player_game_log(player_name)
        
        if 'error' in player_data:
            flash(player_data['error'], category='error')
            return redirect(url_for('views.nfl_research_tool'))
        
        if 'game_log' in player_data:
            rec_per_game_bar_graph(player_data['game_log'])
        
        return render_template("research_tool.html", user=current_user, player_data=player_data, show_graph=True)
     
    return render_template("research_tool.html", user=current_user, show_graph=False)