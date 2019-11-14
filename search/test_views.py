from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, reverse
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from decimal import Decimal
from artifacts.models import Artifact, Category
from auctions.models import Auction
from .forms import SearchArtifactsForm

CATEGORY_LIST = [1,2,3]
TYPE_LIST = ["DATA", "MEDIA", "CULTURAL", "KNOWLEDGE"]

class TestViews(TestCase):  
    @classmethod
    def setUpTestData(cls):
        """create a user"""
        user = User.objects.create_user(username='TestName', email='test@…', password='test')
        """set the user option to remain anonymous"""
        user.profile.remain_anonymous = True
        user.save()

        """create artifacts"""
        number_of_categories = 3
        for category_id in range(number_of_categories):
            category = Category.objects.create(
                name = f'test category { category_id+1 }',
                description = f'test description { category_id+1 }'
            )

        Artifact.objects.create(
            name = f'Name { 1 }',
            description = f'Description { 1 }',
            type = "MEDIA",
            category = get_object_or_404(Category, pk=1), 
            buy_now_price = 1.00
        )            

        Artifact.objects.create(
            name = f'Name { 2 }',
            description = f'Description { 2 }',
            type = "MEDIA",
            category = get_object_or_404(Category, pk=2),
            buy_now_price = 5.00
        )      
        
        Artifact.objects.create(
            name = f'Name { 3 }',
            description = f'{ 3 }',
            type = "CULTURAL",
            category = get_object_or_404(Category, pk=3),
            sold = True,
            buy_now_price = 10.00
        )   
        
        """
        create auctions
        """
        auction = Auction.objects.create(
            artifact = get_object_or_404(Artifact, pk=1),
            name = f'Auction Name {1}',
            start_date = timezone.now() - timedelta(2),
            end_date = timezone.now() + timedelta(1),
        )
        
    """
    test search_artifacts
    """
    
    
    """
    check empty search fails due to lacking category and type
    """
    def test_empty_search_returns_error(self):
        response = self.client.post('/artifacts/list/', { }) 
        self.assertFormError(response, 'search_form', 'category', u'This field is required.')
        self.assertFormError(response, 'search_form', 'type', u'This field is required.')
        
    """
    check name search
    """
    def test_name_search(self):
        self.client.post('/artifacts/list/', { "name" : "Name 1", "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_results = []
        search_result = cache.get('sorted_list')
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1)])
        
    """
    check description search
    """
    def test_description_search(self):
        self.client.post('/artifacts/list/', { "description" : "description", "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2)])        

    """
    check sold search
    """
    def test_sold_search(self):
        self.client.post('/artifacts/list/', { "sold" : True, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=3)])        
    """
    check not sold search
    """
    def test_not_sold_search(self):
        self.client.post('/artifacts/list/', { "unsold" : True, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2)])   
    """
    check in auction search
    """
    def test_in_auction_search(self):
        self.client.post('/artifacts/list/', { "in_auction" : True, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1)])           
        
    """
    check not in auction search
    """
    def test_not_in_auction_search(self):
        self.client.post('/artifacts/list/', { "not_in_auction" : True, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=3)])                   

    """
    check category search
    """
    def test_category_search(self):
        self.client.post('/artifacts/list/', { "type" : TYPE_LIST, "category": 1}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1)])       
 
    """
    check type search
    """
    def test_type_search(self):
        self.client.post('/artifacts/list/', { "type" : ["DATA", "MEDIA", "KNOWLEDGE"], "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2)])    

    """
    check max price 
    """
    def test_max_price_search(self):
        self.client.post('/artifacts/list/', { "max_buy_now_price" : 5.00, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2)])

    """
    check min price 
    """
    def test_min_price_search(self):
        self.client.post('/artifacts/list/', { "min_buy_now_price" : 5.00, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=3)])                                   

    """
    check max and min price 
    """
    def test_min_and_max_price_search(self):
        self.client.post('/artifacts/list/', { "min_buy_now_price" : 2.00, "max_buy_now_price" : 7.00, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=2)])         

    """
    check error returned on max price < min price 
    """
    def test_min_gt_max_price_search(self):
        response = self.client.post('/artifacts/list/', { "min_buy_now_price" : 7.00, "max_buy_now_price" : 2.00, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        self.assertFormError(response, 'search_form', '__all__', u'Invalid price range. Maximum price must be more than minimum price.')


    """
    check zero min_price searches return no price filter 
    """
    def test_zero_min_price_search(self):
        self.client.post('/artifacts/list/', { "min_buy_now_price" : 0.00, "type"  : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=3)])                                   

    """
    check zero max_price searches return no price filter 
    """
    def test_zero_max_price_search(self):
        self.client.post('/artifacts/list/', { "max_buy_now_price" : 0.00, "type"  : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=3)])                                   

    """
    check sort by price ascending 
    """
    def test_sort_price_ascending(self):
        self.client.post('/artifacts/list/', { "sort_by": 1, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=3)])         

    """
    check sort by price descending 
    """
    def test_sort_price_descending(self):
        self.client.post('/artifacts/list/', { "sort_by": 2, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=3), get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=1)])         

    """
    check sort by name ascending 
    """
    def test_sort_name_ascending(self):
        self.client.post('/artifacts/list/', { "sort_by": 3, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=1), get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=3)])         

    """
    check sort by name descending 
    """
    def test_sort_name_descending(self):
        self.client.post('/artifacts/list/', { "sort_by": 4, "type" : TYPE_LIST, "category": CATEGORY_LIST}) 
        search_result = cache.get('sorted_list')
        search_results = []
        if search_result:
            for result in search_result:
                search_results.append(result)
        self.assertEqual(search_results, [get_object_or_404(Artifact, pk=3), get_object_or_404(Artifact, pk=2), get_object_or_404(Artifact, pk=1)])         

