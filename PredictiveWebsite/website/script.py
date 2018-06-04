from flask import Flask, render_template, request
from ML_model.model import PredictPrice

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/form_checking')
def for_checking():

    year = int(request.args.getlist('form1')[0])
    distance = int(request.args.getlist('form2')[0])
    type = str(request.args.getlist('form3')[0])
    engine = float(request.args.getlist('form4')[0])
    transmission = str(request.args.getlist('form5')[0])
    fuel = str(request.args.getlist('form6')[0])
    drive = str(request.args.getlist('form7')[0])
    power = int(request.args.getlist('form8')[0])

    comps = [year, distance, type, engine, transmission, fuel, drive, power]

    model = PredictPrice(comps)
    price = model.predict_p()
    price = price[0].round(1)

    print(request.url_rule.rule)
    return render_template('tmp.html', price=price)


if __name__ == '__main__':
    app.run()
