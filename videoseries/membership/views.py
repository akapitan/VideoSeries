from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Membership, UserMembership, Subcription
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
import stripe


def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)

    
    context = {
        'user_membership':user_membership,
        'user_subscription': user_subscription
    }
    return render(request, "membership/profile_view.html", context)

'''
Dohvaća korisnika s svim podacima o svojoj pretplati
'''
def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subcription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_suscription = user_subscription_qs.first()
        return user_suscription
    return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

'''
Class based view. Za postavljanje contexta se koristi fukcija get_context_data() s takvom sintaksom i vraća dictionary s svim podacima. 
U context dalje možemo upisivati podatke kad je dictionary. To je jednako kao u "Function based view" gdje dodajemo context = {} i onda render
'''
class MembershipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        
        current_membership = get_user_membership(self.request) ## Jer je ovo class based view moramo postaviti self
        context['current_membership'] = str(current_membership.membership_type)
        return context

    def post(self, request, **kwargs):
                
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_type = request.POST.get('membership_type')

        selected_membership_qs = Membership.objects.filter(membership_type= selected_membership_type)
        if selected_membership_qs.exists:
            selected_membership = selected_membership_qs.first()
        
        '''
        ==============
        Validation
        ==============
        '''
        if user_membership.membership_type == selected_membership:
            if user_subscription != None:
                messages.info(request, "You alredy have this membership \
                    Your next paiment is due {}".format('get this value from stripe'))
                return HttpResponseRedirect(request.META.get('HTTP_REFERER')) ## vrati korisnika od kud je došao

        #assing to the session, lijepo postavljanje sesije
        request.session['selected_membership_type'] = selected_membership.membership_type
        ## usmjeri korisnika na ovaj view
        return HttpResponseRedirect(reverse('memberships:payment'))

def PaymentView(request):
    user_membership = get_user_membership(request)

    selected_membership = get_selected_membership(request)

    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    
    if request.method == 'POST':
        try:
            
            token = request.POST['stripeToken']

            customer  = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            customer.source = token
            customer.save()


            subscription = stripe.Subscription.create(
                customer = user_membership.stripe_customer_id,   
                items = [
                    {"plan": selected_membership.stripe_plan_id},
                ]
            )

            return redirect(reverse('memberships:update-transactions', kwargs={
                'subscription_id': subscription.id 
            }))
        except stripe.error.CardError as e:
            messages.info(request, e)
        

    context = {
        'publishKey': publishKey ,
        'selected_membership':selected_membership
    }

    return render(request, "membership/memberships_payment.html", context)

def updateTransactions(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    user_membership.membership_type = selected_membership
    user_membership.save()

    sub, created = Subcription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del requese.session['selected_membership_type']
    except:
        pass
    
    messages.info(request, 'successfully created {} membership'.format(selected_membership))

    return redirect('/courses')

def cancelSubscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active == False:
        messages.info(request, "You don't have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
    
    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.filter(membership_type='Free').first()
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership.membership_type
    user_membership.save()

    messages.info(request, "Successfuly canceled membership")
    #send email here

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    



