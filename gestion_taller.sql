-- Tablas para el sistema de gestión de taller (app.py)
-- Ejecuta "python init_db.py" o impórtalo en phpMyAdmin con la base ya seleccionada.

CREATE TABLE IF NOT EXISTS clientes (
    curp       VARCHAR(18)  NOT NULL PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    apellidos  VARCHAR(100) NOT NULL,
    direccion  VARCHAR(255),
    telefono   VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS vehiculos (
    placas        VARCHAR(15)  NOT NULL PRIMARY KEY,
    modelo        VARCHAR(100) NOT NULL,
    color         VARCHAR(50),
    curp_cliente  VARCHAR(18)  NOT NULL,
    FOREIGN KEY (curp_cliente) REFERENCES clientes(curp)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS mecanicos (
    id_mecanico  INT AUTO_INCREMENT PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL,
    apellidos    VARCHAR(100) NOT NULL,
    telefono     VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS refacciones (
    id_refaccion     INT AUTO_INCREMENT PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    descripcion      VARCHAR(255),
    precio_unitario  DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reparaciones (
    id_reparacion         INT AUTO_INCREMENT PRIMARY KEY,
    placas_vehiculo       VARCHAR(15) NOT NULL,
    id_mecanico_asignado  INT NOT NULL,
    fecha_entrada         DATE NOT NULL,
    hora_entrada          TIME NOT NULL,
    precio_mano_obra      DECIMAL(10,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (placas_vehiculo) REFERENCES vehiculos(placas)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_mecanico_asignado) REFERENCES mecanicos(id_mecanico)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Mecánicos de apoyo en una reparación (la PK evita duplicados: INSERT IGNORE)
CREATE TABLE IF NOT EXISTS equipo_reparacion (
    id_reparacion  INT NOT NULL,
    id_mecanico    INT NOT NULL,
    PRIMARY KEY (id_reparacion, id_mecanico),
    FOREIGN KEY (id_reparacion) REFERENCES reparaciones(id_reparacion)
        ON DELETE CASCADE,
    FOREIGN KEY (id_mecanico) REFERENCES mecanicos(id_mecanico)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Refacciones usadas por reparación (la PK permite ON DUPLICATE KEY UPDATE)
CREATE TABLE IF NOT EXISTS detalle_refacciones_reparacion (
    id_reparacion    INT NOT NULL,
    id_refaccion     INT NOT NULL,
    cantidad         INT NOT NULL DEFAULT 1,
    precio_unitario  DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_reparacion, id_refaccion),
    FOREIGN KEY (id_reparacion) REFERENCES reparaciones(id_reparacion)
        ON DELETE CASCADE,
    FOREIGN KEY (id_refaccion) REFERENCES refacciones(id_refaccion)
        ON DELETE CASCADE
) ENGINE=InnoDB;
