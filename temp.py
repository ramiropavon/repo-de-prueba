#@author: El mas grande y el mejor

import matplotlib.pyplot as plt
import pandas as pd
import requests
# import pandas as pd
import json
from typing import Union
import datetime

# =============================================================================
# Generacion del Token para realizar las consultas
# =============================================================================

def token():
    url = "https://api.invertironline.com/token"
    data = {
            'username':'ramiropavon96@gmail.com',
            'password': 'ctv1KDG@ynv3ava.fre',
            'grant_type':'password'
            }
    # r = requests.post(url=url,data=data).text
    # respuesta = json.loads(r)
    # access_token = respuesta['access_token']
    # refresh_token = respuesta['refresh_token']
    access = json.loads(requests.post(url=url, data=data).text)['access_token']
    refresh = json.loads(requests.post(url=url, data=data).text)['refresh_token']
    return access

# =============================================================================
# Acceso a los datos de mi cuenta
# =============================================================================

def datos_perfil():
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/datos-perfil"
    r = requests.get(url=url, headers=headers).text
    respuesta = json.loads(r)
    
    print(respuesta['apellido'])

def estado_cuenta():
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/estadocuenta"
    r = requests.get(url=url, headers=headers).text
    return r

def portafolio():
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/portafolio"
    data = {'pais':'argentina'}
    r = requests.get(url=url, headers=headers, data=data).text
    return r

def operaciones(estado:str,desde:str,hasta:str,pais:str):
    #Valores permitidos
    estado_correcto = ['todas', 'pendientes','terminadas','canceladas']
    if estado not in estado_correcto:
        return "El valor especificado en Estado no es un parametro valido"
    
    pais_correcto = 'argentina'
    if pais != pais_correcto:
        return "El valor especificado en Pais no es un parametro valido"    
    
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/operaciones"
    data = {'filtro.estado': estado,
            'filtro.fechaDesde': desde,
            'filtro.fechaHasta': hasta,
            'filtro.pais': pais
            }
    r = requests.get(url=url, headers=headers, data=data).text['apellido']
    print(r)

# =============================================================================
# Obtencion de Datos de mercado
# =============================================================================

def cotizacion(simbolo:str, simple = False):
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/bCBA/Titulos/"+str(simbolo)+\
        "/CotizacionDetalle"
    data = {'mercado':'bCBA',
            'simbolo':simbolo}
    r = requests.get(url=url,data=data, headers=headers).text
    if simple == False:
        print(r)
    else:
        dicc = {}
        respuesta = json.loads(r)
        dicc['simbolo'] = respuesta['simbolo']
        dicc['ultimoPrecio'] = respuesta['ultimoPrecio']
        dicc['maximo'] = respuesta['maximo']
        dicc['minimo'] = respuesta['minimo']
        dicc['cierreAnterior'] = respuesta['cierreAnterior']
        dicc['volumenNominal'] = respuesta['volumenNominal']
        dicc['cantidadOperaciones'] = respuesta['cantidadOperaciones']
        try:
            dicc['Bid'] = respuesta['puntas'][0]['precioCompra']
        except IndexError:
            dicc['Bid'] = None
        try:
            dicc['Ask'] = respuesta['puntas'][0]['precioVenta']
        except IndexError:
            dicc['Ask'] = None
        dicc['date'] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        asa = json.dumps(dicc)
        print(asa)

def cotizacion_bonos(mercado = 'argy', coin="pesos"):
    if mercado == 'argy':
        if coin == "pesos":
            bonos = ['AL29','AL30','AL35','AE38','AL41 ']
        if coin == "dolar":
            bonos = ['AL29D','AL30D','AL35D','AE38D','AL41D','BA7DD']
        if coin == "cable":
            bonos = ['AL29C','AL30C','AL35C','AE38C','AL41C']
    else:
        bonos=['GD29','GD30','GD35','GD38','GD41','GD46']
    #Hacer la devolucion como DF
    pass        

