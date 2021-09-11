from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import pandas as pd
import glob
import time
import os
from datetime import date

views = Blueprint('views', __name__)
tesla_list_of_files = glob.glob('all_data/*')
tesla_latest = max(tesla_list_of_files, key=os.path.getctime)
vehicle_pd = pd.read_csv(tesla_latest)
vehicle_models = ['Model S', 'Model 3', 'Model X', 'Model Y']
vehicle_avail = ['Available Now', 'Pre-Order', 'On Hold']
# vehicle_data = vehicle_data[vehicle_data['image'].isnull() == False]
# vehicle_data = vehicle_data.sort_values(by=['price'])

@views.route('/', methods=['GET', 'POST'])
def home():
    vehicle_data = vehicle_pd

    model_s = vehicle_data[vehicle_data['model'] == "Model S"]
    model_3 = vehicle_data[vehicle_data['model'] == "Model 3"]
    model_x = vehicle_data[vehicle_data['model'] == "Model X"]
    model_y = vehicle_data[vehicle_data['model'] == "Model Y"]

    return render_template("home.html", user=current_user, data=vehicle_data, model_s=model_s, model_3=model_3, model_x=model_x, model_y=model_y)

@views.route('/vehicles/', methods=['GET', 'POST'])
def vehicles():
    vehicle_data = vehicle_pd
    data_filter = request.form.get('sort')
    check_dict = {}
    model_filter = request.form.getlist('modelfilters')
    year_filter = list(map(int, request.form.getlist('yearfilters')))
    dealer_filter = request.form.getlist('dealerfilters')
    avail_filter = request.form.getlist('availfilters')

    for arr in [model_filter, year_filter, dealer_filter, avail_filter]:
        for value in arr:
            check_dict[value] = 'checked'

    print(check_dict)

    print(f'year filter: {year_filter}')

    vehicle_years = sorted(list(vehicle_data['year'].drop_duplicates()), reverse=True)
    vehicle_dealers = list(vehicle_data['marketplace'].drop_duplicates())

    if request.method == 'POST':
        if len(year_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['year'].isin(year_filter)]
        if len(model_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['model'].isin(model_filter)]
        if len(dealer_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['marketplace'].isin(dealer_filter)]
        if len(avail_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['avail'].isin(avail_filter)]

        if data_filter:
            if data_filter == "priceLowToHigh":
                vehicle_data = vehicle_data.sort_values(by=['price'])
            if data_filter == "priceHighToLow":
                vehicle_data = vehicle_data.sort_values(by=['price'], ascending=False)
            if data_filter == "yearLowToHigh":
                vehicle_data = vehicle_data.sort_values(by=['year'])
            if data_filter == "yearHighToLow":
                vehicle_data = vehicle_data.sort_values(by=['year'], ascending=False)
            if data_filter == "milesLowToHigh":
                vehicle_data = vehicle_data.sort_values(by=['miles'])
            if data_filter == "milesHighToLow":
                vehicle_data = vehicle_data.sort_values(by=['miles'], ascending=False)

    print(vehicle_years)
    print(vehicle_dealers)

    return render_template("vehicles.html", user=current_user, data=vehicle_data, vehicle_years=vehicle_years, vehicle_models=vehicle_models, vehicle_dealers=vehicle_dealers, check_dict=check_dict, vehicle_avail=vehicle_avail)

@views.route('/vehicles/<model>/', methods=['GET', 'POST'])
def vehicles_model(model):
    vehicle_data = vehicle_pd
    data_filter = request.form.get('sort')
    check_dict = {}
    model_filter = request.form.getlist('modelfilters')
    year_filter = list(map(int, request.form.getlist('yearfilters')))
    dealer_filter = request.form.getlist('dealerfilters')
    avail_filter = request.form.getlist('availfilters')

    for arr in [model_filter, year_filter, dealer_filter, avail_filter]:
        for value in arr:
            check_dict[value] = 'checked'

    print(check_dict)

    print(f'year filter: {year_filter}')

    if model == 's':
        vehicle_data = vehicle_data[vehicle_data['model'] == 'Model S']
        check_dict['Model S'] = 'checked'
        vehicle_models = ['Model S']
    if model == '3':
        vehicle_data = vehicle_data[vehicle_data['model'] == 'Model 3']
        check_dict['Model 3'] = 'checked'
        vehicle_models = ['Model 3']
    if model == 'x':
        vehicle_data = vehicle_data[vehicle_data['model'] == 'Model X']
        check_dict['Model X'] = 'checked'
        vehicle_models = ['Model X']
    if model == 'y':
        vehicle_data = vehicle_data[vehicle_data['model'] == 'Model Y']
        check_dict['Model Y'] = 'checked'
        vehicle_models = ['Model Y']

    vehicle_years = sorted(list(vehicle_data['year'].drop_duplicates()), reverse=True)
    vehicle_dealers = list(vehicle_data['marketplace'].drop_duplicates())


    if request.method == 'POST':
        if len(year_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['year'].isin(year_filter)]
        if len(model_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['model'].isin(model_filter)]
        if len(dealer_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['marketplace'].isin(dealer_filter)]
        if len(avail_filter) > 0:
            vehicle_data = vehicle_data[vehicle_data['avail'].isin(avail_filter)]

        if data_filter:
            if data_filter == "priceLowToHigh":
                vehicle_data = vehicle_data.sort_values(by=['price'])
            if data_filter == "priceHighToLow":
                vehicle_data = vehicle_data.sort_values(by=['price'], ascending=False)
            if data_filter == "yearLowToHigh":
                vehicle_data = vehicle_data.sort_values(by=['year'])
            if data_filter == "yearHighToLow":
                vehicle_data = vehicle_data.sort_values(by=['year'], ascending=False)
            if data_filter == "milesLowToHigh":
                vehicle_data = vehicle_data.sort_values(by=['miles'])
            if data_filter == "milesHighToLow":
                vehicle_data = vehicle_data.sort_values(by=['miles'], ascending=False)

    print(vehicle_years)
    print(vehicle_dealers)

    return render_template("vehicles.html", user=current_user, data=vehicle_data, vehicle_years=vehicle_years, vehicle_models=vehicle_models, vehicle_dealers=vehicle_dealers, check_dict=check_dict, vehicle_avail=vehicle_avail)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')

        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
