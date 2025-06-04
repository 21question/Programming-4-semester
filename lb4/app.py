from main import CurrencyRates
from controllers.databasecontroller import CurrencyRatesCrud
from controllers.viewcontroller import ViewController

if __name__ == "__main__":
    try:
        model = CurrencyRates(['USD', 'EUR', 'GBP'])
        db = CurrencyRatesCrud(model)
        db.create()
        data = db.read()
        print("Данные из БД:", data)

        view = ViewController(model)
        html = view()
        print(html)

    except Exception as e:
        print(f"Ошибка: {e}")