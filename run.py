#!venv/bin/python

from vsvlandb import app

app.config.from_object('configuration.DevelopmentMySQL')

if __name__ == '__main__':
    app.run(debug=True)
