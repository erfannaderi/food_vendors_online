def detect_user(user):
    if user.role == 2:
        redirect_url = 'client-dashboard'
        return redirect_url
    elif user.role == 1:
        redirect_url = 'restaurant-dashboard'
        return redirect_url
    # elif user.role == "UNKNOWN" and user.is_superuser:
    else:
        if user.is_superuser:
            redirect_url = '/admin'
            return redirect_url
