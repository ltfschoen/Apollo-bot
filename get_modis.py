# TODO

# import requests
# import pandas as pd
#
#
# def get_modis(mod = 'MOD11A1.005', startdate = '03-01-2005', enddate = '09-01-2005'):
#     SERVICES_URL = 'https://lpdaacsvc.cr.usgs.gov/services/appeears-api'
#     products_req = requests.get('%s/product?rasterType=tile&format=json' % (SERVICES_URL))
#     products = products_req.json()
#     product = next(p for p in products if p['ProductAndVersion'] == mod)
#     product_layers_req = requests.get('%s/product/%s?format=json' % (SERVICES_URL, product['ProductAndVersion']))
#     product_layers = product_layers_req.json()
#     sample_url = '{0}/sample?'.format(SERVICES_URL)
#     latitude, longitude = '45.50894', '-89.58637'
#     sample_args = {
#         'product': product['ProductAndVersion'],
#         'layer': product_layers['LST_Day_1km']['Layer'],
#         'startdate': startdate,
#         'enddate': enddate,# like '09-01-2005',
#         'coordinate': '{0},{1}'.format(latitude, longitude),
#         'format': 'json'
#     }
#     sample_req = requests.get(sample_url, params=sample_args)
#     samples = sample_req.json()
#     lstData = pd.DataFrame.from_dict(samples)
#     return lstData
#
