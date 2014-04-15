from django.db import models
from django.contrib.auth.models import User
from django.http import *
from django.shortcuts import *

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

import json

from inTabasco_.apps.inTabasco.models import *

@csrf_exempt
def ajaxautocompletable(request):
	if request.is_ajax():
		# recuperamos el campo
		q = request.GET.get('term', '').lower()
		drugs = espacio.objects.filter( nombre__icontains = q, status__status = 'A').distinct('nombre')
		print(drugs)
		results = []
		for drug in drugs:
			drug_json = {}
			drug_json['label'] = drug.nombre
			results.append(drug_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

@csrf_exempt
def ajaxaubicacion(request):
	if request.is_ajax():
		# recuperamos el campo
		q = request.GET.get('term', '').lower()
		# cosultamos
		drugs = cat_localidad.objects.filter( nombre__icontains = q).distinct('nombre')
		results = []
		for drug in drugs:
			drug_json = {}
			drug_json['label'] = str(drug.nombre)
			results.append(drug_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

@csrf_exempt
def ajaxacategoria(request):
	if request.is_ajax():
		# recuperamos el campo
		q = request.GET.get('term', '').lower()
		# cosultamos
		drugs = cat_categorias_espacios.objects.filter( categoria__icontains = q).distinct()
		results = []
		for drug in drugs:
			drug_json = {}
			drug_json['label'] = str(drug.categoria)
			results.append(drug_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)

@csrf_exempt
def ajax_socio_vip(request):
	if request.is_ajax():
		# recuperamos el campo
		q = request.GET.get('term', '').lower()
		# cosultamos
		drugs = espacio.objects.filter( nombre__icontains = q, socio_vip = True, status__status = 'A').distinct('nombre')
		results = []
		for drug in drugs:
			drug_json = {}
			drug_json['label'] = str(drug.nombre)
			results.append(drug_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
