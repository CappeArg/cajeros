from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('cajeros.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS cajeros (id INTEGER PRIMARY KEY, nombre TEXT, estado TEXT, ultima_actualizacion TEXT)')
    conn.execute("INSERT OR IGNORE INTO cajeros (id, nombre, estado, ultima_actualizacion) VALUES (1, 'Cajero 1', 'Desconocido', ?)", (datetime.now().isoformat(),))
    conn.execute("INSERT OR IGNORE INTO cajeros (id, nombre, estado, ultima_actualizacion) VALUES (2, 'Cajero 2', 'Desconocido', ?)", (datetime.now().isoformat(),))
    conn.commit()
    conn.close()

init_db()

@app.route('/cajeros', methods=['GET'])
def get_cajeros():
    conn = get_db_connection()
    cajeros = conn.execute('SELECT * FROM cajeros').fetchall()
    conn.close()
    return jsonify([dict(cajero) for cajero in cajeros])

@app.route('/cajeros/<int:id>', methods=['PUT'])
def update_cajero(id):
    estado = request.json['estado']
    conn = get_db_connection()
    conn.execute('UPDATE cajeros SET estado = ?, ultima_actualizacion = ? WHERE id = ?', (estado, datetime.now().isoformat(), id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Estado actualizado'}), 200

if __name__ == '__main__':
    app.run(debug=True)