from django import forms
from django.contrib.auth.models import User
from .models import (Customer, OrderItem, Order, Address, Payment, Product_Detail, Shoes_Size, Shoes, Clothes,
                     Clothes_Size, Watches, Laptop, Mobile)

Gender = [('K', 'Kids'), ('M', 'Male',), ('F', 'Female'), ('U', "Unisex")]
Type_shoes = [('R', 'Running'), ('Sp', 'Sports'), ('Sn', 'Sneakers'), ('Fo', 'Formal'), ('L', "Loafer")]
Type_shoes.sort()
Shoes_Brand = [('A', "Adidas"), ('P', "Puma"), ('N', "Nike"),
               ('L', "Lotto"), ("R", "Reebok"), ('NB', "New Balance"),
               ('AS', "Asics"), ('F', "Fila")]
Shoes_Brand.sort()


class Count(forms.Form):
    count = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Qauntity of size available"}),
                               required=True)


class Product_Form(forms.Form):
    image0 = forms.ImageField()
    image1 = forms.ImageField()
    image2 = forms.ImageField()
    product_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "Product Name"}), required=True)
    product_price = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                     "placeholder": "Product Price"
                                                                     }), required=True)
    product_color = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                  "placeholder": "Product Colour"
                                                                  }), required=True)
    product_details = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                    "placeholder": "Product Details"
                                                                    }), required=True)
    product_discount = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                     "placeholder": "Product Discount in Percentage"
                                                                     }), required=True)


class Shoes_detail(forms.Form):
    product_gender = forms.CharField(required=True,
                                     widget=forms.Select(choices=Gender, attrs={"class": "form-control"}))
    shoe_brand = forms.CharField(required=True,
                                 widget=forms.Select(choices=Shoes_Brand, attrs={"class": "form-control"}))
    shoe_type = forms.CharField(required=True,
                                widget=forms.Select(choices=Type_shoes, attrs={"class": "form-control"}))
    size = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Available sizes for product"
                                                         }), required=True)
    count = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Product Qauntity For each Size"
                                                             }), required=True)


Laptop_Brand = [('A', "Asus"), ('AC', "Acer"), ('AP', "Apple"), ('D', "Dell"), ('H', "HP"), ('L', "Lenovo"),
                ('S', "Sony")]
Laptop_Brand.sort()
Storage_Type = [('S', "SDD"), ('H', "HDD")]
Storage_Type.sort()


class Laptop_Form(forms.Form):
    count = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Product Qauntity"
                                                             }), required=True)
    model_year = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                  "placeholder": "Model Year"
                                                                  }), required=True)
    model_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "Model Name"
                                                               }), required=True)
    laptop_brand = forms.CharField(widget=forms.Select(choices=Laptop_Brand, attrs={"class": "form-control",
                                                                                    }), required=True)
    screen_size = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                "placeholder": "Screen Size in Inches"
                                                                }), required=True)
    screen_type = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                "placeholder": "Screen Type"
                                                                }), required=True)
    weight = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control",
                                                            "placeholder": "Weight In Kg(ex:1.20)"
                                                            }), required=True)
    processor_brand = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                    "placeholder": "Processor Brand"
                                                                    }), required=True)
    processor_speed = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                    "placeholder": "Processor Speed"
                                                                    }), required=True)
    processor_type = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                   "placeholder": "Processor Type"
                                                                   }), required=True)
    resolution = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "Resolution"
                                                               }), required=True)
    ram = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                        "placeholder": "Ram Size In GB or TB (mention GB or TB Required)"
                                                        }), required=True)
    storage_type = forms.CharField(widget=forms.Select(choices=Storage_Type, attrs={"class": "form-control",
                                                                                    }), required=True)
    storage_size = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "Storage Size In GB or TB (mention GB or TB Required)"
                                                                 }), required=True)

    hard_drive_interface = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                         "placeholder": "Hard Drive Interface"
                                                                         }), required=True)

    hard_drive_rotation_speed = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                              "placeholder": "Hard Drive Rotation Speed"
                                                                              }), required=True)
    operating_system = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                     "placeholder": "Operating System"
                                                                     }), required=True)
    graphics_card_details = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                          "placeholder": "Graphics Card Details"
                                                                          }), required=True)
    graphics_card_ram_type = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                           "placeholder": "Graphics Card Ram Type"
                                                                           }), required=True)
    graphics_card_interface = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                            "placeholder": "Graphics Card Interface"
                                                                            }), required=True)
    graphics_coprocessor = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                         "placeholder": "Graphics Card Processor"
                                                                         }), required=True)
    battery_details = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                    "placeholder": "battery_details"
                                                                    }), required=True)
    max_memory_supported = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                         "placeholder": "Max Extensible Memory"
                                                                         }), required=True)
    usb_ports = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "Number Of USB PORT"
                                                                 }), required=True)
    optical_drive_type = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                       "placeholder": "Optical Drive Type IF any else NA"
                                                                       }), required=True)
    hardware_interface = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                       "placeholder": "Hardware Interface"
                                                                       }), required=True)
    manufacturer = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "Manufacturer"
                                                                 }), required=True)
    connector_type = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                   "placeholder": "Connector Type"
                                                                   }), required=True)
    power_source = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control",
                                                                 "placeholder": "Power Source"
                                                                 }), required=True)


class Clothes_Form(forms.Form):
    pass


class Watch_Form(forms.Form):
    pass


class Mobile_Form(forms.Form):
    pass
