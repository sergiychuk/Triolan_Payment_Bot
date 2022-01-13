# token = '5074195246:AAGClhdTA3IMwjkphYCAj_OupzfrXJE1cyE'  # @triolan_payment_bot
token = '5079445012:AAHfRtAEbsXcmeKK1rGM4mOA8Y4I-6HNZxI'
debug_mode = False
cid = 0
main_url = "https://triolan.name"
account = 3658365
account_phone = '380962614481'
service_status = False
paid_until = '2021-08-08'


def set_service_status(service_bool):
    global service_status
    service_status = service_bool


def set_paid_until_date(date):
    global paid_until
    paid_until = date
