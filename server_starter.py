import numpy as np
from flask import Flask, jsonify, request
from scipy.stats import beta

# create an app
app = Flask(__name__)


class Bandit:
    def __init__(self, name):
        self.name = name
        self.a = 1
        self.b = 1

        self.is_clicked = True  # флаг для обработки ситуации когда реклама была показана но не кликнута

    def sample(self):
        return beta.rvs(self.a, self.b)

    def update(self, click):
        self.a += click
        self.b += 1 - click


# initialize bandits
banditA = Bandit("A")
banditB = Bandit("B")
bandits = [banditA, banditB]


@app.route("/get_ad")
def get_ad():
    # если реклама была показана и не кликнута
    for b in bandits:
        if not b.is_clicked:
            b.update(0)
            b.is_clicked = True

    if banditA.sample() >= banditB.sample():
        banditA.is_clicked = False
        return jsonify({"advertisement_id": "A"})

    banditB.is_clicked = False
    return jsonify({"advertisement_id": "B"})


@app.route("/click_ad", methods=["POST"])
def click_ad():
    result = "OK"
    if request.form["advertisement_id"] == "A":
        banditA.is_clicked = True
        banditA.update(1)
    elif request.form["advertisement_id"] == "B":
        banditB.is_clicked = True
        banditB.update(1)
    else:
        result = "Invalid Input."

    # nothing to return really
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8888")
