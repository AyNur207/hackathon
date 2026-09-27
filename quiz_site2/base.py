from flask import Flask, render_template, request, redirect, url_for
from data import TESTS

app = Flask(__name__)


@app.route("/")
def index():
    """Главная страница — три карточки."""
    return render_template("base.html")


@app.route("/topics")
def topics():
    """Выбор темы теста (спорт, танцы, творчество)."""
    return render_template("topics.html", tests=TESTS)


@app.route("/tests/<topic>")
def tests(topic):
    """Страница прохождения теста по выбранной теме."""
    if topic not in TESTS:
        return redirect(url_for("index"))
    return render_template("tests.html", topic=topic, test=TESTS[topic])


@app.route("/result", methods=["POST"])
def result():
    """Обработка ответов и вывод результата."""
    topic = request.form.get("topic")
    if topic not in TESTS:
        return redirect(url_for("index"))

    test = TESTS[topic]
    counts = {"А": 0, "Б": 0, "В": 0, "Г": 0}

    for key, value in request.form.items():
        if key.startswith("answers_") and value in counts:
            counts[value] += 1

    winner = max(counts, key=counts.get)
    top_result = test["results"][winner]

    total = sum(counts.values()) or 1
    percent = round(counts[winner] / total * 100)

    return render_template(
        "result.html",
        topic=topic,
        test=test,
        result=top_result,
        winner=winner,
        percent=percent,
    )


# Заглушки для кнопок в шапке и на главной, чтобы не было 404
@app.route("/register")
def register():
    return "Страница регистрации в разработке"


@app.route("/login")
def login():
    return "Страница входа в разработке"


@app.route("/announcements")
def announcements():
    return "Раздел объявлений в разработке"


@app.route("/maps")
def maps():
    return "Карты кампуса в разработке"


if __name__ == "__main__":
    app.run(debug=True)
