from flask import Flask, request, send_from_directory
from conf import VERIFY_TOKEN
# from threading import thread
import core


traitement = core.Traitement()
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
    elif request.method == "POST":
        # recuperation de json via facebook
        body = request.get_json()
        # print(body)
        traitement._analyse(body)
        # proc = Thread(target=traitement._analyse, args=[body])
        # proc.start()
    return "receive", 200


@app.route("/<filename>")
def get_file(filename):
    try:
        return send_from_directory(
            './photo/',
            path=filename,
            as_attachment=True
        )
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run(debug=True, port=7000)
