from flask import Blueprint, request, redirect, render_template
from model import CurrencyRatesSingleton

bp = Blueprint("main", __name__)
rates_model = CurrencyRatesSingleton()

@bp.route('/')
def index():
    rates_model.fetch_rates()
    rates = rates_model.get_rates()
    return render_template('index.html', rates=rates)

@bp.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        codes = request.form.get('currencies')
        codes = [code.strip().upper() for code in codes.split(',') if code.strip()]
        rates_model.set_tracked(codes)
        return redirect('/')
    return render_template('update.html')