# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:01:36 2020

@author: Virgilio
"""

def code_request():

    #sandbox-ProductInformation Credentials
    DK_CLIENT_ID = 'dmVGfs4nVKfqdZ9xXJSkA7DNteZEmBIm'
    DK_CLIENT_SECRET = 'tyWh2Z9lHcN8JkKk'
    DK_CALLBACK_URL = 'https://localhost'
    
    # An example url encoded code request with the required query parameters:
    # https://sandbox-api.digikey.com/v1/oauth2/authorize?response_type=code&client_id=123456789abcdefg&redirect_uri=https://client-app-redirect-uri/
    
    #Code request base URL
    cr_base_url = 'https://sandbox-api.digikey.com/v1/oauth2/authorize'
    
    #Diccionario con lo necesario para pedir el codigo necesario para obtener un Token
    params = {'response_type' : 'code',
              'client_id' : DK_CLIENT_ID,
              'redirect_uri' : DK_CALLBACK_URL}
    
    # Hacemos la petición de código para luego pedir un Token
    from urllib.parse import urlencode
    url = cr_base_url + '?' + urlencode(params)
    
    #Abre un navegador para identificarnos y recibir el código de vuelta
    from webbrowser import open_new
    open_new(url)
    
    return
    
    
    
def token_request(code):

    # Sandbox Access Token Endpoint
    ACCESS_TOKEN_ENDPOINT = 'https://sandbox-api.digikey.com/v1/oauth2/token'
    
    #sandbox-ProductInformation Credentials
    DK_CLIENT_ID = 'dmVGfs4nVKfqdZ9xXJSkA7DNteZEmBIm'
    DK_CLIENT_SECRET = 'tyWh2Z9lHcN8JkKk'
    DK_CALLBACK_URL = 'https://localhost'
    
    # Cabecera y parametros necesarios para HTTP POST request
    headers = {'Host': 'sandbox-api.digikey.com',
               'Content-type': 'application/x-www-form-urlencoded'
               }
    data = {'code' : code,
            'client_id' : DK_CLIENT_ID,
            'client_secret' : DK_CLIENT_SECRET,
            'redirect_uri' : DK_CALLBACK_URL,
            'grant_type' : 'authorization_code'
            }
    
    # HTTP POST request
    import requests
    r = requests.post(ACCESS_TOKEN_ENDPOINT, headers=headers, data=data)
    
    # Para imprimir diccionarios cuidando la visualización
    import pprint
    
    #Imprime posibles errores
    try: 
        r.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        print ('ERROR CAPTURADO!!!!\n')
        pprint.pprint (e)
    
    #Convierte el fichero JSON a un diccionario de Python
    token_json = r.json()
    
#    #Imprime el diccionario cuidando la visualización
#    print ('\nTOKEN:\n')
#    pprint.pprint (token_json)
    
    return token_json


def brand_new_token(refresh_token):

    # Sandbox Access Token Endpoint
    ACCESS_TOKEN_ENDPOINT = 'https://sandbox-api.digikey.com/v1/oauth2/token'
        
    #sandbox-ProductInformation Credentials
    DK_CLIENT_ID = 'dmVGfs4nVKfqdZ9xXJSkA7DNteZEmBIm'
    DK_CLIENT_SECRET = 'tyWh2Z9lHcN8JkKk'
    DK_CALLBACK_URL = 'https://localhost'
    
    # Cabecera y parametros necesarios para HTTP POST request
    headers = {'Host': 'sandbox-api.digikey.com',
               'Content-type': 'application/x-www-form-urlencoded'
               }
    data = {'client_id' : DK_CLIENT_ID,
            'client_secret' : DK_CLIENT_SECRET,
            'refresh_token' : refresh_token,
            'grant_type' : 'refresh_token'
            }
    
    # HTTP POST request
    import requests
    r = requests.post(ACCESS_TOKEN_ENDPOINT, headers=headers, data=data)
    
    # Para imprimir diccionarios cuidando la visualización
    import pprint
    
    #Imprime posibles errores
    try: 
        r.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        print ('ERROR CAPTURADO!!!!\n')
        pprint.pprint (e)
    
    #Convierte el fichero JSON a un diccionario de Python
    token_json = r.json()
    
#    #Imprime el diccionario cuidando la visualización
#    print ('\nTOKEN:\n')
#    pprint.pprint (token_json)
    
    return token_json

def product_search(access_token, part_number):

    # Access endpoint de las peticiones ProductSearch
    ACCESS_REQUEST_ENDPOINT = 'https://sandbox-api.digikey.com/Search/v3/Products/'

    # Construimos la URL de la petición HTTP GET    
    url = ACCESS_REQUEST_ENDPOINT + part_number
    
    # Construimos los headers de la petición
    bearer_token = "Bearer " + access_token # Standard https://tools.ietf.org/html/rfc6750#section-2.1
    DK_CLIENT_ID = 'dmVGfs4nVKfqdZ9xXJSkA7DNteZEmBIm'   # Client ID de la API
    
    headers = {'Authorization': bearer_token,
               'X-DIGIKEY-Client-Id': DK_CLIENT_ID
               }    
    
    # Petición HTTP GET   
    import requests
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
        
    #Imprime posibles errores
    try: 
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        import pprint # Para imprimir diccionarios cuidando la visualización
        print ('ERROR CAPTURADO!!!!\n')
        pprint.pprint (e)
        return False
    
    #Convierte el fichero JSON a un diccionario de Python
    component = r.json()
    
    # Imprime el diccionario cuidando la visualización
    #import pprint
    #print ('\nCOMPONENT INFORMATION:\n')
    #pprint.pprint(component)

    return component

def germany_and_USD(component_url):

    import re
    # Cambiamos a Germany (de)
    com2de = re.sub('com{1}', 'de', component_url)
    en2de = re.sub('/../{1}', '/de/', com2de)
    
    # Cambiamos 'currency' & 'language'
    modified_comp_url = en2de + '?cur=USD&lang=en'
    
    return modified_comp_url

def get_pricing_data(component):
    
    # Extraemos los datos relevantes
    try:
        #Manufacturer
        manufacturer = component['Manufacturer']['Value']
        
        #Part number
        manufacturer_part_number = component['ManufacturerPartNumber']
        
        # Tomamos el valor más alto de Price Break y su Precio correspondiente
        standard_pricing = component['StandardPricing'][len(component['StandardPricing'])-1]['UnitPrice']
        break_quantity = component['StandardPricing'][len(component['StandardPricing'])-1]['BreakQuantity']
        
        # Modificamos en la URL los campos país, moneda, idioma
        component_url = component['ProductUrl']
        modified_comp_url = germany_and_USD(component_url)
        
        # Añadimos la fecha de hoy
        from datetime import date
        current_date = str(date.today())

    except:
        return False
    
    return {'manufacturer':manufacturer,
            'manufacturer_part_number':manufacturer_part_number,
            'break_quantity':break_quantity,
            'standard_pricing':standard_pricing,
            'component_url':modified_comp_url,
            'date':current_date               
            }
        

    
#Pseudocódigo: Creación de una lista de Part Numbers
#
#1 - Abrir archivo excel.
#2 - Recorrer línea a línea la columna 'link'
#3 - Mediante regular expresions, comprobar que en el link pone 'digikey'
#4 - Mediante regular expresions, aislar el 'Digikey Part Number':
#    ¡¡¡Siempre termina en '-ND*!!!
#5 - Si en el link pone "digikey" y se encuentra algo terminado en '-ND':
#    guardar el 'Digikey Part Number' en la lista (Si no, guardar False)

def parse_dk_part_number(excel_file_path):
    # Abrimos el fichero
    import pandas as pd
    df = pd.read_excel(excel_file_path)
    
    # Tomamos la primera columna: 'links'
    import numpy as np
    link_array = df['link'].to_numpy()
    
    # Comprobamos para cada fila si:
    #   - Es un link de 'digikey'?
    #   - Es un componente?
    # Para ello, utilizamos dos criterios:
    # 1. Los link a componentes siempre contienen el 'digikey part number'
    # 2. Los 'digikey part number' siempre terminan en '-ND'
    import re
    assess= list()
    for link in link_array:
        if re.search('digikey', str(link)) and re.search('-ND', str(link)):
            assess.append(True)
        else:
            assess.append(False)
    
    # Metemos en la lista 'assess' el 'Digikey Part Number'
    i = 0        
    for check in assess:
        if check:
            try:
                assess[i] = str(re.findall(r'/(.[^/]*?-ND)/',link_array[i])[0])
            except:
                assess[i] = False
        i += 1
    
    return assess
    

    #************* LOOP 2: Búsqueda en DK
#6 - Buscar en la API de DK linea por línea los 5 datos relevantes y hacer un dataset:
#    - Link
#    - Break Quantity
#    - Precio
#7 - Guardar "celda vacía" o su equivalente en Excel en las lineas que guardasemos "False"
#8 - Copiar todo a un Excel nuevo:
#    Columnas 1-3: datos de origen
#    Columnas 4-6: link, price break, price
#    Columnas 7-8: componente, fecha
#9 - Guardar el nuevo archivo Excel.
