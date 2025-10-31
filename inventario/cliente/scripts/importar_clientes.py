import csv
import sys
from django.db import transaction
from django.core.exceptions import ValidationError
from cliente.models import Cliente

def run(*args):
    if not args:
        print("Error: Favor de propocionar la ruta al archivo CSV.")
        print("Uso: ./manage.py runscript import_oficinas --script-args <ruta_al_archivo_csv>")
        sys.exit(1)

    csv_file = args[0]
    try:
        with open(csv_file, 'r', enconding = 'utf-8') as f:
            reader = csv.DictReader(f)
            clientes_a_crear = []
            for row in reader:
                cliente = row.get('cliente')

                if not cliente:
                    print(f'Error en fila {row}. Falta un campo')
                    continue
                
                try:
                    cliente.full_clean()
                    clientes_a_crear.append(cliente)
                except ValidationError as e:
                    print(f'Error de validacion en fila {row}. Detalle: {e}')
                except Exception as e:
                    print(f'Error inesperado en fila {row}. Detalle: {e}')
            with transaction.atomic():
                Cliente.objects.bulk_create(clientes_a_crear)
                print(f"Importacion de {len(clientes_a_crear)} clientes completada exitosamente.")
    except FileNotFoundError:
        print(f"Error: No se encontro el archivo {csv_file}")
    except Exception as e:
        print(f"Error inesperado: {e}")