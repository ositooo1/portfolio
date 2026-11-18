from sqlalchemy import create_engine

from config import URI

with open("base_de_datos.sql", encoding="utf-8") as archivo:
    lineas = [l for l in archivo if not l.strip().startswith("--")]

sentencias = [s.strip() for s in "".join(lineas).split(";") if s.strip()]

engine = create_engine(URI)
with engine.begin() as conexion:
    for sentencia in sentencias:
        conexion.exec_driver_sql(sentencia)

print(f"Listo: se ejecutaron {len(sentencias)} sentencias.")