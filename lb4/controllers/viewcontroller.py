from jinja2 import Environment, FileSystemLoader

class ViewController:
    def __init__(self, currency_rates):
        self.currency_rates = currency_rates

    def __call__(self):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('rates.html')
        return template.render(rates=self.currency_rates.rates)