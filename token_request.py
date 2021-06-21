# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 16:37:24 2020

@author: Virgilio
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 15:12:31 2020

@author: Virgilio
"""

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
    
    #Imprime el diccionario cuidando la visualización
    print ('\nTOKEN:\n')
    pprint.pprint (token_json)