import sys
from io import BytesIO
from PIL import Image as Pillow
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from image_size.settings import MEDIA_ROOT
from .models import Image, ChangedImage
from .forms import AddForm, ChangeForm


# контроллер стартовой страницы со списком всех загруженнных изображений
def index(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, 'image/index.html', context)


# контроллер страницы изменения размера изображения
def one_image(request, image_id):
    image = Image.objects.get(id=image_id)
    proportion = image.width / image.height
    if request.method != 'POST':
        form = ChangeForm()
    else:
        form = ChangeForm(request.POST)
        if form.is_valid():
            # получаем ширину и высоту из формы
            width = form['width'].value()
            height = form['height'].value()
            # сохраняем пропорции
            try:
                width, height = map(int, [width, height])
            except ValueError:
                if height:
                    width = proportion * int(height)
                    width, height = map(int, [width, height])
                elif width:
                    height = int(width) / proportion
                    width, height = map(int, [width, height])

            
            name = "pixel" + str(image)
            pixelSize = 40 
            im = Pillow.open('{}'.format(MEDIA_ROOT+'/'+str(image.file))) 
            pix = im.load()
            width = im.size[0]
            height = im.size[1]
            startX = 0
            startY = 0
            while (startX < width and startY < height):
                deltaX = width - startX if startX + pixelSize > width else pixelSize
                deltaY = height - startY if startY + pixelSize > height else pixelSize
                approxListSize = deltaX * deltaY
                allPixelsInQuadrant = []

                for x in range(startX, startX + deltaX):
                    for y in range(startY, startY + deltaY):
                        allPixelsInQuadrant.append(pix[x, y])

                approxPixels = [sum(x) for x in zip(*allPixelsInQuadrant)]
                approxPixels = [int(x / approxListSize) for x in approxPixels]

                for x in range(startX, startX + deltaX):
                    for y in range(startY, startY + deltaY):
                        pix[x, y] = tuple(approxPixels)

                startX += pixelSize

                if startX >= width:
                    startY = startY + pixelSize
                    startX = 0

            # меняем размер с помощью класса Image(as Pillow) from PIL
            out = im
            buffer = BytesIO()
            out.save(fp=buffer, format='JPEG')
            buffer.seek(0)
            new_pic = InMemoryUploadedFile(buffer, 'ImageField',
                                           name, 'image/jpeg',
                                           sys.getsizeof(buffer), None)

            # сохраняем изменное изображение
            image = ChangedImage.objects.create(file=new_pic)
    context = {'image': image, 'form': form}
    return render(request, 'image/image.html', context)


# контроллер добавления нового изображения
def new_image(request):
    if request.method != 'POST':
        form = AddForm()
    else:
        form = AddForm(request.POST, request.FILES)
        if form.is_valid():

            # проверяем какая форма была заполненна url или file
            img_url = form.cleaned_data.get('url')
            img_file = form.cleaned_data.get('file')

            if img_file:
                image = form.save()
                image_id = image.id
                return HttpResponseRedirect('../id/{}'.format(image_id))

            elif img_url:
                name = img_url.split('/')[-1]
                image_content = ContentFile(requests.get(img_url).content)
                new_pic = InMemoryUploadedFile(image_content, 'ImageField',
                                               name, 'image/jpeg',
                                               sys.getsizeof(image_content), None)
                image = Image.objects.create(file=new_pic)
                image_id = image.id
                return HttpResponseRedirect('../id/{}'.format(image_id))
    context = {'form': form}
    return render(request, 'image/new_image.html', context)


