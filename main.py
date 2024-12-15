import os
import time
from web_functions import create_charts as cc, process_filters as pf, db_interactions as db

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
vacancies, companies, tech, experience = None, None, None, None

def fetch_data_from_db():
    global vacancies, companies, tech, experience
    vacancies = db.read_table('warehouse', 'vacancy', index='id')
    companies = db.read_table('warehouse', 'company', index='id')
    tech = db.read_table('warehouse', 'technology', index='id')
    experience = db.read_table('warehouse', 'experience', index='id')


@app.route('/', methods=['GET', 'POST'])
def home():
    dropdown_data, default_values = pf.get_filters_options(["technology", "experience", "work_format"])
    selected_values = request.form.to_dict() if request.method == 'POST' else default_values
    tech_value, exp_value, format_value = pf.get_filters_values(selected_values)

    return render_template('index.html',
                           vacancies=cc.recent_vacancies(vacancies, companies, technology=tech_value,
                                                           experience=exp_value,
                                                           work_format=format_value),
                           dropdown_data=dropdown_data, selected_values=selected_values)

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    dropdown_data, default_values = pf.get_filters_options(["technology", "experience", "work_format"])
    selected_values = request.form.to_dict() if request.method == 'POST' else default_values
    tech_value, exp_value, format_value = pf.get_filters_values(selected_values)

    return render_template('timeline.html',
                           graph_json=cc.create_time_chart(vacancies, technology=tech_value,
                                                           experience=exp_value,
                                                           work_format=format_value),
                           dropdown_data=dropdown_data, selected_values=selected_values)

@app.route('/work_format', methods=['GET', 'POST'])
def work_format():
    dropdown_data, default_values = pf.get_filters_options(["technology"])
    selected_values = request.form.to_dict() if request.method == 'POST' else default_values
    tech_value, _,_ = pf.get_filters_values(selected_values)

    return render_template('work_format.html',
                           graph_json=cc.create_work_format_chart(vacancies, technology=tech_value),
                           dropdown_data=dropdown_data, selected_values=selected_values)

@app.route('/technologies', methods=['GET', 'POST'])
def technologies():
    dropdown_data, default_values = pf.get_filters_options(["experience"])
    selected_values = request.form.to_dict() if request.method == 'POST' else default_values
    _, exp_value, _ = pf.get_filters_values(selected_values)

    return render_template('technologies.html',
                           graph_json=cc.create_technologies_chart(vacancies, tech, experience=exp_value),
                           dropdown_data=dropdown_data, selected_values=selected_values)

@app.route('/top_companies', methods=['GET', 'POST'])
def top_companies():
    dropdown_data, default_values = pf.get_filters_options(["technology"])
    selected_values = request.form.to_dict() if request.method == 'POST' else default_values
    tech_value, _, _ = pf.get_filters_values(selected_values)

    return render_template('top_companies.html',
                           graph_json=cc.create_top_companies(vacancies, companies, technology=tech_value),
                           dropdown_data=dropdown_data, selected_values=selected_values)

if __name__ == '__main__':
    fetch_data_from_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_data_from_db, 'interval', minutes=3)
    scheduler.start()

    print("Waiting for data to load...")
    time.sleep(60)

    print("Starting Flask app...")
    app.run(debug=True)