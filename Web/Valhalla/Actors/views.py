
from django.shortcuts import render
from .models import HistoryVikings, Norsemen


def index(request):
    return render(request, 'actors/index.html')


def history_vikings_list(request):
    vikings = HistoryVikings.objects.order_by('id')
    return render(request, 'actors/history_vikings_list.html', {'vikings': vikings})


def norsemen_list(request):
    norsemen = Norsemen.objects.all()
    return render(request, 'actors/norsemen_list.html', {'norsemen': norsemen})


def actor_vikings(request, actor_id):
    actors = HistoryVikings.objects.get(id=actor_id)
    print(dir(actors))
    # if actors.image_bytes:
    #
    #     # image = Image.open(io.BytesIO(actors.image_bytes))
    #     # res = ''.join(format(i, '08b') for i in bytearray(actors.image_bytes, encoding='utf-8'))
    #     res = ''.join(format(ord(i), '08b') for i in actors.image_bytes)
    #     print(res)
    #     image_bytes = base64.b64decode(res)
    #     image = Image.open(BytesIO(image_bytes))
    # else:
    #     image = None
    context = {'actors': actors}
    return render(request, 'actors/actor_vikings.html', context)


def actor_norsemen(request, actor_id):
    actors = Norsemen.objects.get(id=actor_id)
    print(dir(actors))
    # if actors.image_bytes:
    #
    #     # image = Image.open(io.BytesIO(actors.image_bytes))
    #     # res = ''.join(format(i, '08b') for i in bytearray(actors.image_bytes, encoding='utf-8'))
    #     res = ''.join(format(ord(i), '08b') for i in actors.image_bytes)
    #     print(res)
    #     image_bytes = base64.b64decode(res)
    #     image = Image.open(BytesIO(image_bytes))
    # else:
    #     image = None
    context = {'actors': actors}
    return render(request, 'actors/actor_norsemen.html', context)
