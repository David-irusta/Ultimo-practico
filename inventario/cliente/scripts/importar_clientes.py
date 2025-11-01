import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from cliente.models import Cliente

def run(*args):
    if not args:
        print("Error: Favor de propocionar la ruta al archivo CSV.")
        print("Uso: python manage.py runscript importar_clientes --script-args <ruta_al_archivo_csv>")
        sys.exit(1)

    csv_file = args[0]
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            clientes_a_crear = []

            # Campos obligatorios (direccion es opcional)
            campos_obligatorios = ['nombre', 'apellido', 'numero_documento', 'email', 'direccion', 'telefono']

            for row in reader:
                # Verificar que no falte ningún campo obligatorio
                if any(row.get(campo) in (None, '') for campo in campos_obligatorios):
                    print(f'Error en fila {row}. Falta un campo obligatorio')
                    continue

                try:
                    cliente = Cliente(
                        nombre=row.get('nombre'),
                        apellido=row.get('apellido'),
                        numero_documento=row.get('numero_documento'),
                        email=row.get('email'),
                        direccion=row.get('direccion'),
                        telefono=row.get('telefono')
                    )
                    cliente.full_clean()
                    clientes_a_crear.append(cliente)
                except ValidationError as e:
                    print(f'Error de validacion en fila {row}. Detalle: {e}')
                except Exception as e:
                    print(f'Error inesperado en fila {row}. Detalle: {e}')

            if clientes_a_crear:
                with transaction.atomic():
                    Cliente.objects.bulk_create(clientes_a_crear)
                print(f"Importacion de {len(clientes_a_crear)} clientes completada exitosamente.")
            else:
                print("No hay clientes válidos para importar.")
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {csv_file}")
    except Exception as e:
        print(f"Error inesperado: {e}")