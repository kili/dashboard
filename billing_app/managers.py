from django.db import models


class StripeCustomerManager(models.Manager):

    def create_stripe_customer(self, name, is_default, 
                               keystone_id, stripe_customer_id):
        card = self.model(name=name, 
                          is_default=is_default, 
                          keystone_id=keystone_id,
                          stripe_customer_id=stripe_customer_id)
        import pdb;pdb.set_trace()
        #if user wants this as default, unset previous default card
        if bool(is_default):
            old_default = self.filter(keystone_id__exact=keystone_id, is_default=True)
            old_default.is_default = False
            old_default.save()
        card.save()
        return True
