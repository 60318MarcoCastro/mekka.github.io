from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'clave_secreta_taller'

# Configuración de conexión a la Base de Datos (Wampserver)
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='', # Si tienes contraseña en Wampserver, colócala aquí
        database='gestion_taller',
        port=3306
    )
    return connection

# --- 1. RUTA PRINCIPAL ---
@app.route('/')
def index():
    return render_template('index.html')


# --- 2. MÓDULO DE CLIENTES ---
@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        campos = ['curp', 'nombre', 'apellidos', 'direccion', 'telefono']
        valores = tuple(request.form[c] for c in campos)

        cursor.execute(
            "INSERT INTO clientes (curp, nombre, apellidos, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
            valores
        )
        conn.commit()
        return redirect(url_for('clientes'))

    cursor.execute("SELECT * FROM clientes")
    lista_clientes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=lista_clientes)


@app.route('/eliminar_cliente/<string:curp>')
def eliminar_cliente(curp):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE curp = %s", (curp,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('clientes'))


# --- 3. MÓDULO DE VEHÍCULOS ---
@app.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        campos = ['placas', 'modelo', 'color', 'curp_cliente']
        valores = tuple(request.form[c] for c in campos)

        cursor.execute(
            "INSERT INTO vehiculos (placas, modelo, color, curp_cliente) VALUES (%s, %s, %s, %s)",
            valores
        )
        conn.commit()
        return redirect(url_for('vehiculos'))

    cursor.execute("""
        SELECT v.*, c.nombre, c.apellidos
        FROM vehiculos v
        JOIN clientes c ON v.curp_cliente = c.curp
    """)
    lista_vehiculos = cursor.fetchall()

    cursor.execute("SELECT curp, nombre, apellidos FROM clientes")
    lista_clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('vehiculos.html', vehiculos=lista_vehiculos, clientes=lista_clientes)


@app.route('/eliminar_vehiculo/<string:placas>')
def eliminar_vehiculo(placas):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehiculos WHERE placas = %s", (placas,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('vehiculos'))



# --- 4. MÓDULO DE MECÁNICOS ---
@app.route('/mecanicos', methods=['GET', 'POST'])
def mecanicos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        campos = ['nombre', 'apellidos', 'telefono']
        valores = tuple(request.form[c] for c in campos)

        cursor.execute(
            "INSERT INTO mecanicos (nombre, apellidos, telefono) VALUES (%s, %s, %s)",
            valores
        )
        conn.commit()
        return redirect(url_for('mecanicos'))

    cursor.execute("SELECT * FROM mecanicos")
    lista_mecanicos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('mecanicos.html', mecanicos=lista_mecanicos)


@app.route('/eliminar_mecanico/<int:id_mecanico>')
def eliminar_mecanico(id_mecanico):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mecanicos WHERE id_mecanico = %s", (id_mecanico,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('mecanicos'))


# --- 5. MÓDULO DE REFACCIONES ---
@app.route('/refacciones', methods=['GET', 'POST'])
def refacciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        campos = ['nombre', 'descripcion', 'precio_unitario']
        valores = tuple(request.form[c] for c in campos)

        cursor.execute(
            "INSERT INTO refacciones (nombre, descripcion, precio_unitario) VALUES (%s, %s, %s)",
            valores
        )
        conn.commit()
        return redirect(url_for('refacciones'))

    cursor.execute("SELECT * FROM refacciones")
    lista_refacciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('refacciones.html', refacciones=lista_refacciones)


@app.route('/eliminar_refaccion/<int:id_refaccion>')
def eliminar_refaccion(id_refaccion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM refacciones WHERE id_refaccion = %s", (id_refaccion,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('refacciones'))


# --- 6. MÓDULO DE REPARACIONES ---
@app.route('/reparaciones', methods=['GET', 'POST'])
def reparaciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        campos = ['placas_vehiculo', 'id_mecanico_asignado', 'precio_mano_obra']
        placas, id_mecanico, precio_mano_obra = (request.form[c] for c in campos)

        cursor.execute(
            """
            INSERT INTO reparaciones 
            (placas_vehiculo, id_mecanico_asignado, fecha_entrada, hora_entrada, precio_mano_obra)
            VALUES (%s, %s, CURDATE(), CURTIME(), %s)
            """,
            (placas, id_mecanico, precio_mano_obra)
        )
        conn.commit()
        return redirect(url_for('reparaciones'))

    cursor.execute("""
        SELECT 
            r.*, 
            m.nombre AS nombre_mecanico, 
            m.apellidos AS apellidos_mecanico,
            IFNULL(
                GROUP_CONCAT(DISTINCT CONCAT(m_ayuda.nombre, ' ', m_ayuda.apellidos) SEPARATOR ', '),
                'Sin ayudantes'
            ) AS ayudantes
        FROM reparaciones r 
        JOIN mecanicos m ON r.id_mecanico_asignado = m.id_mecanico
        LEFT JOIN equipo_reparacion eq ON r.id_reparacion = eq.id_reparacion
        LEFT JOIN mecanicos m_ayuda ON eq.id_mecanico = m_ayuda.id_mecanico
        GROUP BY r.id_reparacion
    """)
    lista_reparaciones = cursor.fetchall()

    cursor.execute("SELECT placas, modelo FROM vehiculos")
    lista_vehiculos = cursor.fetchall()

    cursor.execute("SELECT id_mecanico, nombre, apellidos FROM mecanicos")
    lista_mecanicos = cursor.fetchall()

    cursor.execute("SELECT * FROM refacciones")
    lista_refacciones = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'reparaciones.html',
        reparaciones=lista_reparaciones,
        vehiculos=lista_vehiculos,
        mecanicos=lista_mecanicos,
        refacciones=lista_refacciones
    )