def mep(simbolo = None):
    bonos_locales = ['AL29','AL30','AL35','AE38','AL41']
    bonos_exterior = ['GD29','GD30','GD35','GD38','GD41','GD46']
    headers = {'Authorization': 'Bearer ' + token()}
    mep = {}
    if simbolo != None:
        url = "https://api.invertironline.com/api/v2/Cotizaciones/MEP/"+str(simbolo)
        data = {'simbolo':simbolo}
        r = requests.get(url=url,data=data, headers=headers).text
        return print(r)
    else:
        for i in bonos_locales:
            url = "https://api.invertironline.com/api/v2/Cotizaciones/MEP/"+str(i)
            data = {'simbolo':i}
            r = requests.get(url=url,data=data, headers=headers).text
            mep[i] = r
        for j in bonos_exterior:
            url = "https://api.invertironline.com/api/v2/Cotizaciones/MEP/"+str(j)
            data = {'simbolo':j}
            r = requests.get(url=url,data=data, headers=headers).text
            mep[j] = r
            
        return print(mep)

def cotizacion_historica(mercado:str, simbolo:str,desde:str,hasta:str):
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/"+\
        str(mercado)+"/Titulos/"+str(simbolo)+"/Cotizacion/seriehistorica/"+\
            str(desde) + str(hasta)+"ajustada"
    r = requests.get(url=url, headers=headers).text
    print(r)

def comprar_stock(simbolo: str,
                  cantidad: int,
                  precio: float,
                  plazo: str,
                  validez:str):
    
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/Operar/Comprar"
    data = {'mercado':"bCBA",
            'simbolo': simbolo,
            'cantidad': cantidad,
            'precio': precio,
            'plazo': plazo,
            'validez':validez,
            }
    
    if (cantidad*precio) > json.loads(estado_cuenta())['cuentas'][0]['disponible']:
        print ("No tenes saldo suficiente en la cuenta")
    else:
        comprar = requests.post(url, headers=headers, data=data)
        print(comprar.text)
    
def vender_stock(simbolo:str,
                cantidad:int,
                precio:float,
                plazo:str,
                validez:str):
    
    headers = {'Authorization': 'Bearer ' + token()}
    url = "https://api.invertironline.com/api/v2/Operar/Comprar"
    data = {'mercado':"bCBA",
            'simbolo': simbolo,
            'cantidad': cantidad,
            'precio': precio,
            'plazo': plazo,
            'validez':validez,
            }
     
    # Comprobar si el activo está en cartera
    en_cartera = []
    for i in json.loads(portafolio())['activos']:
        en_cartera.append(i['titulo']['simbolo'])
    posicion = en_cartera.index(simbolo)
    
    if simbolo not in en_cartera:
        print("No podes vender un activo que no tenes en el portafolio")
    
    elif cantidad > (json.loads(portafolio())['activos'][posicion]['cantidad']):
        print("No podes vender mas cantidad de activo que disponible en cartera")
        
        
    # Si pasa ese control, ejecutamos la funcion
    else:
        vender = requests.post(url, headers=headers, data=data)
        print(vender.text)
    


bonos_locales = ['AL29D','AL30D','AL35D','AE38D','AL41D', 'BA7DD']
for i in bonos_locales:
    cotizacion(i, simple=True) 
    print(" ")
mep()

def plot_cotizacion_historica(simbolo: str, desde: str, hasta: str):
    headers = {'Authorization': 'Bearer ' + token()}
    url_historico = "https://api.invertironline.com/api/v2/bCBA/Titulos/" + str(simbolo) + \
                    "/Cotizacion/seriehistorica/" + str(desde) + "/" + str(hasta) + "ajustada"
    
    try:
        historico = json.loads(requests.get(url=url_historico, headers=headers).text)
        if 'cierre' in historico:
            # Convertir datos históricos a DataFrame
            df = pd.DataFrame(historico['cierre'], columns=['date', 'value'])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)

             # Graficar
            plt.figure(figsize=(10, 6))
            plt.plot(df.index, df['value'], label=simbolo)
            plt.title(f'Cotización Histórica de {simbolo}')
            plt.xlabel('Fecha')
            plt.ylabel('Valor')
            plt.legend()
            plt.grid(True)
            plt.show()
        else:
            print(f"No se encontraron datos de cotización histórica para {simbolo}.")
    except Exception as e:
        print(f"Error al obtener cotización histórica para {simbolo}: {e}")

# Llamada a la función para plotear la cotización histórica del bono AL30D en un rango de fechas
plot_cotizacion_historica('AL30D', '2023-01-01', '2023-12-31')

