# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 15:12:31 2020

@author: Virgilio

Modificar en las líneas 106 y 46 los archivos a tratar (deben ser excel.xlsm)
"""
from vir import *

# Abre un navegador para autenticarse, devuelve en la URL el código a copiar.
code_request()

# Introducir el codigo obtenido tras autenticarse 
print('\nInput code:')
code = input()

# Peticion de Token al servidor de DK
token = token_request(code)
access_token = token['access_token']
refresh_token = token['refresh_token']

# Peticion de un nuevo Token y actualización de las variables
token = brand_new_token(refresh_token)
access_token = token['access_token']
refresh_token = token['refresh_token']

# Part_Number de ejemplo
part_number = 'SI5338Q-B06555-GM-ND' # DK part_number

# Obtenemos la info de la DB de DK
component = product_search(access_token, part_number)

## Imprime toda la info del componente
#import pprint
#print ('\nCOMPONENT INFORMATION:\n')
#pprint.pprint(component)

# Obtenemos los datos relevantes del componente
pricing_data = get_pricing_data(component)

# Pruebas
#pprint.pprint(pricing_data)
#print(component['StandardPricing'][len(component['StandardPricing'])-1]['BreakQuantity'])
#print(component['StandardPricing'][len(component['StandardPricing'])-1]['UnitPrice'])

# Extraemos los 'Digikey part_number" de los links de la primera columna
excel_file_path = 'API Pricing Update Test.xlsm'
dk_part_number_list = parse_dk_part_number(excel_file_path)

# Buscamos los componentes mediante la API de DK
list_of_dict = list()
i = 0
for dk_part_number in dk_part_number_list:
    if dk_part_number:
        list_of_dict.append(product_search(access_token, str(dk_part_number)))
    else:
        list_of_dict.append(False)
    i += 1
    
#Abrimos un fichero .csv para imprimir los resultados
#import csv
#with open('output.csv', 'w') as output:
#    writer = csv.writer(output)
#    
#    # Obtenemos los datos relevantes de los componentes y los escribimos en el fichero
#    for component in list_of_dict:
#        if component:
#            pricing_data = get_pricing_data(component)
#            for key, value in pricing_data.items():
#                writer.writerow([value])
    
# Obtenemos los datos relevantes de los componentes y los escribimos en el fichero
link_list = list()
price_break_list = list()
price_list = list()
comp_list = list()
date_list = list()
i = 0
for component in list_of_dict:
    if component:
        try:
            pricing_data = get_pricing_data(component)
            link_list.append(pricing_data['component_url'])
            price_break_list.append(pricing_data['break_quantity'])
            price_list.append(pricing_data['standard_pricing'])
            comp_list.append((pricing_data['manufacturer'] + ' ' + pricing_data['manufacturer_part_number']))
            date_list.append(pricing_data['date'])
        except:
           link_list.append('')
           price_break_list.append('')
           price_list.append('')
           comp_list.append('')
           date_list.append('')
            
    else:
        link_list.append('')
        price_break_list.append('')
        price_list.append('')
        comp_list.append('')
        date_list.append('')
    i += 1
            
pprint.pprint(component)

import xlsxwriter

workbook   = xlsxwriter.Workbook('PL BreakPrice Up to date.xlsx')
    
worksheet1 = workbook.add_worksheet()

# Escribimos las cabeceras
headerrrrsss = ["_Link", "_Price Break", "_Price", "_Component","_Date"]
worksheet1.write_row('A1', headerrrrsss)

#Escribimos los datos en las columnas
worksheet1.write_column('A2', link_list)
worksheet1.write_column('B2', price_break_list)
worksheet1.write_column('C2', price_list)
worksheet1.write_column('D2', comp_list)
worksheet1.write_column('E2', date_list)

workbook.close()


#i = 0
#print('\nCOMPONENT DATA:\n')
## Obtenemos los datos relevantes de los componentes y los imprimimos
#for component in list_of_dict:
#    if component:
#        pricing_data = get_pricing_data(component)
#        
#        # Imprimimos resultados
#        print('Product: ' + pricing_data['manufacturer'] + ' ' + pricing_data['manufacturer_part_number'])
#        print('Break Quantity: ' + str(pricing_data['break_quantity']))
#        print('Unit Price: ' + str(pricing_data['standard_pricing']))
#        print('URL:' + pricing_data['component_url'])
#        print('Date: ' + pricing_data['date'])
#        print('\n')
#    i += 1
