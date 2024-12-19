from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user #this is why I need UserMixin in models.py
from .models import Note, PlayerInfo, GameLog
from . import db
import json



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
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id: #if the user who is signed in owns the note then...
            db.session.delete(note)
            db.session.commit()
                    
    return jsonify({})



@views.route('/searchPlayer', methods=['GET','POST'])
@login_required
def searchPlayer():
    
    search_results = []
    selected_filters = []
    error_message = None
    #when submit happens
    if request.method == 'POST':
        
        #player name = whatever is in text field
        player_name = request.form.get('playerName')
        selected_filters = request.form.getlist('statsFilter') or selected_filters


        if player_name:
            search_results = PlayerInfo.query.filter(PlayerInfo.playerName.ilike(f'%{player_name}%')).all()
            if not search_results:
                error_message = f"No players found with the name '{player_name}'"
                
        

    return render_template("search.html", search_results=search_results, error_message=error_message)  
  

@views.route('/playerProfile/<int:player_id>', methods=['GET','POST'])
@login_required
def playerProfile(player_id):
    
    # print(f"Searching for player with ID: {player_id}")
    
    table_filters = ['passing', 'rushing', 'receiving']
    chart_filters = []
    player = PlayerInfo.query.get(player_id)
    print(PlayerInfo.query.get(player_id))
    game_logs = []
    
    # sets the default filter based off position
    if player.pos == 'QB':  
        table_filters = ['passing']
    elif player.pos == 'RB':  
        table_filters = ['rushing']
    elif player.pos == 'WR':  
        table_filters = ['receiving']
    elif player.pos == 'TE':  
        table_filters = ['receiving']
    else:
        table_filters = ['passing', 'rushing', 'receiving']  # For all other positions, show all stats
    
    if request.method == 'POST':
        table_filters = request.form.getlist('statsFilter') or table_filters
        
    game_logs = GameLog.query.filter_by(playerID=player_id).order_by(
        GameLog.year.desc(), GameLog.week.desc()
    ).all()  
    
    return render_template(
        "player_profile.html", 
        player=player, 
        game_logs=game_logs, 
        table_filters=table_filters
    )