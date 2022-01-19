
import requests
import hashlib
import hmac


def get_status(token)->str:
    base_url = 'https://sandbox.flow.cl/api/'
    secret_key = "523ffbf4a580332ec97c58cd55e4cf1fb0e06791"

    api_url = 'payment/getStatus'
    url = f'{base_url}' + f'{api_url}'

    params = {
        'apiKey': "4EAAFAC5-6F1A-4855-88E2-9A2DE6934L1D",
        'token': token,
    }

    s = sign(secret_key, params)
    params['s'] = s

    response = requests.get(url, params)

    data = response.json()['status']
    #print(data)
    return data


def flow_payment(amount, order):
    base_url = 'https://sandbox.flow.cl/api/'
    secret_key = "523ffbf4a580332ec97c58cd55e4cf1fb0e06791"
    params = {
        'apiKey': "4EAAFAC5-6F1A-4855-88E2-9A2DE6934L1D",
        #'commerceOrder': str(order*2),
        'commerceOrder': order,
        'subject': "Test charge from Dbeers",
        'amount': amount,
        'email' : 'toto.palacios.a@gmail.com',
        'urlConfirmation': 'https://cevtrapiche-django.herokuapp.com/api/v1/confirmation/',
        'urlReturn': 'https://cevtrapiche-django.herokuapp.com/api/v1/confirmation/',
    }

    s = sign(secret_key, params)
    params['s'] = s

    api_url = 'payment/create'
    url = f'{base_url}' + f'{api_url}'
    

    response = requests.post(url, params)
    print(response)

    status = response.status_code
    #print(status)
    if status == 200:
        json = response.json()
        redirect_url = json['url'] + '?token=' + json['token']
        flow_order = json['flowOrder']

        dict = {
            'redirect_url': redirect_url,
            'flow_order': flow_order
        }

        return (dict)
        


def sign(apikey, params):
        """Crea el Hash de validacion para ser enviado con la informacion
        :rtype: str
        """
        string = ""
        for k, d in sorted(params.items()):
            if d is not None:
                string = string + f"{k}{d}"
        hash_string = hmac.new(
            apikey.encode(), string.encode(), hashlib.sha256
        ).hexdigest()

        return hash_string