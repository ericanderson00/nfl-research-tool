from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user #this is why I need UserMixin in models.py
from .models import Note, PlayerInfo, GameLog, Subscription
from . import db
import json
from datetime import datetime



import json

views = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return render_template('landing.html')

@views.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        exisisting_sub = Subscription.query.filter_by(email=email).first()
        if exisisting_sub:
            flash('You are already subscribed!', category='error')
        else:
            new_sub = Subscription(email=email)
            db.session.add(new_sub)
            db.session.commit()
            flash('Thank you for subscribing! We will notifiy you when we go live.', category='success')
    else:
        flash('Please Enter a valid email address.', category='error')
    return redirect('/')


@views.route('/home', methods=['GET']) # home page and what ever is / will run 
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
    error_message = None
    #when submit happens
    if request.method == 'POST':
        
        #player name = whatever is in text field
        player_name = request.form.get('playerName')


        if player_name:
            search_results = PlayerInfo.query.filter(PlayerInfo.playerName.ilike(f'%{player_name}%')).all()
            if not search_results:
                error_message = f"No players found with the name '{player_name}'"
                
        

    return render_template("search.html", search_results=search_results, error_message=error_message)  
  

# @views.route('/playerProfile/<int:player_id>/<string:table_filters>/<string:bar_filters>/<string:year_filter>', methods=['GET','POST'])
@views.route('/playerProfile/<int:player_id>', methods=['GET','POST'])
@login_required
# def playerProfile(player_id, table_filters, bar_filters, year_filter):
def playerProfile(player_id):
    
    # sets current football season
    if datetime.now().month == 1 or datetime.now().month == 2:    
        curr_fb_season = datetime.now().year - 1
    else:
        curr_fb_season = datetime.now().year
        
        
    # gets the filters for stats from the url instead of the passed value
    table_filters = request.args.get('table_filters', '').split('+')
    bar_filters = request.args.get('bar_filters')
    year_filter = request.args.get('year_filter', curr_fb_season) 
    
    # table_filters = table_filters.split('+') if isinstance(table_filters, str) else table_filters
    barDataArr = []
    game_logs_asc_by_year = []
    recBettingLineArr = []
    
    #method that pulls betting line from api or scraper
    #--------------put right here------------------------#
    #|                                                   |
    #----------------------------------------------------#
    recBettingLine = 3.5
    
        
    # print(f"Searching for player with ID: {player_id}")
    
    
    player = PlayerInfo.query.get(player_id)
    print(PlayerInfo.query.get(player_id))
    
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
    
    #sets the default bar filter based off position
    if player.pos == 'QB':  
        bar_filters = 'passYards'
    elif player.pos == 'RB':  
        bar_filters = 'rushYards'
    elif player.pos == 'WR':  
        bar_filters = 'recYds'
    elif player.pos == 'TE':  
        bar_filters = 'recYds'
    else:
        bar_filters = 'touchdowns' # For all other positions, show all stats
    
    
    if request.method == 'POST':
        table_filters = request.form.getlist('tableFilter')
        bar_filters = request.form.get('barFilter')
        year_filter = request.form.get('yearFilter')
        print(f"Selected table Filter: {table_filters}")
        print(f"Selected year Filter: {year_filter}")
        
    

    #descending
    game_logs_desc = GameLog.query.filter_by(playerID=player_id).order_by(
        GameLog.year.desc(), GameLog.week.desc()
    ).all()
    
    #ascending
    game_logs_asc_all = GameLog.query.filter_by(playerID=player_id).order_by(
        GameLog.year.asc(), GameLog.week.asc()
    ).all()
    
    #filter game log by year
    if year_filter == 'all':
        game_logs_asc_by_year = game_logs_asc_all
    else:
        game_logs_asc_by_year = GameLog.query.filter(
            GameLog.playerID==player_id,
            GameLog.year==year_filter
            ).order_by(GameLog.week.asc()).all()
    
    
    print(f"Selected bar filter: {bar_filters}")
    
    if year_filter == 'all':
        if bar_filters == 'passYards':
            for i in game_logs_asc_all:
                barDataArr.append(i.passYards)
        elif bar_filters == 'rushYards':
            for i in game_logs_asc_all:
                barDataArr.append(i.rushYards)
        elif bar_filters == 'recYds':
            for i in game_logs_asc_all:
                barDataArr.append(i.recYds)
        elif bar_filters == 'receptions':
            for i in game_logs_asc_all:
                barDataArr.append(i.receptions)
                recBettingLineArr.append(recBettingLine)
        elif bar_filters == 'touchdowns':
            for i in game_logs_asc_all:
                totalTD = i.recTD + i.rushTD
                barDataArr.append(totalTD)
        
    else:
        if bar_filters == 'passYards':
            for i in game_logs_asc_by_year:
                barDataArr.append(i.passYards)
        elif bar_filters == 'rushYards':
            for i in game_logs_asc_by_year:
                barDataArr.append(i.rushYards)
        elif bar_filters == 'recYds':
            for i in game_logs_asc_by_year:
                barDataArr.append(i.recYds)
        elif bar_filters == 'receptions':
            for i in game_logs_asc_by_year:
                barDataArr.append(i.receptions)
                recBettingLineArr.append(recBettingLine)
        elif bar_filters == 'touchdowns':
            for i in game_logs_asc_by_year:
                totalTD = i.recTD + i.rushTD
                barDataArr.append(totalTD)
                      
    # print(game_logs_asc_by_year)
    # print(game_logs_asc_all)
    
    # print(barDataArr)
    # print(len(barDataArr))
    gamelog_to_dict = []
    for gamelog in game_logs_asc_by_year:
        gamelog_to_dict.append(gamelog.to_dict())
    
    # bettingLine = 5.5
    
    print(year_filter)
    return render_template(
        "player_profile.html", 
        player=player, 
        game_logs_desc=game_logs_desc,
        game_logs_asc_all=game_logs_asc_all,
        game_logs_asc_by_year=gamelog_to_dict, 
        table_filters=table_filters,
        bar_filters=bar_filters,
        bar_data=barDataArr,
        year_filter=year_filter,\
        betting_line=recBettingLineArr
        # game_logs=game_logs,
    )
    
    
    
# Testing api endpoint needs fixing
@views.route('/api/gamelogs', methods=['GET'])
def get_gamelogs():
    # Get query parameters
    year = request.args.get('year', type=int)
    week = request.args.get('week', type=int)

    # Base query
    query = GameLog.query

    # Apply filters based on query parameters
    if year:
        query = query.filter(GameLog.year == year)
    if week:
        query = query.filter(GameLog.week == week)

    # Fetch the filtered results
    game_logs = query.all()

    # Serialize the results into JSON
    results = [
        {
            "id": gamelog.id,
            "week": gamelog.week,
            "playerOpp": gamelog.playerOpp,
            "year": gamelog.year,
            "touchdowns": gamelog.recTD + gamelog.rushTD,
            "passYards": gamelog.passYards,
            "rushYards": gamelog.rushYards,
            "recYds" : gamelog.recYds,
            "receptions": gamelog.receptions,
            "rushTD" : gamelog.rushTD,
            "recTD" : gamelog.recTD
            
        } for gamelog in game_logs
    ]

    return jsonify(results)
    