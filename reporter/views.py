from django import views
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView

from reporter.forms import CreatePointsForm
from reporter.models import PlacePoints

longitude = -80.191788

latitude = 25.761681

my_location = Point(longitude, latitude, srid=4326)  # default location we will use gps geolocation in future totorials.


# Create your views here.


class ListPoints(ListView):
    queryset = PlacePoints.objects.filter(location__isnull=False)
    template_name = 'reporter/map_point.html'
    model = PlacePoints


class LIstPoint(views.View):
    def get(self, request):
        queryset = PlacePoints.objects.filter(location__isnull=False)
        form = CreatePointsForm()

        context = {
            'object_list': queryset,
            'form': form,
        }
        return render(request, 'reporter/map_point.html', context)

    def post(self, request: HttpRequest):
        queryset = PlacePoints.objects.filter(location__isnull=False)

        form = CreatePointsForm(request.POST, request.FILES)
        # print(form)
        if form.is_valid():
            # marker = form.save()
            latitude = float(form.cleaned_data['lat'])
            longitude = float(form.cleaned_data['lng'])
            print("__________________________________________________")
            print(latitude)
            point = Point(longitude, latitude)
            print(point)

            cd = form.cleaned_data
            user = request.user
            print(user)
            mark = PlacePoints.objects.create(
                user=user,
                description=cd['description'],
                picture=cd.get('picture'),
                location=point

            )
            return redirect('lists_points')

        context = {
            'object_list': queryset,
            'form': form,
        }
        messages.error(request, "wrong")
        return render(request, 'reporter/map_point.html', context)


class MyPoint(views.View):
    def get(self, request):
        queryset = PlacePoints.objects.filter(user_id=request.user.id)
        context = {
            'object_list': queryset,
        }
        return render(request, 'reporter/my_points.html', context)


# class EditPoint(views.View):
#     form_class = CreatePointsForm
#
#     def get(self, request, placeID):
#         points = PlacePoints.objects.get(id=placeID)
#         form = self.form_class(instance=points)
#
#         context = {
#             'points': points,
#             'form': form
#         }
#         return render(request, 'reporter/edit_points.html', context)
#
#     def post(self, request: HttpRequest, placeID):
#         points = PlacePoints.objects.get(id=placeID)
#         form = self.form_class(request.POST, request.FILES, instance=points)
#         context = {
#             'points': points,
#             'form': form
#         }
#         print("_____________________________________________________________________________________")
#
#         print(form)
#         print("_____________________________________________________________________________________")
#
#         if form.is_valid():
#             latitude = form.cleaned_data['lat']
#             longitude = form.cleaned_data['lng']
#             print("_____________________________________________________________________________________")
#             point = Point(longitude, latitude)
#
#             cd = form.cleaned_data
#             points.location = point
#             points.picture = cd.get('picture')
#             points.description = cd.get('description')
#             points.save()
#
#             messages.success(request, 'Successfully', 'success')
#             return redirect('lists_points')
#
#         messages.error(request, 'some thing is wrong ', 'danger')
#         return render(request, 'reporter/edit_points.html', context)


class EditPoint(views.View):
    form_class = CreatePointsForm

    def get(self, request, placeID):
        points = PlacePoints.objects.get(id=placeID)
        form = self.form_class(instance=points)

        context = {
            'points': points,
            'form': form
        }
        return render(request, 'reporter/edit_points.html', context)

    def post(self, request: HttpRequest, placeID):
        points = PlacePoints.objects.get(id=placeID)
        form = self.form_class(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            # Extract latitude and longitude from form data
            latitude = float(form.cleaned_data['lat'])
            longitude = float(form.cleaned_data['lng'])
            point = Point(longitude, latitude)

            # Update the point and other fields
            points.location = point
            points.picture = form.cleaned_data['picture']
            points.description = form.cleaned_data['description']
            points.save()

            messages.success(request, 'Successfully updated.', 'success')
            return redirect('lists_points')
        else:
            print(form.errors)
        messages.error(request, 'Something went wrong.', 'danger')
        context = {
            'points': points,
            'form': form
        }
        return render(request, 'reporter/edit_points.html', context)


class DeletePoint(views.View):
    def get(self, request: HttpRequest, placeID):
        PlacePoints.objects.get(id=placeID).delete()
        return redirect('lists_points')
