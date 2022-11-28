import requests
import json

# redx in python 

redx_token = 'your-token-number'
headers = {'API-ACCESS-TOKEN':  f'Bearer {redx_token}' }
api_get = 'https://sandbox.redx.com.bd/v1.0.0-beta/parcel/info/2211A6SUOSB77'
response = requests.get(api_get, headers=headers)

print(response.json())



# redx in django , parcel create

def create_redx_parcel(request,pk):
    order = Order.objects.get(pk=pk)
    form = PercelForm(request.POST)
    if request.method == 'POST':
        form = PercelForm(request.POST)
        if form.is_valid():
            form.instance.order = order
            form.instance.customer_name = order.shipping_address.full_name
            form.instance.customer_phone = order.shipping_address.phone
            form.instance.customer_address = order.shipping_address.full_address
            form.instance.merchant_invoice_id =  order.id
            form.instance.cash_collection_amount = order.due_amount
    
            token = 'your-token-number'
            api_url = 'https://sandbox.redx.com.bd/v1.0.0-beta/parcel'

            payload = json.dumps({
            "customer_name": order.shipping_address.full_name,
            "customer_phone":  order.shipping_address.phone,
            "delivery_area":  request.POST.get('delivery_area'),
            "delivery_area_id": 1,
            "customer_address":  order.shipping_address.full_address,
            "merchant_invoice_id": str(order.id),
            "cash_collection_amount":  order.due_amount,
            "parcel_weight":  request.POST.get('parcel_weight'),
            })
            headers = {
                "Content-Type": "application/json",
                'API-ACCESS-TOKEN':  f'Bearer {token}'
            }
            response = requests.request("POST", api_url, headers=headers, data=payload)
            print(response.text)

            resp = json.loads(response.text)

            for x in resp:
                form.instance.tracking_id = resp[x]
            
            form.save()
            order.order_traking_number = form.instance.tracking_id
            order.save()
            
            return redirect('all-order')
    else:
        form = PercelForm()
        return render(request, 'dashboard/order_parcel/redx-percel-create.html',{'form':form, 'order':order})


