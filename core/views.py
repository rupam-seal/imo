from django.shortcuts import render, redirect
import numpy as np
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
from keras.applications import vgg16
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array, load_img
from tensorflow.python.keras.backend import set_session

from .forms import ImageCreationForm
from .models import *

# Create your views here.
def home(request):
    # get all images from db
    images = Image.objects.all()
    # get all category from db
    categories = Category.objects.all()

    context = {
        'nav':'home',
        'images':images,
        'categories':categories
    }

    return render(request, 'home.html', context)

def upload(request):
    context = {
        'nav':'upload',
    }

    if request.method == "POST":
        # get multiple images from input
        image_list = request.FILES.getlist('images')
        for image in image_list:
            # Django image API
            file_name = default_storage.save(image.name, image)
            file_url = default_storage.path(file_name)

            # *Testing*
            # print("image name : "+image.name)

            # https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/load_img
            load_image = load_img(file_url, target_size=(224, 224))
            numpy_array = img_to_array(load_image)
            image_batch = np.expand_dims(numpy_array, axis=0)
            processed_image = vgg16.preprocess_input(image_batch.copy())

            # get the predicted probabilities
            with settings.GRAPH1.as_default():
                set_session(settings.SESS)
                predictions = settings.IMAGE_MODEL.predict(processed_image)

            # Output/Return data
            # get only one list [top=1]
            label = decode_predictions(predictions, top=1)
            # filter name from label list
            label_name = label[0][0][1]
            # replace '_' with spaces
            name = label_name.replace('_', ' ')

            # *Testing*
            # print("name : ", name)

            if Category.objects.filter(name=name).exists():
                i = Image.objects.create(
                    category=Category.objects.get(name=name),
                    name=name,
                    photo=image
                )
                i.save()
                # *Testing*
                # print("YES")
            else:
                cm = Category.objects.create(name=name)
                cm.save()
                i = Image.objects.create(
                    category=cm,
                    name=name,
                    photo=image
                )
                i.save()
                # *Testing*
                # print("NO")

    else:
        return render(request, "upload.html", context)

    return render(request, "upload.html", context)

def view(request, pk):
    images = Image.objects.filter(name=pk)
    title = pk

    context = {
        'nav':'home',
        'images':images,
        'title': title,
    }

    return render(request, 'view.html', context)