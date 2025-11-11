import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from productos.models import Producto

def run(*args):
    if not args:
        print("Error: Favor de propocionar la ruta al archivo CSV.")
        print("Uso: python manage.py runscript importar_clientes --script-args <ruta_al_archivo_csv>")
        sys.exit(1)

    csv_file = args[0]
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            producto_a_crear = []

            # Campos obligatorios (direccion es opcional)
            campos_obligatorios = ['nombre', 'descripcion', 'precio_unitario', 'sku', 'stock']

            for row in reader:
                # Verificar que no falte ningún campo obligatorio
                if any(row.get(campo) in (None, '') for campo in campos_obligatorios):
                    print(f'Error en fila {row}. Falta un campo obligatorio')
                    continue

                try:
                    producto = Producto(
                        nombre=row.get('nombre'),
                        descripcion=row.get('descripcion'),
                        sku=row.get('sku'),
                        stock=row.get('stock'),
                        precio_unitario=row.get('precio_unitario'),
                    )
                    producto.full_clean()
                    producto_a_crear.append(producto)
                except ValidationError as e:
                    print(f'Error de validacion en fila {row}. Detalle: {e}')
                except Exception as e:
                    print(f'Error inesperado en fila {row}. Detalle: {e}')

            if producto_a_crear:
                with transaction.atomic():
                    Producto.objects.bulk_create(producto_a_crear)
                print(f"Importacion de {len(producto_a_crear)} clientes completada exitosamente.")
            else:
                print("No hay clientes válidos para importar.")
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {csv_file}")
    except Exception as e:
        print(f"Error inesperado: {e}")