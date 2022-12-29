from flask import Flask, render_template, request

import datetime

messages = [{'name': 'name one',
             'email': 'email one'},
            {'name': 'name two',
             'email': 'email two'}
            ]

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    @app.route('/')
    def index():
        # today = datetime.datetime()
        # day_name = today.strftime("%A")
        day_name='dayname'
        print(day_name)
        return render_template('index.html', day=day_name, messages=messages)

    @app.route('/info')
    def info_page():
        return render_template("info.html")

    @app.route('/info')
    def info_add_page():
        if request.method == "GET":
            return render_template(
                "info.html"
            )
            
        else:
            form_title = request.form["title"]
            person_name = request.form["name"]
            # email = Email(form_title, name=person_name if person_name else None)
    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)


#https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
