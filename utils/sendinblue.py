import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
import os

API_KEY = os.environ.get('SENDINBLUE_API_KEY')
CONTACT_EMAIL = os.environ.get('CONTACT_EMAIL')
SENDINBLUE_CONTACT_TEMPLATE_ID = int(os.environ.get('SENDINBLUE_CONTACT_TEMPLATE_ID'))

def send_transactional_email(email,data,template_id):
    """Send transactional email """
    # Configure API key authorization: api-key
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = API_KEY

    # Uncomment below lines to configure API key authorization using: partner-key
    # configuration = sib_api_v3_sdk.Configuration()
    # configuration.api_key['partner-key'] = 'YOUR_API_KEY'

    # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{
            "email":email,
        }], 
        template_id=template_id,
        params=data, 
        headers={"X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3", "charset": "iso-8859-1"}) 
        # SendSmtpEmail | Values to send a transactional email

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

def send_contact_email(data):
    """Wrapper from send transactional email to send specifically the contact form email """
    send_transactional_email(CONTACT_EMAIL,data,SENDINBLUE_CONTACT_TEMPLATE_ID)