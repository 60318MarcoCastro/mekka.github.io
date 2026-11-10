"""Crea las tablas y carga los datos de gestion_taller.sql (ejecutar una sola vez).

Uso:  python init_db.py
Usa la misma configuración que app.py (variables de entorno o Wampserver)
y pide la contraseña del usuario admin (o la toma de ADMIN_PASSWORD).
"""
import getpass
import os

import mysql.connector

from app import DB_CONFIG

SQL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gestion_taller.sql')


def main():
    config = dict(DB_CONFIG)
    database = config.pop('database')

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # En tu PC se crea la base; en PythonAnywhere ya existe (se crea en la pestaña Databases).
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{database}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
    except mysql.connector.Error as err:
        print(f"Aviso: no se pudo crear la base ({err.msg}); se usará la existente.")
    cursor.execute(f"USE `{database}`")

    with open(SQL_FILE, encoding='utf-8') as f:
        sql = f.read()

    for statement in sql.split(';'):
        lines = [l for l in statement.splitlines() if not l.strip().startswith('--')]
        statement = '\n'.join(lines).strip()
        if statement:
            cursor.execute(statement)
    conn.commit()

    # Contraseña del administrador: se pide aquí para que nunca esté en GitHub.
    password = os.environ.get('ADMIN_PASSWORD') or getpass.getpass(
        'Escribe la contraseña para el usuario admin (no se mostrará): ')
    while not password.strip():
        password = getpass.getpass('La contraseña no puede estar vacía. Escríbela de nuevo: ')
    cursor.execute("UPDATE usuarios SET password = %s WHERE usuario = 'admin'", (password,))
    conn.commit()
    print("Contraseña del usuario admin guardada.")

    cursor.execute("SHOW TABLES")
    print("Tablas en", database + ":", ", ".join(t[0] for t in cursor.fetchall()))
    cursor.close()
    conn.close()


if __name__ == '__main__':
    main()
