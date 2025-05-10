import requests
from django.shortcuts import render, redirect
from django.conf import settings
from . import models


def verify_payment(request, cstr):
    main = models.course.objects.filter(c_str=cstr).first()
    print(main.price)
    reference = request.GET.get('reference')
    
    if not reference:
        return redirect(f'/payment/pay/{cstr}')
    
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result['data']['status'] == 'success':
        email = result['data']['customer']['email']
        amount = result['data']['amount'] / 100
        status = result['data']['status']
        
        valid =models.transaction.objects.filter(email=email, amount=amount, status=True).exists() 
        if not valid:
            models.transaction.objects.create(
                email=email,
                amount=amount,
                status=True,
                decript='payment for course',
            )
        return redirect(main.drive_link)
    else:
        # redirect to success page
        return render(request, 'payment_faild.html', {'course': main})
    

def lesson_verify_payment(request, cstr):
    main = models.lesson.objects.filter(lesson_str=cstr).first()
    print(main.price)
    reference = request.GET.get('reference')
    
    if not reference:
        return redirect(f'/lesson/pay/{cstr}')
    
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    response = requests.get(url, headers=headers)
    result = response.json()
    
    if result['data']['status'] == 'success':
        email = result['data']['customer']['email']
        amount = result['data']['amount'] / 100
        status = result['data']['status']
        
        valid =models.transaction.objects.filter(email=email, amount=amount, status=True).exists() 
        if not valid:
            models.transaction.objects.create(
                email=email,
                amount=amount,
                status=True,
                decript='payment for course',
            )
        return render(request, 'payment_succes.html', {'course': main})
    else:
        # redirect to success page
        return render(request, 'payment_faild.html', {'course': main})