CREATE DATABASE IF NOT EXISTS empresa_db;
USE empresa_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    estado VARCHAR(20) DEFAULT 'ACTIVO'
);

CREATE TABLE IF NOT EXISTS productos (
    codigo VARCHAR(20) PRIMARY KEY,
    descripcion VARCHAR(150) NOT NULL,
    unidad_medida VARCHAR(50) NOT NULL,
    presentacion VARCHAR(50) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL,
    fecha_registro DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS inventario (
    id_inventario INT AUTO_INCREMENT PRIMARY KEY,
    codigo_producto VARCHAR(20) NOT NULL,
    cantidad INT NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (codigo_producto) REFERENCES productos(codigo) ON DELETE CASCADE
);

INSERT INTO usuarios (usuario, password, estado) 
VALUES 
('admin', 'admin123', 'ACTIVO'),
('bodega', 'clave123', 'ACTIVO');

INSERT INTO productos (codigo, descripcion, unidad_medida, presentacion, precio, stock, estado, fecha_registro) 
VALUES 
('FER-001', 'Cemento Tolteca 42.5kg', 'Sacos', 'Saco', 85.00, 150, 'Activo', '2026-03-01'),
('FER-002', 'Clavo para Concreto 2.5 pulg', 'Libras', 'Bolsa', 12.50, 80, 'Activo', '2026-03-01'),
('FER-003', 'Varilla de Hierro 3/8 Grado 40', 'Quintales', 'Atado', 380.00, 25, 'Activo', '2026-03-02'),
('FER-004', 'Pintura Látex Blanca 1 Galón', 'Galones', 'Cubeta', 145.00, 40, 'Activo', '2026-03-02');

INSERT INTO inventario (codigo_producto, cantidad, fecha) 
VALUES 
('FER-001', 150, '2026-03-01'),
('FER-002', 80, '2026-03-01'),
('FER-003', 25, '2026-03-02'),
('FER-004', 40, '2026-03-02');