# Sistema de Gestión de Taller "Porras"

Aplicación web en Flask + MySQL para administrar clientes, vehículos, mecánicos,
refacciones, reparaciones y facturas de un taller mecánico. Requiere iniciar sesión
(usuarios de la tabla `usuarios`).

Página publicada: **https://marcocastro32.pythonanywhere.com**

## Ejecutar en tu computadora (Wampserver)

1. Enciende Wampserver (icono en verde).
2. Instala las dependencias: `pip install -r requirements.txt`
3. Crea la base y carga los datos (solo la primera vez): `python init_db.py`
4. Inicia la app: `python app.py` y abre http://127.0.0.1:5000

## Publicar en PythonAnywhere (usuario `MarcoCastro32`)

### 1. Base de datos
En la pestaña **Databases**: define una contraseña de MySQL y crea una base llamada
`gestion_taller`. Su nombre completo será `MarcoCastro32$gestion_taller`.

### 2. Código y datos
Abre **Consoles → Bash** y ejecuta (cambia `TU_CONTRASEÑA` por la de MySQL):

```bash
git clone https://github.com/60318MarcoCastro/mekka.github.io.git
cd mekka.github.io
pip install --user -r requirements.txt
export DB_HOST=MarcoCastro32.mysql.pythonanywhere-services.com
export DB_USER=MarcoCastro32
export DB_PASSWORD='TU_CONTRASEÑA'
export DB_NAME='MarcoCastro32$gestion_taller'
python init_db.py
```

`init_db.py` carga `gestion_taller.sql` (tablas y datos) y te pide la **contraseña del
usuario `admin`** (no se muestra al escribirla). Ejecútalo **una sola vez**.

### 3. Aplicación web
1. Pestaña **Web → Add a new web app → Manual configuration → Python 3.12**.
2. **Source code:** `/home/MarcoCastro32/mekka.github.io`
3. Abre el **WSGI configuration file**, borra todo y pega:

```python
import os
import sys

path = '/home/MarcoCastro32/mekka.github.io'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DB_HOST'] = 'MarcoCastro32.mysql.pythonanywhere-services.com'
os.environ['DB_USER'] = 'MarcoCastro32'
os.environ['DB_PASSWORD'] = 'TU_CONTRASEÑA'
os.environ['DB_NAME'] = 'MarcoCastro32$gestion_taller'
os.environ['SECRET_KEY'] = 'escribe-aqui-una-frase-larga-y-secreta'

from app import app as application
```

4. **Static files:** URL `/static/` → Directory `/home/MarcoCastro32/mekka.github.io/static`
5. Presiona **Reload** y abre https://marcocastro32.pythonanywhere.com

> La contraseña de MySQL solo vive en el archivo WSGI de PythonAnywhere; nunca la subas a GitHub.

### 4. Cambiar la contraseña del administrador (opcional)
La contraseña de `admin` no está en GitHub; solo existe en tu base. Para cambiarla después,
desde la consola Bash (con las variables del paso 2 cargadas):

```bash
mysql -h $DB_HOST -u $DB_USER -p"$DB_PASSWORD" "$DB_NAME" \
  -e "UPDATE usuarios SET password='NUEVA_CONTRASEÑA' WHERE usuario='admin';"
```

### Actualizar después de cambiar el código
Haz `git push` desde tu PC y luego, en la consola Bash de PythonAnywhere:

```bash
cd ~/mekka.github.io && git pull
```

y presiona **Reload** en la pestaña **Web**.

### Mantenerla encendida
En el plan gratuito, cada 3 meses entra a la pestaña **Web** y presiona
**"Run until 3 months from today"**; si no, la página se apaga.
