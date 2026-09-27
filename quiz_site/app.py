from flask import Flask, render_template, request, redirect, url_for
from data import TESTS

app = Flask(__name__)


@app.route("/")
def index():
    """Главная страница — выбор темы."""
    return render_template("index.html", tests=TESTS)


@app.route("/test/<topic>")
def test(topic):
    """Страница прохождения теста."""
    if topic not in TESTS:
        return redirect(url_for("index"))
    return render_template("test.html", topic=topic, test=TESTS[topic])


@app.route("/result", methods=["POST"])
def result():
    """Обработка ответов и вывод результата."""
    topic = request.form.get("topic")
    if topic not in TESTS:
        return redirect(url_for("index"))

    test = TESTS[topic]
    counts = {"А": 0, "Б": 0, "В": 0, "Г": 0}

    # Считаем ответы (в форме поля answers_0, answers_1, ...)
    for key, value in request.form.items():
        if key.startswith("answers_") and value in counts:
            counts[value] += 1

    # Находим букву-победителя
    winner = max(counts, key=counts.get)
    top_result = test["results"][winner]

    # Считаем процент совпадения
    total = sum(counts.values()) or 1
    percent = round(counts[winner] / total * 100)

    return render_template(
        "result.html",
        topic=topic,  # Передаем тему, чтобы кнопка "Пройти заново" работала
        test=test,
        result=top_result,
        winner=winner,
        percent=percent,
    )


if __name__ == "__main__":
    app.run(debug=True)
