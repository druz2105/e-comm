from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField
from django.urls import reverse
from django.conf import settings
import uuid

COUNTRY_CHOICES = (('I', "INDIA"), ('P', "PAKISTAN"), ('B', 'Bangladesh'))
Add_Choices = (('S', 'Shipping'), ('B', "Billing"))
Product_Type = [('S', "Shoes"), ('C', "Clothes"), ('W', "Watch"), ('L', "Laptop"), ('M', "Mobile")]
Product_Type.sort()


# Create your models here.
class Address(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    apartment_address = models.CharField(max_length=20, null=False, blank=False)
    street_address = models.CharField(max_length=20, null=False, blank=False)
    state = models.CharField(max_length=20, null=False, blank=False)
    zip = models.CharField(max_length=8, null=False, blank=False)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, null=False, blank=False)
    address_type = models.CharField(max_length=1, choices=Add_Choices)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.apartment_address + ' ' + self.street_address + ' ' + self.state


class Customer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=10, null=False, blank=True)
    alternate_mobile_number = models.CharField(max_length=10, null=False, blank=True)
    addresses = models.ManyToManyField(Address)

    def __str__(self):
        return self.user_id.username


Gender = [('K', 'Kids'), ('M', 'Male',), ('F', 'Female'), ('U', "Unisex")]


