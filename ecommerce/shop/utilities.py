import datetime
import itertools
import random
import secrets
import string
import hashlib

def create_payment_id(n=5, salt='nawoka'):
    """Create a payment token for Google enhanced ecommerce"""
    tokens = [secrets.token_hex(2) for _ in range(0, n)]
    # Append the salt that allows us to identify
    # if the payment method is a valid one
    tokens.append(hashlib.sha256(salt.encode('utf-8')).hexdigest())
    return '-'.join(tokens)

def validate_payment_id(token, salt='nawoka'):
    """Validate a payment ID"""
    parts = token.split('-')
    hashed_salt = hashlib.sha256(salt.encode('utf-8')).hexdigest()
    
    # The salt should always theoretically
    # be the last component of the array
    incoming_hashed_part = parts.pop(-1)

    truth_array = []

    # Compare incoming salt to salt
    if hashed_salt == incoming_hashed_part:
        truth_array.append(True)
    else:
        truth_array.append(False)

    # We should only have 5
    # parts in the array outside
    # of the salt
    if len(parts) == 5:
        truth_array.append(True)
    else:
        truth_array.append(False)
    
    # Each part should have a
    # maximum of 5 characters
    for part in parts:
        if len(part) != 4:
            truth_array.append(False)

    return all(truth_array)

def create_reference(n=5):
    """Create a basic reference: `NAW201906126011b0e0b8`
    """
    current_date = datetime.datetime.now().date()
    prefix = f'NAW{current_date.year}{current_date.month}{current_date.day}'
    return prefix + secrets.token_hex(n)

def create_product_reference():
    """Creates a product reference number: AC4565ZE4TEZD
    """
    # Create two first letters ex. AC
    capital_letters = string.ascii_uppercase
    first = ''.join(random.choice(capital_letters) for _ in range(0, 2))
    # Get a number between 1000 and 9000
    second = random.randrange(1000, 9000)
    # Add a salt that makes sure the reference
    # is unique in every ways
    salt = secrets.token_hex(4).upper()
    return f'{first}{second}{salt}'

def create_slug(name):
    names = name.split(' ')

    def normalize_names(raw_name):
        return raw_name.strip().lower()

    for name in names:
        names[names.index(name)] = normalize_names(name)

    return '-'.join(names)

def create_image_slug(name, reverse=False):
    """Create an image slug
    
    Example
    -------

        an_image_slug.jpg

    Parameters
    ----------

        reverse: from an image slug, guess the name of the image: an_image_slug 
        becomes in that case 'An image slug'
    """
    if reverse:
        if '_' in name:
            spaced_name = name.split('_')
            cleaned_name = [name.split('.') for name in spaced_name if '.' in name][0][0]
            spaced_name.pop(-1)
            spaced_name.append(cleaned_name)
            return ' '.join(spaced_name).capitalize()

    image_name = '_'.join(name.split(' '))
    return f'{image_name.strip().lower()}.jpg'
    
def transform_to_list(data):
    """Transform a dict to a list containing list
    of values: 
    
    Description
    -----------

        [{a: c}, {e: t}] becomes [[c], [t]].

        This is useful for the .add() method for m2m
        creation fields for an item
    """
    values = []
    for items in data:
        values.append(list(items.values()))
    
    return values

def full_address(address, zip_code, city):
    return f"{address}, {zip_code}, {city}"
    
def create_cart_id(n=12):
    """Creates an iD for the Anonymous cart so that we can
    easily get all the items registered by an anonymous user
    in the cart.

    This iD is saved in the session and in the local storage.

    Description
    -----------

        2019_01_02_token
    """
    token = secrets.token_hex(n)
    date = datetime.datetime.now().date()
    return f'{date.year}_{date.month}_{date.day}_' + token

def stripe_tax(price):
    """Calculates the percentage stripe takes
    on each given sale

    Formula
    -------

        price * (2.9% / 100) + 0.27c
    """
    return round(price * (2.9 / 100) + 0.27, 2)

def calculate_discount(price, pct):
    """Calculates a discount price

    Formula
    -------
        price * (1 - (pct / 100))
    """
    return round(float(price) * (1 - (pct / 100)), 2)

def calculate_tva(price, tva=20):
    """Calculates the tax on a product

    Formula
    -------
        price * (1 + (tax / 100))
    """
    return round(float(price) * (1 + (tva / 100)), 2)

def impressions_helper(queryset):
    """A helper function that helps create an impressions
    datalayer for a list of products
    """
    items = []
    position = 1
    try:
        for product in queryset:
            if product.discount_price > 0:
                price = product.discount_price
            else:
                price = product.price_ht

            items.append(
                {
                    'id': product.reference,
                    'name': product.name,
                    'price': price,
                    'brand': "Nawoka",
                    'category': product.collection.collection_name,
                    'position': position 
                }
            )
            position = position + 1
    except:
        return []
    return items

def add_to_current_date(d=15):
    """Return a possible delivery date in the future"""
    current_date = datetime.datetime.now().date()
    return current_date + datetime.timedelta(days=d)

def split_colors(colors):
    """Takes a comma separated list of colors and returns
    them into a list"""
    if "," in colors:
        return colors.split(",")
    return [colors]