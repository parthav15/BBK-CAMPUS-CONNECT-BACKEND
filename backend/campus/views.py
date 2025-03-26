from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.text import slugify

from campus.models import Campus, Incident
from users.models import CustomUser

from users.utils import jwt_decode, auth_user

import os
import json

@csrf_exempt
def get_all_campuses(request):
    try:
        if request.method != 'GET':
            return JsonResponse({'success': False, 'message': 'Invalid request method. Use GET.'}, status=405)
        
        campuses = Campus.objects.all()
        campus_list = []
        for campus in campuses:
            campus_dict = {
                'id': campus.id,
                'name': campus.name,
                'address': campus.address,
                'city': campus.city,
                'state': campus.state,
                'country': campus.country,
                'website': campus.website,
                'head_name': campus.head_name,
                'head_phone': campus.head_phone,
                'head_email': campus.head_email,
                'image': str(campus.image.url) if campus.image else None,
                'established_year': campus.established_year,
                'created_at': campus.created_at,
                'updated_at': campus.updated_at,
            }
            campus_list.append(campus_dict)
        return JsonResponse({'success': True, 'message': 'Campus List retrieved successfully.', 'campus_list': campus_list}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error retrieving campus list: {str(e)}'}, status=500)
    
@csrf_exempt
def create_incident(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method. Use POST.'}, status=405)
    
    try:
        bearer = request.headers.get('Authorization')
        if not bearer:
            return JsonResponse({'success': False, 'message': 'Authentication header is required.'}, status=401)

        token = bearer.split()[1]
        if not auth_user(token):
            return JsonResponse({'success': False, 'message': 'Invalid token data.'}, status=401)

        try:
            decoded_token = jwt_decode(token)
            user_email = decoded_token.get('email')
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Invalid or expired token.'}, status=401)

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
        
        data = request.POST
        title = data.get('title')
        description = data.get('description')
        incident_type = data.get('incident_type')
        location = data.get('location')
        media_files = request.FILES.getlist('media_files')

        try:
            user_campus = user.campus
            campus = Campus.objects.get(id=user_campus.id)
        except Campus.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Campus not found.'}, status=404)
        
        incident = Incident.objects.create(
            title=title,
            description=description,
            reported_by=user,
            campus=campus,
            incident_type=incident_type,
            location=location,
        )

        saved_media_files = []
        for media_file in media_files:
            file_extension = os.path.splitext(media_file.name)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                folder = 'incident_images'
            elif file_extension in ['.mp4', '.avi', '.mov', '.mkv']:
                folder = 'incident_videos'
            else:
                continue 

            file_name = f"{incident_type}_{slugify(incident.title)}_{incident.id}{file_extension}"
            file_path = os.path.join(folder, file_name)
            saved_path = default_storage.save(file_path, ContentFile(media_file.read()))
            saved_media_files.append(saved_path)

        incident.media_files = saved_media_files
        incident.save()

        incident_data = {
            'id': incident.id,
            'title': incident.title,
            'description': incident.description,
            'reported_by': {
                'id': incident.reported_by.id,
                'email': incident.reported_by.email,
                'first_name': incident.reported_by.first_name,
                'last_name': incident.reported_by.last_name,
                'phone': incident.reported_by.phone_number,
            },
            'campus': {
                'id': incident.campus.id,
                'name': incident.campus.name,
                'address': incident.campus.address,
                'city': incident.campus.city,
                'state': incident.campus.state,
                'country': incident.campus.country,
                'website': incident.campus.website,
                'head_name': incident.campus.head_name,
                'head_phone': incident.campus.head_phone,
                'head_email': incident.campus.head_email,
                'image': str(incident.campus.image.url) if incident.campus.image else None,
                'established_year': incident.campus.established_year,
            },
            'incident_type': incident.incident_type,
            'status': incident.status,
            'location': incident.location,
            'media_files': incident.media_files,
            'created_at': incident.created_at,
            'updated_at': incident.updated_at,
        }
        return JsonResponse({'success': True, 'message': 'Incident created successfully.', 'incident': incident_data}, status=201)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error creating incident: {str(e)}'}, status=500)

@csrf_exempt
def get_incidents(request):
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Invalid request method. Use GET.'}, status=405)
    
    try:
        bearer = request.headers.get('Authorization')
        if not bearer:
            return JsonResponse({'success': False, 'message': 'Authentication header is required.'}, status=401)

        token = bearer.split()[1]
        if not auth_user(token):
            return JsonResponse({'success': False, 'message': 'Invalid token data.'}, status=401)

        try:
            decoded_token = jwt_decode(token)
            user_email = decoded_token.get('email')
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Invalid or expired token.'}, status=401)

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
        
        user_campus = user.campus
        incidents = Incident.objects.filter(campus=user_campus).order_by('-created_at')
        incident_list = []
        for incident in incidents:
            incident_data = {
                'id': incident.id,
                'title': incident.title,
                'description': incident.description,
                'reported_by': {
                    'id': incident.reported_by.id,
                    'email': incident.reported_by.email,
                    'first_name': incident.reported_by.first_name,
                    'last_name': incident.reported_by.last_name,
                    'phone': incident.reported_by.phone_number,
                },
                'campus': {
                    'id': incident.campus.id,
                    'name': incident.campus.name,
                    'address': incident.campus.address,
                    'city': incident.campus.city,
                    'state': incident.campus.state,
                    'country': incident.campus.country,
                    'website': incident.campus.website,
                    'head_name': incident.campus.head_name,
                    'head_phone': incident.campus.head_phone,
                    'head_email': incident.campus.head_email,
                    'image': str(incident.campus.image.url) if incident.campus.image else None,
                    'established_year': incident.campus.established_year,
                },
                'incident_type': incident.incident_type,
                'status': incident.status,
                'location': incident.location,
                'media_files': incident.media_files,
                'created_at': incident.created_at,
                'updated_at': incident.updated_at,
            }
            incident_list.append(incident_data)
        return JsonResponse({'success': True, 'message': 'Incident List retrieved successfully.', 'incident_list': incident_list}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error retrieving incident list: {str(e)}'}, status=500)
    
@csrf_exempt
def get_specific_incident(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method. Use POST.'}, status=405)
    
    try:
        bearer = request.headers.get('Authorization')
        if not bearer:
            return JsonResponse({'success': False, 'message': 'Authentication header is required.'}, status=401)

        token = bearer.split()[1]
        if not auth_user(token):
            return JsonResponse({'success': False, 'message': 'Invalid token data.'}, status=401)

        try:
            decoded_token = jwt_decode(token)
            user_email = decoded_token.get('email')
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'Invalid or expired token.'}, status=401)

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)
        
        user_campus = user.campus
        incident_id = request.POST.get('incident_id')
        incident = Incident.objects.get(id=incident_id, campus=user_campus)
        incident_data = {
            'id': incident.id,
            'title': incident.title,
            'description': incident.description,
            'reported_by': {
                'id': incident.reported_by.id,
                'email': incident.reported_by.email,
                'first_name': incident.reported_by.first_name,
                'last_name': incident.reported_by.last_name,
                'phone': incident.reported_by.phone_number,
            },
            'campus': {
                'id': incident.campus.id,
                'name': incident.campus.name,
                'address': incident.campus.address,
                'city': incident.campus.city,
                'state': incident.campus.state,
                'country': incident.campus.country,
                'website': incident.campus.website,
                'head_name': incident.campus.head_name,
                'head_phone': incident.campus.head_phone,
                'head_email': incident.campus.head_email,
                'image': str(incident.campus.image.url) if incident.campus.image else None,
                'established_year': incident.campus.established_year,
            },
            'incident_type': incident.incident_type,
            'status': incident.status,
            'location': incident.location,
            'media_files': incident.media_files,
            'created_at': incident.created_at,
            'updated_at': incident.updated_at,
        }
        return JsonResponse({'success': True, 'message': 'Incident retrieved successfully.', 'incident_list': incident_data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error retrieving incident list: {str(e)}'}, status=500)