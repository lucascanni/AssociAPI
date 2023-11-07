from fastapi import APIRouter, Header, Request, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse
import stripe
from firebase_admin import auth
from database.firebase import db
from routers.router_auth import get_current_user
from dotenv import dotenv_values
from datetime import datetime
from dateutil.relativedelta import relativedelta


router = APIRouter(
    tags=["Stripe"],
    prefix='/stripe'
)

config = dotenv_values("/etc/secrets/.env")
# config = dotenv_values(".env")
stripe.api_key=config['STRIPE_SK'] # votre API KEY

YOUR_DOMAIN = config['DOMAIN']

@router.get('/checkout')
async def stripe_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # PRICE ID du produit que vous vouler vendre
                    'price':'price_1O9TEDGQ2alTbrjjclqgIWDH',
                    'quantity' : 1,
                },
            ],
            mode='subscription',
            payment_method_types=['card'],
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        response = RedirectResponse(checkout_session['url'])
        return response
    except Exception as e:
        return str(e)
  
    
@router.post('/webhook')
async def webhook_received(request:Request, stripe_signature: str = Header (None)):
    webhook_secret = config['WEBHOOK_SECRET']
    data = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload = data,
            sig_header=stripe_signature,
            secret=webhook_secret
        )
        event_data =event['data']
    except Exception as e:
        return  {"error":str(e)}
    
    event_type = event['type']
    if event_type == 'checkout.session.completed':
        print('checkout session completed')
    elif event_type == 'invoice.paid':
        print('invoice paid')
        cust_email = event_data['object']['customer_email'] # email de notre customer
        fireBase_user = auth.get_user_by_email(cust_email) # Identifiant firebase correspondant (uid)
        cust_id =event_data['object']['customer'] # Stripe ref du customer
        item_id= event_data['object']['lines']['data'][0]['subscription_item']
        start_date= datetime.now()
        end_date= start_date + relativedelta(months=+1)

        db.child("users").child(fireBase_user.uid).child("stripe").set({"item_id":item_id, "cust_id":cust_id,"end_date":end_date.isoformat(),"start_date":start_date.isoformat()}) # écriture dans la DB firebase      

    elif event_type == 'invoice.payment_failed':
        print('invoice payment failed')
    else:
        print(f'unhandled event: {event_type}')

    return {"status": "success"}

@router.get('/usage')
async def stripe_usage(userData: int = Depends(get_current_user)):
    fireBase_user = auth.get_user(userData['uid']) # Identifiant firebase correspondant (uid)
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    cust_id =stripe_data['cust_id']
    return stripe.Invoice.upcoming(customer=cust_id)

# Ne fonctionne pas car je fonctionne par abonnement
def validation_abonnement(userId:str):
    fireBase_user = auth.get_user(userId) # Identifiant firebase correspondant (uid)
    stripe_data= db.child("users").child(fireBase_user.uid).child("stripe").get().val()
    if stripe_data is None:
        raise HTTPException(status_code=401, detail="Aucun abonnement trouvé")
    else:
        date_request = datetime.now()
        end_date = datetime.fromisoformat(stripe_data['end_date'])
        if date_request < end_date:
            return True
        else:
            raise HTTPException(status_code=401, detail="Abonnement expiré")
        