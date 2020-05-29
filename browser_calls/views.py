from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from twilio.jwt.client import ClientCapabilityToken
from twilio.twiml.voice_response import VoiceResponse


@login_required
def get_token(request):
    """Returns a Twilio Client token"""

    # Create a TwilioCapability token with our Twilio API credentials
    capability = ClientCapabilityToken(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
    )

    # Allow our users to make outgoing calls with Twilio Client
    capability.allow_client_outgoing(settings.TWIML_APPLICATION_SID)

    capability.allow_client_incoming('awareness_user')

    # Generate the capability token
    token = capability.to_jwt()

    return JsonResponse({'token': token.decode('utf-8')})


@login_required
@csrf_exempt
def call(request):
    """Returns TwiML instructions to Twilio's POST requests"""

    response = VoiceResponse()
    dial = response.dial(caller_id=settings.TWILIO_NUMBER)

    dial.client('understand_user')

    return HttpResponse(
        str(response), content_type='application/xml; charset=utf-8'
    )
