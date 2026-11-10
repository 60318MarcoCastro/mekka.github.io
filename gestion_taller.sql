-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 10-11-2026 a las 02:27:00
-- Versión del servidor: 5.5.24-log
-- Versión de PHP: 5.4.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `taller`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE IF NOT EXISTS `cliente` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `curp` varchar(18) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidos` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `curp` (`curp`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `curp`, `nombre`, `apellidos`, `direccion`, `telefono`) VALUES
(1, 'CAPAHGTNRN02', 'ANGEL URIEL JOSAFAT', 'CANO PORRAS ', 'RADIO #103', '4776621913');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura`
--

CREATE TABLE IF NOT EXISTS `factura` (
  `id_factura` int(11) NOT NULL AUTO_INCREMENT,
  `id_reparacion` int(11) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `iva` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_factura`),
  KEY `fk_factura_reparacion` (`id_reparacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mecanico`
--

CREATE TABLE IF NOT EXISTS `mecanico` (
  `id_mecanico` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidos` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_mecanico`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `mecanico`
--

INSERT INTO `mecanico` (`id_mecanico`, `nombre`, `apellidos`, `telefono`) VALUES
(1, 'juan', 'perez', '467979889');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mecanico_reparacion`
--

CREATE TABLE IF NOT EXISTS `mecanico_reparacion` (
  `id_reparacion` int(11) NOT NULL,
  `id_mecanico` int(11) NOT NULL,
  PRIMARY KEY (`id_reparacion`,`id_mecanico`),
  KEY `fk_mr_mecanico` (`id_mecanico`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `refaccion`
--

CREATE TABLE IF NOT EXISTS `refaccion` (
  `id_refaccion` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_refaccion`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=7 ;

--
-- Volcado de datos para la tabla `refaccion`
--

INSERT INTO `refaccion` (`id_refaccion`, `nombre`, `precio_unitario`) VALUES
(1, 'espejo lateral', '451.00'),
(2, 'aleron', '9599.00'),
(3, 'salpicadera', '899.00'),
(4, 'puerta copiloto', '4899.00'),
(5, 'amortiguador delantero', '3566.00'),
(6, 'calavera trasera', '899.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `refaccion_reparacion`
--

CREATE TABLE IF NOT EXISTS `refaccion_reparacion` (
  `id_reparacion` int(11) NOT NULL,
  `id_refaccion` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_reparacion`,`id_refaccion`),
  KEY `fk_rr_refaccion` (`id_refaccion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `refaccion_reparacion`
--

INSERT INTO `refaccion_reparacion` (`id_reparacion`, `id_refaccion`, `cantidad`, `precio_unitario`) VALUES
(1, 2, 1, '0.00'),
(2, 2, 1, '9599.00'),
(2, 5, 1, '3566.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparacion`
--

CREATE TABLE IF NOT EXISTS `reparacion` (
  `id_reparacion` int(11) NOT NULL AUTO_INCREMENT,
  `id_vehiculo` int(11) NOT NULL,
  `id_mecanico_principal` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date DEFAULT NULL,
  `mano_obra` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_reparacion`),
  KEY `fk_reparacion_vehiculo` (`id_vehiculo`),
  KEY `fk_reparacion_mecanico` (`id_mecanico_principal`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `reparacion`
--

INSERT INTO `reparacion` (`id_reparacion`, `id_vehiculo`, `id_mecanico_principal`, `fecha_inicio`, `fecha_fin`, `mano_obra`) VALUES
(1, 2, 1, '2026-08-09', '2026-08-14', '1250.00'),
(2, 1, 1, '2026-08-09', '2026-08-14', '1250.00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=2 ;

--
-- Volcado de datos para la tabla `usuarios`
--

-- La contraseña NO se guarda aquí (este archivo es público en GitHub).
-- init_db.py la pide al cargar la base y la asigna al usuario admin.
INSERT INTO `usuarios` (`id`, `usuario`, `password`) VALUES
(1, 'admin', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculo`
--

CREATE TABLE IF NOT EXISTS `vehiculo` (
  `id_vehiculo` int(11) NOT NULL AUTO_INCREMENT,
  `placas` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `modelo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha_entrada` date NOT NULL,
  `hora_entrada` time NOT NULL,
  `id_cliente` int(11) NOT NULL,
  PRIMARY KEY (`id_vehiculo`),
  UNIQUE KEY `placas` (`placas`),
  KEY `fk_vehiculo_cliente` (`id_cliente`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `vehiculo`
--

INSERT INTO `vehiculo` (`id_vehiculo`, `placas`, `modelo`, `color`, `fecha_entrada`, `hora_entrada`, `id_cliente`) VALUES
(1, 'GTSH971Q', 'MATIZ', 'AMARILLO', '2026-08-01', '19:39:00', 1),
(2, 'gth245f', 'matiz', 'amarillo', '2026-08-07', '20:15:00', 1);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `factura`
--
ALTER TABLE `factura`
  ADD CONSTRAINT `fk_factura_reparacion` FOREIGN KEY (`id_reparacion`) REFERENCES `reparacion` (`id_reparacion`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `mecanico_reparacion`
--
ALTER TABLE `mecanico_reparacion`
  ADD CONSTRAINT `fk_mr_mecanico` FOREIGN KEY (`id_mecanico`) REFERENCES `mecanico` (`id_mecanico`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_mr_reparacion` FOREIGN KEY (`id_reparacion`) REFERENCES `reparacion` (`id_reparacion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `refaccion_reparacion`
--
ALTER TABLE `refaccion_reparacion`
  ADD CONSTRAINT `fk_rr_refaccion` FOREIGN KEY (`id_refaccion`) REFERENCES `refaccion` (`id_refaccion`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_rr_reparacion` FOREIGN KEY (`id_reparacion`) REFERENCES `reparacion` (`id_reparacion`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `reparacion`
--
ALTER TABLE `reparacion`
  ADD CONSTRAINT `fk_reparacion_mecanico` FOREIGN KEY (`id_mecanico_principal`) REFERENCES `mecanico` (`id_mecanico`) ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_reparacion_vehiculo` FOREIGN KEY (`id_vehiculo`) REFERENCES `vehiculo` (`id_vehiculo`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `vehiculo`
--
ALTER TABLE `vehiculo`
  ADD CONSTRAINT `fk_vehiculo_cliente` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
