import os
import sys
import math
import random
import itertools
import numpy as np 
import numpy.random

from faker import Faker
from statistics import mean
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zelthy_assignment.settings")

import django
if __name__ == "__main__":
    django.setup()

from purchase.models import Purchase, PurchaseStatus

def random_names_generator(length):
    '''
    Function to generate list of fake names using faker.
    '''
    fake = Faker()
    return [fake.name() for _ in range(length)]


def get_quantity_list(length):
    '''
    Function to generate a list of specified length whos average is 7.
    '''
    quantity_list = list()
    while True:
        quantity_list.append(random.randrange(1,10))
        if len(quantity_list) == length:
            break
        if len(quantity_list) > 1:
            if 10 > mean(quantity_list) >= 7:
                # Appending number less than 7 to decrease the average
                quantity_list.append(random.randrange(1,7))
            elif 0 < mean(quantity_list) < 7:
                # Appending number greater than 7 to increase the average
                quantity_list.append(random.randrange(8,10))
            if len(quantity_list) == length:
                break

    return quantity_list


def get_distr_list(names_list_len, quantity_len):
    '''
    Function to get list of indices by which qunatity list will spliced.
    '''
    # Returns a list of elements which add upto 1
    distr_list = np.random.dirichlet(np.ones(names_list_len),size=1)[0]

    distr_list = [round(x*5000) for x in distr_list]

    # Rounding can cause length to increase or decrease by 1
    if sum(distr_list) != quantity_len:
        diff = quantity_len - sum(distr_list)
        for i in range(diff):
            distr_list[i] += 1

    return distr_list


def get_random_date():
    '''
    Function to return random date from specified timespan.
    '''
    start_date = datetime(2019, 1, 1, 17, 0)
    end_date = datetime(2020, 3, 31, 22, 0)

    days_between_dates = (end_date - start_date).days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)

    # Changing naive timedate to timezone aware timedate 
    return make_aware(random_date)

def purchase_object_creator(names, quantity):
    '''
    Function to create Purchase and PurchaseStatus objects.
    '''
    # list of randomly selected lengths
    distr_list = get_distr_list(len(names), len(quantity))

    # Adding list elements to use as indices
    indexes = list(itertools.accumulate(distr_list))

    # Splicing the qunatity list into sublists based on indices
    individual_purchase_quantities = [quantity[i:j] for i, j in zip([0]+indexes, indexes+[None])]

    for i, name in enumerate(names):
        for quant in individual_purchase_quantities[i]:
            purchase_obj = Purchase.objects.create(purchaser_name=name, quantity=quant)
            print(purchase_obj)
            purchase_status_option = ['Open', 'Verified', 'Dispatched', 'Delivered']
            for j in range(random.randrange(1, len(purchase_status_option))):
                purchase_status_obj = PurchaseStatus.objects.create(purchase=purchase_obj, 
                                                                    status=purchase_status_option[j-1],
                                                                    created_at=get_random_date())
                print(purchase_status_obj)


def populate_purchase():
    # Generating 10 random names
    names_list = random_names_generator(length=10)

    # Generating order quanities
    quantity_list = get_quantity_list(length=5000)

    # Puchase and PurchaseStatus object creation
    purchase_object_creator(names_list, quantity_list)


populate_purchase()