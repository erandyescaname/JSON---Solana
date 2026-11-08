##JSON TAREA##
import json
import requests
import argparse
import sys

##Para ejecutarse desde terminal: python ##JSON-Solana##.py [numero de bloque a descargar]###
##desde la ubicación del archivo##

##endpoint solana##
SOLANA = "https://api.mainnet.solana.com"

##generar solicitud##
##obtener bloque correspondiente al slot, si este está finalizado##
def descargar(slot):
    payload = {
        "jsonrpc": "2.0", ##version de JSON a usar##
        "id": 1, ##identificador de la solicitud##
        "method": "getBlock",
        ##argumentos necesarios para la consulta##
        "params": [
            slot,
            {
                "commitment": "finalized", ##que el bloque ya esté finalizado##
                "encoding": "json", ## datos en formato json##
                "transactionDetails": "full", ##transacciones completas##
                "maxSupportedTransactionVersion": 0, ##se admiten transacciones de versión 0##
                "rewards": True ##se incluyne las recompensas asociadas al bloque##
            }
        ]
    }

    try:
        print(f'Descargando bloque (slot): {slot}')

        respuesta =requests.post(
            SOLANA, ##dirección del nodo de solana##
            json=payload, ##envía el diccionario  como json de la solicitud##
            headers={"Content-Type":"application/json"}, ##esécofica que el contenido es JSON##
            timeout=60 ##limite ed tiempo de la solicitud##
        )

        ##procesamiento de la respuesta HTTP##
        respuesta.raise_for_status()
        datos = respuesta.json()

        ##comprobar errores##
        if "error" in datos:
            print('Error RPC:', datos["error"])
            return

        ##obtener infor del bloque##
        bloque = datos.get("result")

        ##si la clave no existe o es None##
        if bloque is None:
            print('El bloque no existe')
            return

        ##Guardar bloque en el archivo JSON##
        nombre = f'bloque_{slot}.json'

        ##escribe los satos del bloque en el disco##
        with open(nombre, 'w', encoding='utf-8)') as archivo:
            json.dump(bloque, archivo, indent=4, ensure_ascii=False)

        print(f'Bloque descargado correctamente')
        print(f'Archivo generado: {nombre}')
        print(f'Hash del bloque: {bloque["blockhash"]}')
        print(f'Transacciones: {len(bloque.get("transactions", []))}')

    ##manejo de excepciones##
    except requests.exceptions.RequestException as error:
        print(f'Error de conexión: {error}')

    except (ValueError, KeyError) as error:
        print(f'Error al procesar la respuesta {error}')

        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Descargar un bloque de la Mainnet de Solana"
    )

    parser.add_argument(
        "bloque",
        type=int,
        help="Número de slot del bloque que se desea descargar"
    )

    ##Obtener argumentos de la terminal ##
    argumentos = parser.parse_args()

    if argumentos.bloque < 0:
        parser.error("El n+umero del bloque no puede ser negativo")

    descargar(argumentos.bloque)

###El archivo json se descarga en la carpeta donde se ejecuta el código###

##Me apoyé bastante en chatgpt y se nota##