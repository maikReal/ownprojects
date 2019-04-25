import redis
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/api/v1/get_rabbit')
def rabbit():
    return render_template('rabbitmq.html')


@app.route('/api/v1/get_mongo')
def mongo():
    return render_template('mongodb.html')


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)