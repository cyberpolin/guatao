from django.db import models
from django.contrib.auth.models import User
from django.http import *
from django.shortcuts import *

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

import json

from inTabasco_.apps.inTabasco.models import *

@csrf_exempt
def ajaxautocompletable(request):
	if request.is_ajax():
		# recuperamos el campo
		q = request.GET.get('term', '').lower()
		drugs = espacio.objects.filter( (Q(nombre__icontains = q ) | Q(descripcion_corta__icontains = q )), status__status = 'A').distinct('nombre')
		print(drugs)
		results = []
		for drug in drugs:
			drug_json = {}
			drug_json['label'] = drug.descripcion_corta
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

@csrf_exempt
def ajax_busqueda_personas(request):
	if request.is_ajax():
		print("hola")
		# recuperamos el campo
		q = request.GET.get('term', '').lower()

		drugs = cat_persona.objects.distinct('nombre','apellido_paterno','apellido_materno').extra(where=[" LOWER((trim(nombre) || ' ' || trim(apellido_paterno) || ' ' || trim(apellido_materno))) like %s "], params=['%'+q+'%'])
		results = []
		for drug in drugs:
			drug_json = {}
			drug_json['id'] = drug.id
			drug_json['label'] = drug.nombre+' '+drug.apellido_paterno+' '+drug.apellido_materno
			drug_json['value'] = drug.nombre+' '+drug.apellido_paterno+' '+drug.apellido_materno
			results.append(drug_json)
		data = json.dumps(results)
	else:
		data = 'fail'
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
