
from .models import *
from django.shortcuts import render
import razorpay
from .forms import PaymentForm

def payment(request):
    if request.method == "POST":
        
        name = request.user
        amount1=request.POST.get('amount')
        amount = int(request.POST.get('amount')) *100
        client = razorpay.Client(auth=('rzp_test_48Z9LMTDVAN5JU', 'gMxfhwgZ73ANYJQCeblLMy7W'))
        response_payment = client.order.create(dict(amount=amount,
                                                    currency='INR')
                                               )

        order_id = response_payment['id']
        order_status = response_payment['status']
        
        if order_status == 'created':
            payment = Payment(
                user=request.user,
                name=name,
                amount=amount1,
                order_id=order_id,
               
            )
          
        payment.save()
        response_payment['name'] = name

        form = PaymentForm(request.POST or None)
        return render(request, 'payment/payment.html', {'form':form,'payment': response_payment})

    form = PaymentForm()
    return render(request, 'payment/payment.html', {'form': form})


def payment_status(request):
    response = request.POST
    params_dict = {

       'razorpay_order_id': response['razorpay_order_id'],
       'razorpay_payment_id': response['razorpay_payment_id'],
       'razorpay_signature': response['razorpay_signature'],
     
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_48Z9LMTDVAN5JU', 'gMxfhwgZ73ANYJQCeblLMy7W'))
    

    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.user=request.user
        payment.is_paid = True
        payment.save()

       
        
        return render(request, 'payment/payment_status.html', {'status': True,'payment_id':payment.payment_id})
    except:
        return render(request, 'payment/payment_status.html', {'status': False})




