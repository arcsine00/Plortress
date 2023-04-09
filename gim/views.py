from django.shortcuts import render, redirect
from .models import Request
from gim.GIM import GIM
from .forms import RequestForm
from django.utils import timezone
from django.http import HttpResponse
import os

def request(req):
    req_list = Request.objects.order_by('-timestamp')
    context = {'req_list': req_list}
    return render(req, 'gim/req_list.html', context)

def detail(req, req_id):
    requ = Request.objects.get(id=req_id)
    context = {'req': requ}
    return render(req, 'gim/req_detail.html', context)

def req_write(req):
    if req.method == 'POST':
        form = RequestForm(req.POST)
        if form.is_valid():
            fn, err = GIM(req.POST['speech'], req.POST['bpm'], req.POST['beats'])
            ourreq = form.save(commit=False)
            ourreq.timestamp = timezone.now()
            ourreq.fname = fn.split('/')[-1]+err
            ourreq.save()
            return redirect('gim:detail', req_id=ourreq.id)
    else:
        form = RequestForm()
    context = {'form': form}
    return render(req, 'gim/req_form.html', context)