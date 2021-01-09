from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import UserManager, User, Forum, ForumManager, Comment
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ContactForm
import stripe
from django.conf import settings

def index(request):
    return render(request, "main.html")

def logreg(request):
    return render(request, "logreg.html")

def register(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/logreg')

        user_pw=request.POST['pw']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/member')
    return redirect('/')

def log_in(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/member')
            else:
                messages.error(request, "Password was incorrect.")
        else:
            messages.error(request, "Email was not found.")
    return redirect('/logreg')

def newlog(request):
    return render(request, "signup.html")

def sign_up(request):
    if request.method=='POST':
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/newlog')

        user_pw=request.POST['pw']
        hash_pw=bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/forum')
    return redirect('/')

def sign_in(request):
    if request.method=='POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/forum')
            else:
                messages.error(request, "Password was incorrect.")
        else:
            messages.error(request, "Email was not found.")
    return redirect('/newlog')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, "member.html")

def about(request):
    return render(request, "about.html")

def coach(request):
    return render(request, "coach.html")

def tutorials(request):
    if 'user_id' in request.session:
        return redirect('/member')
    return render(request, "tutorials.html")

def virtual(request):
    return render(request, "virtual.html")

def forum(request):
    if 'user_id' not in request.session:
        return redirect('/no_access')
    context = {
        'all_messages':Forum.objects.all()
    }
    return render(request, "policy.html", context)

def no_access(request):
    return render(request, "no_access.html")

def logout(request):
    request.session.clear()
    return redirect('/')

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
        print(form)
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success/')
    return render(request, "contact.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

def purchase(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(1500)
    description = 'Video Analysis'
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )
        except stripe.error.CardError as e:
            return False,e
    return render(request, "purchase.html", dict(data_key = data_key, stripe_total = stripe_total, description = description))

def charge(request):
    return render(request, "charge.html")

def add_like(request, user_id):
    liked_message = Forum.objects.get(id=user_id)
    print(f'user_id{user_id}')
    print(liked_message)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    print(user_liking.first_name)
    return redirect('/forum')

def create_mess(request):
    if request.method=='POST':
        print(request.POST)
        error=Forum.objects.empty_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/forum')
        Forum.objects.create(content=request.POST['contents'], poster=User.objects.get(id=request.session['user_id']))
        return redirect('/forum')
    return redirect('/')

def delete_mess(request, mess_id):
    Forum.objects.get(id=mess_id).delete()
    return redirect('/forum')

def create_comm(request):
    if request.method=='POST':
        Comment.objects.create(content=request.POST['contents'], poster=User.objects.get(id=request.session['user_id']), message=Forum.objects.get(id=request.POST['message']))
        return redirect('/forum')
    return redirect('/')

def delete_comm(request, comm_id):
    Comment.objects.get(id=comm_id).delete()
    return redirect('/forum')