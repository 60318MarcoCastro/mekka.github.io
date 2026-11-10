# Sistema de Gestión de Taller

Aplicación web en Flask + MySQL para administrar clientes, vehículos, mecánicos,
refacciones, reparaciones y facturas de un taller mecánico.

## Ejecutar en tu computadora (Wampserver)

1. Enciende Wampserver (icono en verde).
2. Instala las dependencias: `pip install -r requirements.txt`
3. Crea la base y las tablas: `python init_db.py`
4. Inicia la app: `python app.py` y abre http://127.0.0.1:5000

## Publicar en PythonAnywhere (encendido 24/7)

Sustituye `USUARIO` por tu usuario de PythonAnywhere y `REPO` por el nombre de este repositorio.

### 1. Crear la cuenta y la base de datos
1. Crea una cuenta gratis en https://www.pythonanywhere.com (plan *Beginner*).
2. Ve a la pestaña **Databases**, define una contraseña de MySQL y crea una base llamada
   `gestion_taller`. Su nombre completo será `USUARIO$gestion_taller`.

### 2. Descargar el código desde GitHub
Abre **Consoles → Bash** y ejecuta:

```bash
git clone https://github.com/TU_USUARIO_GITHUB/REPO.git
cd REPO
pip install --user -r requirements.txt
```

### 3. Crear las tablas
En la misma consola (cambia la contraseña por la que pusiste en *Databases*):

```bash
DB_HOST=USUARIO.mysql.pythonanywhere-services.com \
DB_USER=USUARIO \
DB_PASSWORD='TU_CONTRASEÑA_MYSQL' \
DB_NAME='USUARIO$gestion_taller' \
python init_db.py
```

### 4. Crear la aplicación web
1. Pestaña **Web → Add a new web app → Manual configuration** → elige Python 3.12
   (o la versión más reciente que aparezca).
2. En **Code → Source code** pon `/home/USUARIO/REPO`.
3. Abre el **WSGI configuration file** (enlace en la misma pestaña), borra todo y pega:

```python
import os
import sys

path = '/home/USUARIO/REPO'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DB_HOST'] = 'USUARIO.mysql.pythonanywhere-services.com'
os.environ['DB_USER'] = 'USUARIO'
os.environ['DB_PASSWORD'] = 'TU_CONTRASEÑA_MYSQL'
os.environ['DB_NAME'] = 'USUARIO$gestion_taller'
os.environ['SECRET_KEY'] = 'escribe-aqui-una-frase-larga-y-secreta'

from app import app as application
```

4. En **Static files** agrega: URL `/static/` → Directory `/home/USUARIO/REPO/static`.
5. Presiona **Reload**. La página queda en `https://USUARIO.pythonanywhere.com`.

> La contraseña de MySQL solo vive en el archivo WSGI de PythonAnywhere; nunca la subas a GitHub.

### Actualizar después de cambiar el código
Haz `git push` desde tu PC y luego, en la consola Bash de PythonAnywhere:

```bash
cd ~/REPO && git pull
```

y presiona **Reload** en la pestaña **Web**.

### Mantenerla encendida
En el plan gratuito la app sigue encendida, pero cada 3 meses hay que entrar a la pestaña
**Web** y presionar **"Run until 3 months from today"**; si no, se apaga.
