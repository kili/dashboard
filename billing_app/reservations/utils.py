from billing_app.context_processors import balance

def package_affordable(reservation_id, request):
    return prepaid_reservation.total_price < balance(request)['balance'] 
