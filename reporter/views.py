# Django build-in
from django import views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import Point
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
# Local Django
from reporter.forms import CreatePointsForm
from reporter.models import PlacePoints


class ListPoint(views.View):
    def get(self, request):
        user = request.user
        queryset = PlacePoints.objects.filter(status=True)
        form = CreatePointsForm()

        context = {
            'object_list': queryset,
            'form': form,
        }
        return render(request, 'reporter/map_point.html', context)

    @method_decorator(login_required)
    def post(self, request: HttpRequest):
        queryset = PlacePoints.objects.filter(status=True)

        form = CreatePointsForm(request.POST, request.FILES)
        if form.is_valid():
            latitude = float(form.cleaned_data['lat'])
            longitude = float(form.cleaned_data['lng'])
            print(latitude)
            # create a value for mode PointField
            point = Point(longitude, latitude)
            print(point)

            cd = form.cleaned_data
            user = request.user
            print(user)
            # save a marker
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


class EditPoint(LoginRequiredMixin, views.View):
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


class DeletePoint(LoginRequiredMixin, views.View):
    def get(self, request: HttpRequest, placeID):
        PlacePoints.objects.get(id=placeID).delete()
        return redirect('lists_points')
