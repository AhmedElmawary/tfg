import requests
import json
from tfg.settings import ACCEPT_CONF


# def paymoblog(title, text='\n\n'):
#     import datetime
#     x = open('paymoblog.txt', 'a')
#     string = datetime.datetime.now().strftime(
#         '%d/%m/%Y, %I:%M:%S %p, ') + title + ': ' + str(text)
#     x.write(string+'\n')
#     x.close()


# INPUT: merchant's credentials
# OUTPUT: authentication token , merchant id
def get_order_token():
    url = "https://accept.paymobsolutions.com/api/auth/tokens"
    payload = {"api_key": ACCEPT_CONF["API_KEY"]}
    headers = {"content-type": "application/json"}
    modified_payload = json.dumps(payload)
    # paymoblog('Sending to paymob credentials requiring authentication',
    #   modified_payload)
    response = requests.post(url, data=modified_payload, headers=headers)
    # paymoblog('Paymob Response', response)
    response = response.json()
    # paymoblog('Response in Jason', response)
    final_response = {
        "token": response["token"],
        "merchant_id": response["profile"]["id"],
    }
    # paymoblog('Converted response', final_response)
    return final_response


# INPUT: return output from authentication method + amount + currency + shipping_info. The items, merchant order id,
# delivery need are optional fields.
# OUTPUT: order id
def create_order(
    get_token_response,
    amount,
    currency,
    shipping_info,
    items=False,
    merchant_order_id=False,
    delivery_needed=False,
):
    url = "https://accept.paymobsolutions.com/api/ecommerce/orders"
    querystring = {"token": get_token_response["token"]}
    payload = {
        "delivery_needed": delivery_needed,
        "merchant_id": get_token_response["merchant_id"],
        "amount_cents": amount,
        "currency": currency,
        "items": [],
        "shipping_data": shipping_info,
    }
    if merchant_order_id:
        payload["merchant_order_id"] = merchant_order_id
    if items:
        payload["items"] = items
    headers = {"content-type": "application/json"}
    modified_payload = json.dumps(payload)
    # paymoblog('Sending to paymob to create an order', modified_payload)
    response = requests.post(
        url, data=modified_payload, headers=headers, params=querystring
    )
    response = response.json()
    # paymoblog('Response', response)

    get_token_response["order_id"] = response["id"]
    get_token_response["amount"] = amount
    get_token_response["currency"] = currency
    return get_token_response


# INPUT: return output from order creation method + merchant's card integration ID + client's billing information
# OUTPUT: payment key token


def generate_payment_key(
    previous_response,
    card_integration_id,
    billing_info,
    items=False,
    installment_plan=False,
):
    url = "https://accept.paymobsolutions.com/api/acceptance/payment_keys"
    querystring = {"token": previous_response["token"]}
    payload = {
        "amount_cents": previous_response["amount"],
        "currency": previous_response["currency"],
        "card_integration_id": card_integration_id,
        "order_id": previous_response["order_id"],
        "billing_data": billing_info,
    }
    if items:
        payload["items"] = items
    if installment_plan:
        payload["installment_plan"] = installment_plan
    headers = {"content-type": "application/json"}
    modified_payload = json.dumps(payload)
    # paymoblog('Sending to paymob to create payment key', modified_payload)
    response = requests.post(
        url, data=modified_payload, headers=headers, params=querystring
    )
    response = response.json()
    # paymoblog('Response', response)
    previous_response["payment_key"] = response["token"]
    # LOG
    # paymoblog('payment_key', response['token'])
    # paymoblog('End of transaction')
    return previous_response
