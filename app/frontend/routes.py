from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from nicegui import ui

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@ui.page('/')
def fraud_detection_ui():
    ui.label('Irish Fraud Detection System').classes('text-h3')
    
    with ui.card():
        ui.label('Enter Transaction Details').classes('text-h5')
        transaction_id = ui.input('Transaction ID')
        amount = ui.number('Amount (€)')
        sender = ui.input('Sender Account')
        recipient = ui.input('Recipient Account')
        description = ui.input('Description')
        ip_address = ui.input('IP Address')
        
        async def submit():
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'http://localhost:8000/api/detect-fraud',
                    json={
                        'id': transaction_id.value,
                        'amount': amount.value,
                        'sender': sender.value,
                        'recipient': recipient.value,
                        'description': description.value,
                        'ip_address': ip_address.value
                    }
                )
                result = response.json()
                ui.notify(f"Risk Level: {result['fraud_detection_result']['risk_level']}")
                with result_card:
                    ui.label(f"Risk Score: {result['fraud_detection_result']['risk_score']}")
                    ui.label(f"Risk Level: {result['fraud_detection_result']['risk_level']}")
                    ui.label("Risk Factors:")
                    for factor in result['fraud_detection_result']['risk_factors']:
                        ui.label(f"- {factor}")
        
        ui.button('Check for Fraud', on_click=submit)
    
    with ui.card() as result_card:
        ui.label('Fraud Detection Results').classes('text-h5')

ui.run()