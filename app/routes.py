from app import app, db, bcrypt
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user
from app.forms import RegisterForm, LoginForm
from app.models import UserModel

from app.data_for_state_overview import StateData
from app.data_for_data_timeline import GraphData
from app.data_for_county_maps import MapData


@app.route('/')
@login_required
def index():
    title = 'home'
    data = StateData()
    return render_template('index.html', title=title,
                           cases_and_deaths_all_time_data=data.query_all_time_cases_and_deaths(),
                           cases_and_deaths_past_day_data=data.query_past_day_cases_and_deaths(),
                           cases_and_deaths_past_week_data=data.query_past_week_cases_and_deaths(),
                           cases_and_deaths_past_month_data=data.query_past_month_cases_and_deaths(),
                           test_and_positivity_all_time_data=data.query_all_time_test_and_positivity(),
                           test_past_day_data=data.query_past_day_test(),
                           test_and_positivity_past_week_data=data.query_past_week_test_and_positivity(),
                           test_and_positivity_past_month_data=data.query_past_month_test_and_positivity(),
                           vaccine_data=data.query_vaccine_data(),
                           graphJSON_hospitalizations=data.draw_hospitalizations())



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'register'
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)

        user = UserModel(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Congrats, registration success', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title=title, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = 'login'
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = UserModel.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Login success', category='success')
            return redirect(url_for('index'))
        flash('User not exists or password not match', category='danger')
    return render_template('login.html', title=title, form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/data_timeline')
@login_required
def data_timeline():
    title = 'Data Timeline'
    data = GraphData()
    return render_template('data_timeline.html', title=title,
                           graphJSON_cases=data.graph_cases(),
                           graphJSON_deaths=data.graph_deaths(),
                           graphJSON_test_positivity=data.graph_test_positivity(),
                           graphJSON_hospitalizations=data.graph_hospitalizations(),
                           graphJSON_vaccinations=data.graph_vaccinations())


@app.route('/county_maps')
@login_required
def county_maps():
    title = 'County Maps'
    data = MapData()
    return render_template('county_maps.html', title=title,
                           mapJSON_acc_confirmed=data.map_cumulative_data_total_cases(),
                           mapJSON_acc_deaths=data.map_cumulative_data_total_deaths(),
                           mapJSON_daily_confirmed=data.map_daily_data_and_demo_cases(),
                           mapJSON_daily_deaths=data.map_daily_data_and_demo_deaths(),
                           graphJSON_racial=data.graph_racial_breakdown())