class Product_Detail(models.Model):
    image0 = models.ImageField(upload_to='file/', blank=False)
    image1 = models.ImageField(upload_to='file/', blank=False)
    image2 = models.ImageField(upload_to='file/', blank=True)
    product_name = models.CharField(max_length=100, null=False, blank=False)
    product_price = models.FloatField(null=False, blank=False)
    product_color = models.CharField(max_length=10, null=False, blank=False)
    product_type = models.CharField(max_length=2, choices=Product_Type)
    product_details = models.CharField(max_length=1000, null=False, blank=False)
    product_deal_week = models.BooleanField(default=False)
    product_deal_month = models.BooleanField(default=False)
    added_date = models.DateField(auto_now_add=True)
    deal_price = models.FloatField(null=True, blank=True)
    discount = models.IntegerField(default=10)
    shoes_detail = models.ForeignKey('Shoes', on_delete=models.SET_NULL, null=True, blank=True)
    clothe_detail = models.ForeignKey('Clothes', on_delete=models.SET_NULL, null=True, blank=True)
    watch_detail = models.ForeignKey('Watches', on_delete=models.SET_NULL, null=True, blank=True)
    laptop_detail = models.ForeignKey('Laptop', on_delete=models.SET_NULL, null=True, blank=True)
    mobile_detail = models.ForeignKey('Mobile', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.product_name

    @property
    def value(self):
        if self.product_type == 'S':
            return self.shoes_detail
        elif self.product_type == 'C':
            return self.clothe_detail
        elif self.product_type == 'W':
            return self.watch_detail
        elif self.product_type == "L":
            return self.laptop_detail
        elif self.product_type == 'M':
            return self.mobile_detail
        else:
            pass

    @property
    def img_url(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url


Type = [('R', 'Running'), ('Sp', 'Sports'), ('Sn', 'Sneakers'), ('Fo', 'Formal'), ('L', "Loafer")]
Type.sort()
Shoes_Brand = [('A', "Adidas"), ('P', "Puma"), ('N', "Nike"),
               ('L', "Lotto"), ("R", "Reebok"), ('NB', "New Balance"),
               ('AS', "Asics"), ('F', "Fila")]
Shoes_Brand.sort()


class Shoes(models.Model):
    product_gender = models.CharField(max_length=1, choices=Gender)
    shoe_brand = models.CharField(max_length=2, choices=Shoes_Brand)
    shoe_type = models.CharField(max_length=2, choices=Type)
    shoes_size = models.ManyToManyField('Shoes_Size')

    def __str__(self):
        return self.shoe_brand


class Shoes_Size(models.Model):
    size = models.IntegerField(null=True, blank=False)
    count = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return str(self.size)


class Clothes(models.Model):
    product_gender = models.CharField(max_length=1, choices=Gender)
    cloth_type = models.CharField(max_length=20, null=True, blank=True)
    cloth_brand = models.CharField(max_length=15, null=True, blank=True)
    cloth_size = models.ManyToManyField('Clothes_Size')
    wear_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.cloth_type)


size_choice = [('S', "Small"), ('M', "Medium"), ('L', "Large"), ('XL', "Extra Large"), ("XXL", "Extra Extra Large"),
               ("XXXL", "Extra Extra Extra Large"), ('O', "Other")]
size_choice.sort()


class Clothes_Size(models.Model):
    size = models.CharField(max_length=4, choices=size_choice, null=True, blank=True)
    count = models.IntegerField()

    def __str__(self):
        return str(self.cloth_size)



class Watches(models.Model):
    product_gender = models.CharField(max_length=1, choices=Gender)
    watch_brand = models.CharField(max_length=20,  null=True, blank=True)
    count = models.IntegerField()

    def __str__(self):
        return self.watch_brand


Laptop_Brand = [('A', "Asus"), ('AC', "Acer"), ('AP', "Apple"), ('D', "Dell"), ('H', "HP"), ('L', "Lenovo"),
                ('S', "Sony")]
Laptop_Brand.sort()
storage_type = [('S', "SDD"), ('H', "HDD")]
storage_type.sort()


class Laptop(models.Model):
    count = models.IntegerField()
    model_year = models.IntegerField(null=True, blank=True)
    model_name = models.CharField(max_length=20, null=True, blank=True)
    laptop_brand = models.CharField(max_length=2, choices=Laptop_Brand, null=True, blank=True)
    screen_size = models.CharField(max_length=4, null=True, blank=True)
    screen_type = models.CharField(max_length=50, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    processor_brand = models.CharField(max_length=10, null=True, blank=True)
    processor_speed = models.CharField(max_length=50, null=True, blank=True)
    processor_type = models.CharField(max_length=50, null=True, blank=True)
    resolution = models.CharField(max_length=20, null=True, blank=True)
    ram = models.CharField(max_length=20, null=True, blank=True)
    storage_type = models.CharField(max_length=1, choices=storage_type, null=True, blank=True)
    storage_size = models.CharField(max_length=40, null=True, blank=True)
    hard_drive_interface = models.CharField(max_length=40, null=True, blank=True)
    hard_drive_rotation_speed = models.CharField(max_length=40, null=True, blank=True)
    operating_system = models.CharField(max_length=40, null=True, blank=True)
    graphics_card_detail = models.CharField(max_length=20, null=True, blank=True)
    graphics_card_ram_type = models.CharField(max_length=50, null=True, blank=True)
    graphics_card_interface = models.CharField(max_length=50, null=True, blank=True)
    graphics_coprocessor = models.CharField(max_length=50, null=True, blank=True)
    battery_details = models.CharField(max_length=30, null=True, blank=True)
    max_memory_supported = models.CharField(max_length=50, null=True, blank=True)
    usb_port = models.IntegerField()
    optical_drive_type = models.CharField(max_length=100, null=True, blank=True)
    hardware_interface = models.CharField(max_length=250, null=True, blank=True)
    manufacturer = models.CharField(max_length=50, null=True, blank=True)
    connector_type = models.CharField(max_length=50, null=True, blank=True)
    power_source = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.model_name


Mobile_brand = [('A', "Apple"), ('B', "Black Berry"), ('MI', "RedMi"), ('OP', "One Plus"), ('O', "Oppo"), ('V', "Vivo"),
                ('SS', "Samsung"), ('S', "Sony"), ('N', "Nokia"), ('M', "Motorola"), ('L', "Lava")]
Mobile_brand.sort()


class Mobile(models.Model):
    count = models.IntegerField()
    model_name = models.CharField(max_length=20, null=True, blank=True)
    mobile_brand = models.CharField(max_length=2, choices=Mobile_brand, null=True, blank=True)
    screen_size = models.CharField(max_length=40, null=True, blank=True)
    screen_type = models.CharField(max_length=50, null=True, blank=True)
    dimensions = models.CharField(max_length=30, null=True, blank=True)
    display_technology = models.CharField(max_length=70, null=True, blank=True)
    weight = models.CharField(max_length=30, null=True, blank=True)
    wireless_communication = models.CharField(max_length=30, null=True, blank=True)
    connectivity_technology = models.CharField(max_length=40, null=True, blank=True)
    operating_system = models.CharField(max_length=40, null=True, blank=True)
    ram = models.CharField(max_length=40, null=True, blank=True)
    rom = models.CharField(max_length=40, null=True, blank=True)
    front_camera_number = models.IntegerField()
    back_camera_number = models.IntegerField()
    camera_details = models.CharField(max_length=50, null=True, blank=True)
    box_detail = models.CharField(max_length=80, null=True, blank=True)
    battery_power = models.CharField(max_length=40, null=True, blank=True)
    special = models.CharField(max_length=400, null=True, blank=True)
    manufacturer = models.CharField(max_length=200, null=True, blank=True)
    packer = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.model_name


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product_Detail, on_delete=models.CASCADE)
    product_quantity = models.IntegerField(default=1)
    order_size = models.CharField(max_length=5, null=True, blank=True)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.item.product_name

    def get_total_item_price(self):
        if self.product_quantity <= 0:
            return 0
        else:
            return self.product_quantity * self.item.product_price

    def get_total_disc_price(self):
        if self.product_quantity <= 0:
            return 0
        else:
            return self.product_quantity * self.item.deal_price

    def amount_saved(self):
        return int(self.get_total_item_price() - self.get_total_disc_price())

    def get_final_price(self):
        if self.item.discount:
            return self.get_total_disc_price()
        return self.get_total_item_price()


class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, blank=True,
                                        null=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL,
                                         blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for oi in self.items.all():
            total += oi.get_final_price()
        return total


class Payment(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.user.username
