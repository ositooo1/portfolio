-- =====================================================================
-- Portfolio - Diseño físico de la base de datos (MySQL)
-- Importar con la base YA creada (en Clever Cloud el add-on la trae).
-- Las tablas coinciden con las clases de modelos.py.
-- =====================================================================

SET NAMES utf8mb4;

-- Cuenta de acceso al modo edición (la contraseña se guarda con hash;
-- el usuario se crea con: python crear_usuario.py)
CREATE TABLE IF NOT EXISTS usuario (
  id            INT          NOT NULL AUTO_INCREMENT,
  username      VARCHAR(50)  NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_usuario_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Datos personales (hay una sola fila: el dueño del portfolio)
CREATE TABLE IF NOT EXISTS perfil (
  id          INT          NOT NULL AUTO_INCREMENT,
  nombre      VARCHAR(100) NOT NULL,
  titulo      VARCHAR(100) NULL,
  descripcion TEXT         NULL,
  email       VARCHAR(120) NULL,
  ubicacion   VARCHAR(100) NULL,
  foto        VARCHAR(255) NULL,
  banner      VARCHAR(255) NULL,
  cv          VARCHAR(255) NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Un perfil tiene muchas redes sociales, experiencias, estudios,
-- habilidades y proyectos (relaciones 1 a N por perfil_id).
CREATE TABLE IF NOT EXISTS red_social (
  id        INT          NOT NULL AUTO_INCREMENT,
  perfil_id INT          NOT NULL,
  nombre    VARCHAR(50)  NOT NULL,
  url       VARCHAR(255) NOT NULL,
  icono     VARCHAR(50)  NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_red_perfil FOREIGN KEY (perfil_id)
    REFERENCES perfil (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS experiencia (
  id           INT          NOT NULL AUTO_INCREMENT,
  perfil_id    INT          NOT NULL,
  empresa      VARCHAR(120) NOT NULL,
  puesto       VARCHAR(120) NOT NULL,
  fecha_inicio DATE         NULL,
  fecha_fin    DATE         NULL,
  descripcion  TEXT         NULL,
  orden        INT          NULL DEFAULT 0,
  PRIMARY KEY (id),
  CONSTRAINT fk_experiencia_perfil FOREIGN KEY (perfil_id)
    REFERENCES perfil (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS educacion (
  id           INT          NOT NULL AUTO_INCREMENT,
  perfil_id    INT          NOT NULL,
  instituto    VARCHAR(120) NOT NULL,
  carrera      VARCHAR(120) NOT NULL,
  fecha_inicio DATE         NULL,
  fecha_fin    DATE         NULL,
  orden        INT          NULL DEFAULT 0,
  PRIMARY KEY (id),
  CONSTRAINT fk_educacion_perfil FOREIGN KEY (perfil_id)
    REFERENCES perfil (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- tipo_id: 1 = Hard, 2 = Soft, 3 = Idioma
CREATE TABLE IF NOT EXISTS habilidad (
  id         INT         NOT NULL AUTO_INCREMENT,
  perfil_id  INT         NOT NULL,
  tipo_id    INT         NOT NULL,
  nombre     VARCHAR(60) NOT NULL,
  porcentaje INT         NOT NULL,
  orden      INT         NULL DEFAULT 0,
  PRIMARY KEY (id),
  CONSTRAINT fk_habilidad_perfil FOREIGN KEY (perfil_id)
    REFERENCES perfil (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS proyecto (
  id          INT          NOT NULL AUTO_INCREMENT,
  perfil_id   INT          NOT NULL,
  nombre      VARCHAR(120) NOT NULL,
  fecha       DATE         NULL,
  descripcion TEXT         NULL,
  link        VARCHAR(255) NULL,
  orden       INT          NULL DEFAULT 0,
  PRIMARY KEY (id),
  CONSTRAINT fk_proyecto_perfil FOREIGN KEY (perfil_id)
    REFERENCES perfil (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =====================================================================
-- Datos iniciales mínimos (sin esto la página no abre: necesita 1 perfil)
-- El resto (experiencia, estudios, skills, proyectos) se carga desde el
-- modo edición. Los nombres de foto, banner y CV son los archivos que ya
-- están en static/img y static/docs.
-- =====================================================================
INSERT INTO perfil (nombre, titulo, descripcion, foto, banner, cv)
VALUES (
  'Juan Cruz Duré',
  'Full Stack Developer Jr',
  'Editá esta descripción desde el modo edición.',
  'foto-a2f6206f386240bc.jpg',
  'banner-fcb92aa7039a7fb8.jpg',
  'cv-26d2ef5a52c1ded4.pdf'
);

INSERT INTO red_social (perfil_id, nombre, url, icono)
VALUES (1, 'GitHub', 'https://github.com/ositooo1', 'fa-brands fa-github');

-- Para que aparezca el mapa (iframe) del pie de página, cargá tu ciudad
-- desde el modo edición (Acerca de mí → lápiz → Ciudad), o con:
-- UPDATE perfil SET ubicacion = 'TU CIUDAD, PAÍS' WHERE id = 1;
