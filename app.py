import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_taller')

# Configuración de conexión a la Base de Datos.
# En tu PC usa los valores de Wampserver; en el servidor (PythonAnywhere)
# se toman de las variables de entorno definidas en el archivo WSGI.
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'gestion_taller'),
    'port': int(os.environ.get('DB_PORT', '3306')),
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def ejecutar(sql, params=(), mensaje_error='No se pudo completar la operación.'):
    """Ejecuta una instrucción de escritura (INSERT/UPDATE/DELETE).
    Si MySQL la rechaza (dato duplicado o registro en uso), muestra un aviso
    en la página en lugar de un error."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        conn.rollback()
        flash(mensaje_error, 'error')
        return False
    finally:
        cursor.close()
        conn.close()


def consultar(sql, params=(), uno=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params)
    resultado = cursor.fetchone() if uno else cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado


# --- 0. INICIO DE SESIÓN (tabla usuarios) ---
@app.before_request
def requiere_login():
    if request.endpoint in ('login', 'static'):
        return None
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = consultar(
            "SELECT usuario FROM usuarios WHERE usuario = %s AND password = %s AND password <> ''",
            (request.form['usuario'], request.form['password']),
            uno=True,
        )
        if usuario:
            session['usuario'] = usuario['usuario']
            return redirect(url_for('index'))
        flash('Usuario o contraseña incorrectos.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# --- 1. RUTA PRINCIPAL ---
@app.route('/')
def index():
    return render_template('index.html')


# --- 2. MÓDULO DE CLIENTES ---
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'POST':
        campos = ['curp', 'nombre', 'apellidos', 'direccion', 'telefono']
        valores = tuple(request.form[c].strip() for c in campos)
        ejecutar(
            "INSERT INTO cliente (curp, nombre, apellidos, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
            valores,
            'Ya existe un cliente con esa CURP.',
        )
        return redirect(url_for('clientes'))

    lista_clientes = consultar("SELECT * FROM cliente ORDER BY id_cliente")
    return render_template('clientes.html', clientes=lista_clientes)


@app.route('/eliminar_cliente/<string:curp>')
def eliminar_cliente(curp):
    ejecutar(
        "DELETE FROM cliente WHERE curp = %s",
        (curp,),
        'No se puede eliminar el cliente porque tiene vehículos registrados. Elimina primero sus vehículos.',
    )
    return redirect(url_for('clientes'))


# --- 3. MÓDULO DE VEHÍCULOS ---
@app.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos():
    if request.method == 'POST':
        placas = request.form['placas'].strip().upper()
        cliente = consultar("SELECT id_cliente FROM cliente WHERE curp = %s",
                            (request.form['curp_cliente'],), uno=True)
        if not cliente:
            flash('El cliente seleccionado no existe.', 'error')
        else:
            ejecutar(
                """
                INSERT INTO vehiculo (placas, modelo, color, fecha_entrada, hora_entrada, id_cliente)
                VALUES (%s, %s, %s, CURDATE(), CURTIME(), %s)
                """,
                (placas, request.form['modelo'], request.form['color'], cliente['id_cliente']),
                'Ya existe un vehículo con esas placas.',
            )
        return redirect(url_for('vehiculos'))

    lista_vehiculos = consultar("""
        SELECT v.*, c.nombre, c.apellidos
        FROM vehiculo v
        JOIN cliente c ON v.id_cliente = c.id_cliente
        ORDER BY v.id_vehiculo
    """)
    lista_clientes = consultar("SELECT curp, nombre, apellidos FROM cliente ORDER BY nombre")
    return render_template('vehiculos.html', vehiculos=lista_vehiculos, clientes=lista_clientes)


@app.route('/eliminar_vehiculo/<string:placas>')
def eliminar_vehiculo(placas):
    ejecutar(
        "DELETE FROM vehiculo WHERE placas = %s",
        (placas,),
        'No se puede eliminar el vehículo porque tiene reparaciones registradas.',
    )
    return redirect(url_for('vehiculos'))


# --- 4. MÓDULO DE MECÁNICOS ---
@app.route('/mecanicos', methods=['GET', 'POST'])
def mecanicos():
    if request.method == 'POST':
        campos = ['nombre', 'apellidos', 'telefono']
        ejecutar(
            "INSERT INTO mecanico (nombre, apellidos, telefono) VALUES (%s, %s, %s)",
            tuple(request.form[c] for c in campos),
        )
        return redirect(url_for('mecanicos'))

    lista_mecanicos = consultar("SELECT * FROM mecanico ORDER BY id_mecanico")
    return render_template('mecanicos.html', mecanicos=lista_mecanicos)


@app.route('/eliminar_mecanico/<int:id_mecanico>')
def eliminar_mecanico(id_mecanico):
    ejecutar(
        "DELETE FROM mecanico WHERE id_mecanico = %s",
        (id_mecanico,),
        'No se puede eliminar el mecánico porque está asignado a una o más reparaciones.',
    )
    return redirect(url_for('mecanicos'))


# --- 5. MÓDULO DE REFACCIONES ---
@app.route('/refacciones', methods=['GET', 'POST'])
def refacciones():
    if request.method == 'POST':
        ejecutar(
            "INSERT INTO refaccion (nombre, precio_unitario) VALUES (%s, %s)",
            (request.form['nombre'], request.form['precio_unitario']),
        )
        return redirect(url_for('refacciones'))

    lista_refacciones = consultar("SELECT * FROM refaccion ORDER BY id_refaccion")
    return render_template('refacciones.html', refacciones=lista_refacciones)


@app.route('/eliminar_refaccion/<int:id_refaccion>')
def eliminar_refaccion(id_refaccion):
    ejecutar(
        "DELETE FROM refaccion WHERE id_refaccion = %s",
        (id_refaccion,),
        'No se puede eliminar la refacción porque ya se usó en una reparación.',
    )
    return redirect(url_for('refacciones'))


# --- 6. MÓDULO DE REPARACIONES ---
@app.route('/reparaciones', methods=['GET', 'POST'])
def reparaciones():
    if request.method == 'POST':
        vehiculo = consultar("SELECT id_vehiculo FROM vehiculo WHERE placas = %s",
                             (request.form['placas_vehiculo'],), uno=True)
        if not vehiculo:
            flash('El vehículo seleccionado no existe.', 'error')
        else:
            ejecutar(
                """
                INSERT INTO reparacion (id_vehiculo, id_mecanico_principal, fecha_inicio, mano_obra)
                VALUES (%s, %s, CURDATE(), %s)
                """,
                (vehiculo['id_vehiculo'], request.form['id_mecanico_asignado'],
                 request.form['precio_mano_obra']),
                'No se pudo registrar la reparación (revisa el vehículo y el mecánico).',
            )
        return redirect(url_for('reparaciones'))

    lista_reparaciones = consultar("""
        SELECT
            r.id_reparacion, r.fecha_inicio, r.fecha_fin,
            r.mano_obra AS precio_mano_obra,
            v.placas AS placas_vehiculo, v.modelo,
            m.nombre AS nombre_mecanico,
            m.apellidos AS apellidos_mecanico,
            IFNULL(
                GROUP_CONCAT(DISTINCT CONCAT(m_ayuda.nombre, ' ', m_ayuda.apellidos) SEPARATOR ', '),
                'Sin ayudantes'
            ) AS ayudantes
        FROM reparacion r
        JOIN vehiculo v ON r.id_vehiculo = v.id_vehiculo
        JOIN mecanico m ON r.id_mecanico_principal = m.id_mecanico
        LEFT JOIN mecanico_reparacion eq ON r.id_reparacion = eq.id_reparacion
        LEFT JOIN mecanico m_ayuda ON eq.id_mecanico = m_ayuda.id_mecanico
        GROUP BY r.id_reparacion, r.fecha_inicio, r.fecha_fin, r.mano_obra,
                 v.placas, v.modelo, m.nombre, m.apellidos
        ORDER BY r.id_reparacion
    """)

    return render_template(
        'reparaciones.html',
        reparaciones=lista_reparaciones,
        vehiculos=consultar("SELECT placas, modelo FROM vehiculo ORDER BY placas"),
        mecanicos=consultar("SELECT id_mecanico, nombre, apellidos FROM mecanico ORDER BY nombre"),
        refacciones=consultar("SELECT * FROM refaccion ORDER BY nombre"),
    )


@app.route('/terminar_reparacion/<int:id_reparacion>')
def terminar_reparacion(id_reparacion):
    ejecutar("UPDATE reparacion SET fecha_fin = CURDATE() WHERE id_reparacion = %s AND fecha_fin IS NULL",
             (id_reparacion,))
    return redirect(url_for('reparaciones'))


# --- 7. ASIGNAR MECÁNICO DE APOYO (EQUIPO) ---
@app.route('/agregar_mecanico_equipo', methods=['POST'])
def agregar_mecanico_equipo():
    ejecutar(
        "INSERT IGNORE INTO mecanico_reparacion (id_reparacion, id_mecanico) VALUES (%s, %s)",
        (request.form['id_reparacion'], request.form['id_mecanico_ayudante']),
    )
    return redirect(url_for('reparaciones'))


# --- 8. ASIGNAR REFACCIÓN A REPARACIÓN ---
@app.route('/agregar_refaccion_reparacion', methods=['POST'])
def agregar_refaccion_reparacion():
    id_reparacion = request.form['id_reparacion']
    id_refaccion = request.form['id_refaccion']
    cantidad = int(request.form['cantidad'])

    refaccion = consultar("SELECT precio_unitario FROM refaccion WHERE id_refaccion = %s",
                          (id_refaccion,), uno=True)
    if refaccion:
        ejecutar(
            """
            INSERT INTO refaccion_reparacion (id_reparacion, id_refaccion, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)
            """,
            (id_reparacion, id_refaccion, cantidad, refaccion['precio_unitario']),
        )
    return redirect(url_for('reparaciones'))


@app.route('/eliminar_reparacion/<int:id_reparacion>')
def eliminar_reparacion(id_reparacion):
    # Las facturas no se borran en cascada, así que se eliminan primero.
    ejecutar("DELETE FROM factura WHERE id_reparacion = %s", (id_reparacion,))
    ejecutar("DELETE FROM reparacion WHERE id_reparacion = %s", (id_reparacion,))
    return redirect(url_for('reparaciones'))


# --- 9. GENERAR Y MOSTRAR FACTURA DETALLADA ---
@app.route('/factura/<int:id_reparacion>')
def generar_factura(id_reparacion):
    factura_data = consultar("""
        SELECT
            r.id_reparacion, r.mano_obra AS precio_mano_obra, r.fecha_inicio, r.fecha_fin,
            c.curp, c.nombre AS cliente_nombre, c.apellidos AS cliente_apellidos,
            c.direccion, c.telefono,
            v.placas, v.modelo, v.color,
            m.nombre AS mecanico_nombre, m.apellidos AS mecanico_apellidos
        FROM reparacion r
        JOIN vehiculo v ON r.id_vehiculo = v.id_vehiculo
        JOIN cliente c ON v.id_cliente = c.id_cliente
        JOIN mecanico m ON r.id_mecanico_principal = m.id_mecanico
        WHERE r.id_reparacion = %s
    """, (id_reparacion,), uno=True)

    if not factura_data:
        flash('La reparación no existe.', 'error')
        return redirect(url_for('reparaciones'))

    detalles = consultar("""
        SELECT ref.nombre AS nombre_refaccion, d.cantidad, d.precio_unitario
        FROM refaccion_reparacion d
        JOIN refaccion ref ON d.id_refaccion = ref.id_refaccion
        WHERE d.id_reparacion = %s
    """, (id_reparacion,))

    # Cálculos de totales
    total_refacciones = sum(float(d['cantidad'] * d['precio_unitario']) for d in detalles)
    subtotal = round(float(factura_data['precio_mano_obra']) + total_refacciones, 2)
    iva = round(subtotal * 0.16, 2)
    total = round(subtotal + iva, 2)

    # Guarda (o actualiza) la factura en la tabla factura
    existente = consultar("SELECT id_factura FROM factura WHERE id_reparacion = %s",
                          (id_reparacion,), uno=True)
    if existente:
        id_factura = existente['id_factura']
        ejecutar("UPDATE factura SET subtotal = %s, iva = %s, total = %s WHERE id_factura = %s",
                 (subtotal, iva, total, id_factura))
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO factura (id_reparacion, subtotal, iva, total) VALUES (%s, %s, %s, %s)",
            (id_reparacion, subtotal, iva, total),
        )
        conn.commit()
        id_factura = cursor.lastrowid
        cursor.close()
        conn.close()

    factura_data.update({
        'id_factura': id_factura,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
    })

    return render_template('factura.html', factura=factura_data, detalles=detalles)


if __name__ == '__main__':
    app.run(debug=True)
