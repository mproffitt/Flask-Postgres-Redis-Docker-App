#!/usr/bin/env python3
from flask import Flask
from flask import render_template, request, redirect, url_for
from redis import Redis
from src.database.posgre import get_db_engine
from sqlalchemy import text
import sqlalchemy as sa
import pickle

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

db_engine = get_db_engine()

def cache():
    '''
    Cache the database results in Redis
    '''
    sql_qry = "SELECT * FROM PROD.test_table ORDER BY username;"
    result = None
    with db_engine.connect() as conn:
        result = conn.execute(text(sql_qry)).mappings().all()
        redis.set('results', pickle.dumps(result))

@app.route('/')
def hello():
    '''
    Simple cache hit counter
    '''
    redis.incr('hits')
    cnt = redis.get('hits').decode("utf-8")
    return render_template('displayMenu.html', hits=cnt)

@app.route('/dbdisplay')
def db_display():
    '''
    Display the database results
    '''
    results=redis.get('results')
    return render_template('displayDbData.html', result=pickle.loads(results))

@app.route('/dbcapture', methods=['GET', 'POST'])
def db_capture():
    '''
    Capture the data from the form and insert into the database
    '''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        sql_stmt = f'''INSERT INTO PROD.test_table (username, email)
                       VALUES ('{name}', '{email}')
                    '''
        with db_engine.connect() as conn:
            conn.execute(text(sql_stmt))
            conn.commit()
        cache()
        return redirect(url_for('db_display'))
    return render_template('captureDbData.html')


@app.route('/dbdelete/<name>')
def db_delete(name):
    '''
    Delete the named user from the database
    '''
    sql_stmt = f'''DELETE FROM PROD.test_table WHERE username = '{name}';'''
    with db_engine.connect() as conn:
        conn.execute(text(sql_stmt))
        conn.commit()
    cache()
    return redirect(url_for('db_display'))


@app.route('/dbupdate/<name>', methods=['GET', 'POST'])
def db_update(name):
    '''
    Update the named user in the database
    '''
    if request.method == 'GET':
        sql_stmt = f'''SELECT * FROM PROD.test_table
                       WHERE username = '{name}';
                    '''
        result = None
        with db_engine.connect() as conn:
            result = conn.execute(text(sql_stmt))

        for item in result:
            name = item[0]
            email = item[1]

        return render_template('editDbData.html', name=name, email=email)

    # Default POST
    username = request.form['username']
    email = request.form['email']
    updt_sql_stmt = f'''UPDATE PROD.test_table
                        SET username = '{username}',
                            email = '{email}'
                        WHERE username = '{name}';'''
    with db_engine.connect() as conn:
        conn.execute(text(updt_sql_stmt))
        conn.commit()
    cache()
    return redirect(url_for('db_display'))

def create_table():
    '''
    Create the database and table
    '''
    sql_stmt = '''CREATE TABLE PROD.test_table
                  (username VARCHAR(50) PRIMARY KEY,
                   email VARCHAR(50));
               '''
    if not db_engine.dialect.has_table(db_engine, 'test_table', schema='PROD'):
        with db_engine.connect() as conn:
            conn.execute(text(sql_stmt))
            conn.commit()
    cache()

def create_schema():
    '''
    Create the schema
    '''
    sql_stmt = '''CREATE SCHEMA PROD;
               '''

    if not db_engine.dialect.has_schema(db_engine, 'PROD'):
        with db_engine.connect() as conn:
            conn.execute(text(sql_stmt))
            conn.commit()
    create_table()

def create_db():
    '''
    Create the database
    '''
    sql_stmt = '''CREATE DATABASE case_db;
               '''
    with db_engine.connect() as conn:
        conn.execute(text(sql_stmt))
        conn.commit()

if __name__ == '__main__':
    create_db()
    create_schema()
    app.run(host="0.0.0.0", debug=True, port=80)
