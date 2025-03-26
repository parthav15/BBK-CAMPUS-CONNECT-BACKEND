from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import CustomUser
from notice.models import Notice

from users.utils import jwt_decode, auth_user

@csrf_exempt
def get_all_notices(request):
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
        except Exception:
            return JsonResponse({'success': False, 'message': 'Invalid or expired token.'}, status=401)

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)

        user_campus = user.campus
        notices = Notice.objects.filter(campus=user_campus)

        notice_list = []
        for notice in notices:
            notice_data = {
                'id': notice.id,
                'title': notice.title,
                'slug': notice.slug,
                'description': notice.description,
                'posted_by': {
                    'id': notice.posted_by.id,
                    'email': notice.posted_by.email,
                    'first_name': notice.posted_by.first_name,
                    'last_name': notice.posted_by.last_name,
                    'phone': notice.posted_by.phone_number,
                },
                'campus': {
                    'id': notice.campus.id,
                    'name': notice.campus.name,
                    'address': notice.campus.address,
                    'city': notice.campus.city,
                    'state': notice.campus.state,
                    'country': notice.campus.country,
                    'website': notice.campus.website,
                    'head_name': notice.campus.head_name,
                    'head_phone': notice.campus.head_phone,
                    'head_email': notice.campus.head_email,
                    'image': str(notice.campus.image.url) if notice.campus.image else None,
                    'established_year': notice.campus.established_year,
                },
                'created_at': notice.created_at,
                'updated_at': notice.updated_at,
                'is_pinned': notice.is_pinned,
                'status': notice.status,
                'priority': notice.priority,
                'file_attachment': str(notice.file_attachment.url) if notice.file_attachment else None,
            }
            notice_list.append(notice_data)

        return JsonResponse({'success': True, 'message': 'Notices retrieved successfully.', 'notices': notice_list}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)

@csrf_exempt
def get_specific_notice(request):
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
        except Exception:
            return JsonResponse({'success': False, 'message': 'Invalid or expired token.'}, status=401)

        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'}, status=404)

        user_campus = user.campus
        slug = request.POST.get('slug')
        notice = Notice.objects.get(slug=slug)

        notice_data = {
            'id': notice.id,
            'title': notice.title,
            'slug': notice.slug,
            'description': notice.description,
            'posted_by': {
                'id': notice.posted_by.id,
                'email': notice.posted_by.email,
                'first_name': notice.posted_by.first_name,
                'last_name': notice.posted_by.last_name,
                'phone': notice.posted_by.phone_number,
            },
            'campus': {
                'id': notice.campus.id,
                'name': notice.campus.name,
                'address': notice.campus.address,
                'city': notice.campus.city,
                'state': notice.campus.state,
                'country': notice.campus.country,
                'website': notice.campus.website,
                'head_name': notice.campus.head_name,
                'head_phone': notice.campus.head_phone,
                'head_email': notice.campus.head_email,
                'image': str(notice.campus.image.url) if notice.campus.image else None,
                'established_year': notice.campus.established_year,
            },
            'created_at': notice.created_at,
            'updated_at': notice.updated_at,
            'is_pinned': notice.is_pinned,
            'status': notice.status,
            'priority': notice.priority,
            'file_attachment': str(notice.file_attachment.url) if notice.file_attachment else None,
        }

        return JsonResponse({'success': True, 'message': 'Notices retrieved successfully.', 'notices': notice_data}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'}, status=500)