# --- 7. ASIGNAR MECÁNICO DE APOYO (EQUIPO) ---
@app.route('/agregar_mecanico_equipo', methods=['POST'])
def agregar_mecanico_equipo():
    id_reparacion = request.form['id_reparacion']
    id_mecanico = request.form['id_mecanico_ayudante']

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT IGNORE INTO equipo_reparacion (id_reparacion, id_mecanico) VALUES (%s, %s)"
    cursor.execute(sql, (id_reparacion, id_mecanico))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('reparaciones'))


# --- 8. ASIGNAR REFACCIÓN A REPARACIÓN ---
@app.route('/agregar_refaccion_reparacion', methods=['POST'])
def agregar_refaccion_reparacion():
    id_reparacion = request.form['id_reparacion']
    id_refaccion = request.form['id_refaccion']
    cantidad = int(request.form['cantidad'])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT precio_unitario FROM refacciones WHERE id_refaccion = %s", (id_refaccion,))
    refaccion = cursor.fetchone()

    if refaccion:
        precio_unitario = refaccion['precio_unitario']

        sql = """
            INSERT INTO detalle_refacciones_reparacion (id_reparacion, id_refaccion, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE cantidad = cantidad + VALUES(cantidad)
        """
        cursor.execute(sql, (id_reparacion, id_refaccion, cantidad, precio_unitario))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('reparaciones'))


@app.route('/eliminar_reparacion/<int:id_reparacion>')
def eliminar_reparacion(id_reparacion):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reparaciones WHERE id_reparacion = %s", (id_reparacion,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('reparaciones'))


# --- 9. GENERAR Y MOSTRAR FACTURA DETALLADA ---
@app.route('/factura/<int:id_reparacion>')
def generar_factura(id_reparacion):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Datos principales de la reparación, cliente, vehículo y mecánico
    cursor.execute("""
        SELECT 
            r.id_reparacion, r.precio_mano_obra,
            c.curp, c.nombre AS cliente_nombre, c.apellidos AS cliente_apellidos, 
            c.direccion, c.telefono,
            v.placas, v.modelo, v.color,
            m.nombre AS mecanico_nombre, m.apellidos AS mecanico_apellidos
        FROM reparaciones r
        JOIN vehiculos v ON r.placas_vehiculo = v.placas
        JOIN clientes c ON v.curp_cliente = c.curp
        JOIN mecanicos m ON r.id_mecanico_asignado = m.id_mecanico
        WHERE r.id_reparacion = %s
    """, (id_reparacion,))
    factura_data = cursor.fetchone()

    # Refacciones utilizadas
    cursor.execute("""
        SELECT 
            ref.nombre AS nombre_refaccion, 
            d.cantidad, 
            d.precio_unitario
        FROM detalle_refacciones_reparacion d
        JOIN refacciones ref ON d.id_refaccion = ref.id_refaccion
        WHERE d.id_reparacion = %s
    """, (id_reparacion,))
    detalles = cursor.fetchall()

    # Cálculos de totales
    total_refacciones = sum(d['cantidad'] * d['precio_unitario'] for d in detalles)
    subtotal = float(factura_data['precio_mano_obra']) + float(total_refacciones)
    iva = subtotal * 0.16
    total = subtotal + iva

    factura_data.update({
        'subtotal': subtotal,
        'iva': iva,
        'total': total
    })

    cursor.close()
    conn.close()

    return render_template('factura.html', factura=factura_data, detalles=detalles)


if __name__ == '__main__':
    app.run(debug=True)