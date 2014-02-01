#!venv/bin/python

from vsvlandb import app

app.config.from_object('configuration.Development')

if __name__ == '__main__':
    app.run(debug=True)
