from billing_app.context_processors import balance

def package_affordable(reservation_id, request):
    return prepaid_reservation.upfront_price < balance(request)['balance'] 
