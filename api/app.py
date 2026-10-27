from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

def get_conn():
    return mysql.connector.connect(
        host=os.environ.get('DB_HOST', 'db'),
        user=os.environ.get('DB_USER', 'holamundo'),
        password=os.environ.get('DB_PASS', 'holamundo'),
        database=os.environ.get('DB_NAME', 'holamundo')
    )

@app.route('/api/mensajes')
def mensajes():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute('CREATE TABLE IF NOT EXISTS mensajes (id INT AUTO_INCREMENT PRIMARY KEY, mensaje VARCHAR(255) NOT NULL, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    cur.execute('SELECT COUNT(*) as total FROM mensajes')
    res = cur.fetchone()
    if res['total'] == 0:
        cur.execute("INSERT INTO mensajes (mensaje) VALUES ('¡Bienvenido!')")
        conn.commit()
    cur.execute('SELECT * FROM mensajes ORDER BY id DESC')
    datos = cur.fetchall()
    cur.close()
    conn.close()
    for d in datos:
        if hasattr(d['fecha'], 'strftime'):
            d['fecha'] = d['fecha'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
