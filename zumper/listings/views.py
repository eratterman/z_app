from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import Listing, Image
import json


class Get(View):
    def get(self, request, pk=None):
        if pk:
            listing = Listing.objects.get(pk=pk)
            data = {
                'id': listing.id,
                'address1': listing.address1,
                'address2': listing.address2,
                'apt_num': listing.apt_num,
                'city': listing.city,
                'state': listing.state,
                'zip_code': listing.zip_code,
                'sq_ft':  listing.sq_ft,
                'num_bedrooms': listing.num_bedrooms,
                'num_bathrooms': listing.num_bathrooms,
                'description': listing.description,
                'cost': listing.cost,
                'create_date': listing.create_date,
                'modified_date': listing.modified_date
            }
            images = Image.objects.filter(listing_id=listing.id).all()
            if images:
                data['images'] = list(images)

            return JsonResponse({'listings': data})

        listings = Listing.objects.values(
            'id',
            'address1',
            'address2',
            'apt_num',
            'city',
            'state',
            'zip_code',
            'sq_ft',
            'num_bedrooms',
            'num_bathrooms',
            'description',
            'cost'
        )
        out_list = []
        for i in listings:
            listid = i.get('id', '')
            print(listid)
            images = Image.objects.filter(listing_id=listid).all()
            print(images)
            if images:
                i['images'] = list(images)

            out_list.append(i)

        return JsonResponse({'listings': list(out_list)})


class Create(View):

    def post(self, request):
        # get fields from request.post data
        # print(request.POST)
        image_data = json.loads(request.POST.get('images', []))
        # print(image_data, type(image_data))

        # add listing and get object
        listing, added = Listing.objects.get_or_create(
            address1=request.POST.get('address1', ''),
            address2=request.POST.get('address2', ''),
            apt_num=request.POST.get('apt_num', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            zip_code=request.POST.get('zip_code', ''),
            sq_ft=request.POST.get('sq_ft', ''),
            num_bedrooms=request.POST.get('num_bedrooms', ''),
            num_bathrooms=request.POST.get('num_bathrooms', ''),
            description=request.POST.get('description', ''),
            cost=request.POST.get('cost', ''),
        )
        for data in image_data:
            image = Image(
                listing_id=listing,
                file_path=data.get('file_path', ''),
                description=data.get('description', ''),
            )
            image.save()

        return HttpResponse('Successfully added listing')


class Update(View):
    def post(self, request):
        # get fields from request.post data
        if 'images' in request.POST:
            image_data = json.loads(request.POST.get('images', []))
            xref = {i.get('id', ''): i for i in image_data}
        else:
            xref = {}

        # add listing and get object
        listing = Listing.objects.get(pk=request.POST.get('id', ''))
        listing.address1 = request.POST.get('address1', '')
        listing.address2 = request.POST.get('address2', '')
        listing.apt_num = request.POST.get('apt_num', '')
        listing.city = request.POST.get('city', '')
        listing.state = request.POST.get('state', '')
        listing.zip_code = request.POST.get('zip_code', '')
        listing.sq_ft = request.POST.get('sq_ft', '')
        listing.num_bedrooms = request.POST.get('num_bedrooms', '')
        listing.num_bathrooms = request.POST.get('num_bathrooms', '')
        listing.description = request.POST.get('description', '')
        listing.cost = request.POST.get('cost', '')
        listing.save()
        # print(listing)

        if xref:
            images = Image.objects.filter(listing_id=listing.id).all()
            for i in images:
                curr_id = i.id
                update_data = xref.get(curr_id, {})
                new_desc = update_data.get('description', '')
                new_file_path = update_data.get('file_path', '')
                if not (new_desc and new_file_path):
                    continue

                if i.description != new_desc:
                    i.description = update_data.get('description', '')

                if i.file_path != new_file_path:
                    i.file_path = update_data.get('file_path', '')

                if new_desc or new_file_path:
                    i.save()

        return HttpResponse('Successfully updated listing')


class Delete(View):
    def post(self, request):
        # check for id in request.post data
        if 'id' not in request.POST:
            return HttpResponse('Failed to delete data - id key was not found')

        listing_id = request.POST.get('id', '')

        # check for empty id
        if not listing_id:
            return HttpResponse('Failed to delete data - id value was empty')
        elif not listing_id.isdigit():
            return HttpResponse('Failed to delete data - id needs to be an integer')

        listing_id = int(listing_id)

        # delete data
        try:
            result = Listing.objects.get(pk=listing_id).delete()
        except Exception as e:
            if 'Listing matching query does not exist' in str(e):
                return HttpResponse(f'Listing ID: {listing_id} does not exist')

        return HttpResponse('Successfully deleted listing')
