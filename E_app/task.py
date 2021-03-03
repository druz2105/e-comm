from .models import Customer, Address, Product_Detail, Order, OrderItem, Shoes_Size
import json
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from E_Comm import settings as se
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from django.core.mail import send_mail
from django.conf import settings

settings.SENDGRID_SANDBOX_MODE_IN_DEBUG = False


def confirm_order(user_id, email, id):
    global order_get
    try:
        order_qs = Order.objects.get(user=user_id, order_id=id)

        for i in order_qs.items.all():
            order_item_qs = OrderItem.objects.get(user=user_id, order_id=id)

            product_que = serializers.serialize("json", Product_Detail.objects.filter(product_name=i.item.product_name,
                                                                                      product_size__size=i.order_size))
            order_get = Order.objects.filter(user=user_id, order_id=id)
            data = [i['fields'] for i in json.loads(product_que)]
            product_que_s = Product_Detail.objects.get(product_name=i.item.product_name,
                                                       product_size__size=i.order_size)
            order_v = Order.objects.filter(user=user_id, order_id=id)

            for j in product_que_s.product_size.all():
                if j.count > 0:
                    if j.size == i.order_size:
                        j.count -= i.product_quantity
                        j.save()
                        if j.count >= 0:
                            order_item_qs.ordered = True
                            order_item_qs.save()
                            order_qs.confirmed = True
                            order_qs.save()
                            subject = 'Order Get Confirmed Will Be Delivered Soon'
                            html_message = render_to_string('mail_template.html',
                                                            {'order': order_v, 'object': order_qs})
                            plain_message = strip_tags(html_message)
                            from_email = 'druz2105@gmail.com'
                            to = email
                            message = Mail(
                                from_email=from_email,
                                to_emails=to,
                                subject=subject,
                                plain_text_content=plain_message,
                            )
                            sg = SendGridAPIClient(se.SENDGRID_API_KEY)
                            response = sg.send(message)
                            print(response.status_code)
                            print(response.body)
                            print(response.headers)
                    else:
                        order_item_qs.canceled = True
                        order_item_qs.save()
                        order_qs.canceled = True
                        order_qs.save()
                        subject = 'Order Get Canceled as item is not in stock'
                        plain_message = "Order GOT CANCELED REFUND WILL BE SENT IF PAYMENT WAS DONE BY CARD"
                        from_email = 'druz2105@gmail.com'
                        to = email
                        message = Mail(
                            from_email=from_email,
                            to_emails=to,
                            subject=subject,
                            plain_text_content=plain_message,
                        )
                        sg = SendGridAPIClient(se.SENDGRID_API_KEY)
                        response = sg.send(message)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)

                else:
                    Shoes_Size.objects.filter(size=i.order_size, count=0).delete()
                    order_item_qs.canceled = True
                    order_item_qs.save()
                    order_qs.canceled = True
                    order_qs.save()
                    subject = 'Order Get Canceled as item is not in stock'
                    plain_message = "Order GOT CANCELED REFUND WILL BE SENT IF PAYMENT WAS DONE BY CARD"
                    from_email = 'druz2105@gmail.com'
                    to = email
                    message = Mail(
                        from_email=from_email,
                        to_emails=to,
                        subject=subject,
                        plain_text_content=plain_message,
                    )
                    sg = SendGridAPIClient(se.SENDGRID_API_KEY)
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
    except ObjectDoesNotExist:
        print("hey")
