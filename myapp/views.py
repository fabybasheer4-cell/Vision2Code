import base64
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.contrib.auth.models import Group,User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime


# Create your views here.
from myapp.models import *

uu=User.objects.get(username="abcd@gmail.com")
uu.set_password("user1234")
uu.save()




def home_new_index(request):
    return render(request,"adminindex.html")

def landing_index(request):
    return render(request,'landing_index.html')

def login_get(request):
    # return render(request, 'login.html')
    return render(request,'login_index.html')
def login_post(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        if user.groups.filter(name='Admin').exists():
            messages.success(request, 'Login successful.')
            return redirect('/myapp/home_new_index/')
        else:
            # messages.error(request, 'Access denied: Not an admin user.')
            # return redirect('/myapp/landing_index/')
            return HttpResponse('''<script>alert('Access denied: Not an admin user');window.location="/myapp/landing_index/"</script>''')
    else:
        # messages.error(request, 'Invalid username or password.')
        # return redirect('/myapp/landing_index/')
        return HttpResponse('''<script>alert('Invalid username or password.');window.location="/myapp/landing_index/"</script>''')


def change_password_get(request):
    return render(request,"change_password.html")

def change_password_post(request):
    Current_Password = request.POST['textfield']
    New_Password = request.POST['textfield2']
    Confirm_Password = request.POST['textfield3']

    if check_password(Current_Password, request.user.password):
        if New_Password == Confirm_Password:
            user = request.user
            user.set_password(New_Password)
            user.save()
            logout(request)
            messages.success(request, 'Password changed successfully.')
            return redirect('/myapp/landing_index/')
        else:
            messages.error(request, 'New and Confirm password do not match.')
            return redirect('/myapp/change_password_get/')
    else:
        messages.error(request, 'Current password is incorrect.')
        return redirect('/myapp/change_password_get/')



##### forgotten passoword
def and_forget_password(request):
    return render(request, 'forgottenpassword.html')

def and_forget_password_post(request):
    if request.method == 'POST':
        email = request.POST.get('textfield', '').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request,'Email doest not exists')
            return redirect('/myapp/login_get/')
        psw = random.randint(1000, 9999)

        user.set_password(str(psw))
        user.save()

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("trainingstarted@gmail.com", "nlxasujxgazlbmgz")  # App Password

            subject = "Password Reset - Construction App"
            body = "Your new password is: " + str(psw)
            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail("trainingstarted@gmail.com", email, msg)
            server.quit()

            messages.success(request,'Password Send successfully')
            return redirect('/myapp/login_get/')

        except Exception as e:
            messages.warning(request, 'Failed to send')
            return redirect('/myapp/login_get/')

    messages.warning(request,'Failed to send')
    return redirect('/myapp/login_get/')


def logout_get(request):
    logout(request)
    messages.success(request,'Logout successfully')
    return redirect('/myapp/landing_index/')
    # return HttpResponse('<script>alert(" Logout  successfully");window.location="/myapp/login_get/"</script>')


###### ADMIN ######
def admin_home_get(request):
    return render(request,'Admin_index.html')

# def admin_view_customer_get(request):
#     d=Customer.objects.all()
#     return render(request,'view_users.html',{'data':d})


def admin_view_customer_get(request):
    # Session Reporting
    print("\n" + "=" * 80)
    print("📊 ADMIN CUSTOMER VIEW - SESSION REPORT")
    print("=" * 80)
    print(f"📍 Session Key: {request.session.session_key}")
    print(f"👤 User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
    print(f"🔐 Authenticated: {request.user.is_authenticated}")

    # Print all session data
    print("\n📦 SESSION DATA:")
    if request.session.items():
        for key, value in request.session.items():
            print(f"  • {key}: {value}")
    else:
        print("  • No session data available")

    # Get customer data
    d = Customer.objects.all()

    # Print report statistics
    print(f"\n📊 REPORT STATISTICS:")
    print(f"  • Total Customers: {d.count()}")
    print(f"  • Male: {d.filter(gender='Male').count() if hasattr(Customer, 'gender') else 'N/A'}")
    print(f"  • Female: {d.filter(gender='Female').count() if hasattr(Customer, 'gender') else 'N/A'}")

    from datetime import datetime
    print(f"  • Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80 + "\n")

    male_users=d.filter(gender='Male').count() if hasattr(Customer, 'gender') else 'N/A'
    female_users=d.filter(gender='Female').count() if hasattr(Customer, 'gender') else 'N/A'

    # Store report info in session
    request.session['last_customer_report'] = {
        'timestamp': str(datetime.now()),
        'total_customers': d.count(),
        'user': request.user.username if request.user.is_authenticated else 'anonymous'
    }

    return render(request, 'view_users.html', {
        'data': d,
        'session_data': dict(request.session),  # Pass session to template
        'total_customers': d.count(),
        'report_time': datetime.now(),
        "male":male_users,
        "female":female_users
    })






def admin_view_customer_post(request):
    search=request.POST['textfield']
    d=User.objects.filter(name__icontains=search)
    return render(request,'',{'data':d})

def admin_view_review_get(request):
    d=Feedback.objects.all()
    return render(request,'view_feedback.html',{'data':d})
def admin_view_review_post(request):
    time_from=request.POST['textfield']
    time_to=request.POST['textfield2']
    d=Feedback.objects.filter(date__range=[time_from,time_to])
    return render(request,'view_feedback.html',{'data':d})

def admin_view_history_get(request):
    d=History.objects.all()
    return render(request,'view_users_history.html',{'data':d})

def admin_view_history_post(request):
    time_from=request.POST['textfield']
    time_to=request.POST['textfield2']
    d=History.objects.filter(date__range=[time_from,time_to])
    return render(request,'view_users_history.html',{'data':d})




#### User Android

def android_login_post(request):
    user_name=request.POST['username']
    pass_word=request.POST['password']

    user = authenticate(request,username=user_name,password=pass_word)

    if user is not None:
        login(request, user)
        if user.groups.filter(name='Customer').exists():
            return JsonResponse({'status': 'ok','type':'Customer','lid':str(user.id)})

        # elif user.groups.filter(name='Children').exists():
        #     return JsonResponse({'status': 'ok','type':'Children','lid':str(user.id)})
        else:
            return JsonResponse({'status': 'invalid'})
    else:
        return JsonResponse({'status': 'invalid'})




def android_forget_password_post(request):
    email = request.POST.get('email')
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'})

    try:
        user = User.objects.get(username=email)
        print(email)

        # Generate new password
        new_pass = str(random.randint(1000, 9999))
        user.password = make_password(new_pass)
        user.save()

        # Email configuration
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "trainingstarted@gmail.com"
        app_password = "nlxasujxgazlbmgz"

        subject = "Your New Password"
        body = f"Your new password is: {new_pass}"
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(message)
        server.quit()

        return JsonResponse({'status': 'ok', 'message': 'Password sent to your email'})

    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Email not found'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Email send error: {str(e)}'})


def android_user_register(request):

    print("Incoming data:", request.POST)
    name = request.POST['name']
    mobile = request.POST['mobile']
    email = request.POST['email']
    place = request.POST['place']
    pin = request.POST['pin']
    district = request.POST['district']
    dob = request.POST['dob']
    gender = request.POST['gender']
    photo = request.POST['photo']
    password = request.POST['password']

    if User.objects.filter(username=email).exists():
        return JsonResponse({'status': 'exists'})

    user = User.objects.create(username=email, password=make_password(password))
    user.groups.add(Group.objects.get(name='Customer'))
    user.save()

    # Save image
    date2 = datetime.now().strftime('%Y%m%d-%H%M%S')
    image_data = base64.b64decode(photo)
    image_folder = r"C:\visiontocode\media"
    os.makedirs(image_folder, exist_ok=True)
    file_path = os.path.join(image_folder, f"{date2}.jpg")
    with open(file_path, "wb") as f:
        f.write(image_data)
    db_path = f"/media/{date2}.jpg"

    # Save parent record
    customer = Customer(
        name=name,
        email=email,
        phone=mobile,
        place=place,
        pin=pin,
        district=district,
        gender=gender,
        dob=dob,
        photo=db_path,
        USER=user
    )
    customer.save()

    print("User saved successfully.")
    return JsonResponse({'status': 'ok'})



def android_user_view_profile_post(request):
    lid=request.POST['lid']
    d=Customer.objects.get(USER=lid)
    photo_path = d.photo
    if not photo_path.startswith("/media/"):
        photo_path = "/media/" + photo_path

    # Full URL
    photo_url = f"{request.scheme}://{request.get_host()}{photo_path}"
    return JsonResponse({'status':'ok',
                         'name':d.name,
                         'email':d.email,
                         'phone':d.phone,
                         'pin':d.pin,
                         'district':d.district,
                         'place':d.place,
                         'gender':d.gender,
                         'dob':str(d.dob),
                         'photo':photo_url
                         })


def android_user_edit_profile_get(request):
    lid=request.POST['lid']

    d = Customer.objects.get(USER_id=lid)
    return JsonResponse({
        'status': 'ok',
        'name': d.name,
        'email': d.email,
        'phone': d.phone,
        'pin': d.pin,
        'district': d.district,
        'place': d.place,
        'dob': d.dob,
        'gender': d.gender,
        'photo': d.photo
    })


def android_user_edit_profile(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    place = request.POST['place']
    pin = request.POST['pin']
    district = request.POST['district']
    gender = request.POST['gender']
    dob = request.POST['dob']
    lid = request.POST['lid']

    d = Customer.objects.get(USER_id=lid)

    photo = request.POST['photo']
    date2 = datetime.now().strftime('%Y%m%d-%H%M%S')
    a = base64.b64decode(photo)
    image_folder = r"C:\visiontocode\media"
    os.makedirs(image_folder, exist_ok=True)
    path = f"/media/{date2}.jpg"
    file_path = os.path.join(image_folder, f"{date2}.jpg")
    with open(file_path, "wb") as f:
        f.write(a)
    d.photo = path
    d.save()

    d.name = name
    d.email = email
    d.phone = phone
    d.pin=pin
    d.district=district
    d.place = place
    d.gender = gender
    d.dob = dob
    d.save()
    return JsonResponse({'status': 'ok'})



def user_changepassword_post(request):
    id = request.POST['id']
    currentpassword = request.POST['currentpassword']
    print(currentpassword)
    newpassword = request.POST['newpassword']
    print(newpassword)
    confirmpassword = request.POST['confirmpassword']
    print(confirmpassword)

    try:
        user =  User.objects.get(id=id)

        obj = Customer.objects.get(USER_id=id)
        if user.check_password(currentpassword):
            if newpassword == confirmpassword:
                obj.password = newpassword
                user.set_password(newpassword)
                user.save()
                obj.save()

                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'data': 'not'})
        else:
            return JsonResponse({'status': 'no'})
    except Customer.DoesNotExist:
        return JsonResponse({'status': 'error'})


def android_user_send_feedback(request):
    lid=request.POST['lid']
    feedback=request.POST['issuetype']

    d=Feedback()
    d.feedback=feedback
    d.date=datetime.now().today()
    d.CUSTOMER_id=Customer.objects.get(USER_id=lid).id
    d.save()
    return  JsonResponse({'status':'ok'})




# import google.generativeai as genai
# from PIL import Image
#
# def android_upload_image(request):
#
#     photo = request.POST['photo']
#     title = request.POST['title']
#     file_type = request.POST['type']   # "html" or "python"
#     lid = request.POST['lid']
#
#     # ====== Save Uploaded Image ======
#     date2 = datetime.now().strftime('%Y%m%d-%H%M%S')
#     image_folder = "C:/Users/user/PycharmProjects/visiontocode/media/image"
#     os.makedirs(image_folder, exist_ok=True)
#
#     file_path = os.path.join(image_folder, f"{date2}.jpg")
#     with open(file_path, "wb") as f:
#         f.write(base64.b64decode(photo))
#
#     db_image_path = f"/media/image/{date2}.jpg"   # For DB
#
#     # ===== Gemini API Config =====
#     genai.configure(api_key="AIzaSyAqTwYwseX8CHyMhlFizAhmPXWY-sX6S4A")
#
#     # Load image correctly (use local file path, not db path)
#     img = Image.open(file_path)
#
#     print("Image saved")
#
#     # ===== Generate Code Based on Type =====
#     code_output_folder = "C:/Users/user/PycharmProjects/visiontocode/media/code"
#     os.makedirs(code_output_folder, exist_ok=True)
#     print("Code created")
#
#     if file_type.lower() == "html":
#         print("HTMLL")
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = (
#             "This is a drawing of a form UI. Generate a complete standalone HTML page "
#             "with full structure: <!DOCTYPE html>, <html>, <head>, <title>, <style>, and <body>. "
#             "Use clean internal CSS. Do not include explanations or Markdown formatting."
#         )
#         response = model.generate_content([img, prompt])
#         html_code = response.text.strip()
#
#         if html_code.startswith("```"):
#             html_code = html_code.replace("```html", "").replace("```", "").strip()
#
#         code_filename = f"{date2}.html"
#         code_path = os.path.join(code_output_folder, code_filename)
#         with open(code_path, "w", encoding="utf-8") as f:
#             f.write(html_code)
#
#
#
#     elif file_type.lower() == "python":
#
#         print("PYTHON")
#
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         prompt = (
#             "This is a hand-drawn form UI. Generate complete Python Tkinter code "
#             "to build this GUI. Include appropriate labels, entry fields, and buttons. "
#             "Use clean layout with grid or pack. Return only the code without any explanation."
#         )
#         response = model.generate_content([img, prompt])
#         tkinter_code = response.text.strip()
#
#         if tkinter_code.startswith("```"):
#             tkinter_code = tkinter_code.split("```")[1] if "```" in tkinter_code else tkinter_code
#             tkinter_code = tkinter_code.strip()
#
#         code_filename = f"{date2}.py"
#         code_path = os.path.join(code_output_folder, code_filename)
#         with open(code_path, "w", encoding="utf-8") as f:
#             f.write(tkinter_code)
#
#
#     elif file_type.lower() == "flutter":
#
#         print("FLUTTER")
#
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         prompt = (
#             "This is a hand-drawn mobile app UI. Generate complete Flutter code "
#             "for a single page (StatelessWidget or StatefulWidget as appropriate). "
#             "Use Material Design widgets like Scaffold, AppBar, Column, Row, Text, "
#             "TextField, ElevatedButton, etc. Ensure proper alignment, spacing, and padding. "
#             "Include a complete main() function with runApp() so the code is runnable directly. "
#             "Return only the Flutter Dart code without any explanation."
#         )
#         response = model.generate_content([img, prompt])
#         flutter_code = response.text.strip()
#
#         if flutter_code.startswith("```"):
#             flutter_code = flutter_code.split("```")[1] if "```" in flutter_code else flutter_code
#             flutter_code = flutter_code.strip()
#
#         code_filename = f"{date2}.dart"
#         code_path = os.path.join(code_output_folder, code_filename)
#         with open(code_path, "w", encoding="utf-8") as f:
#             f.write(flutter_code)
#
#     else:
#         print("Error")
#         return JsonResponse({"status": "error", "message": "Invalid file type"})
#
#     # DB path for code
#     db_file_path = f"/media/code/{code_filename}"
#
#     print("Code Saved")
#
#     # ====== Save DB Record ======
#     d = History(
#         date=datetime.now().today(),
#         image=db_image_path,
#         title=title,
#         type=file_type,
#         code_file=db_file_path,
#         CUSTOMER_id=Customer.objects.get(USER_id=lid).id
#     )
#     d.save()
#
#     # return JsonResponse({'status': 'ok', 'file': db_file_path})
#     full_url = f"{request.scheme}://{request.get_host()}{db_file_path}"
#     return JsonResponse({'status': 'ok', 'file_url': full_url})
#
#


def android_user_view_history_post(request):
    lid=request.POST['lid']
    data=History.objects.filter(CUSTOMER__USER_id=lid)
    l = []
    for i in data:
        l.append({
            'id': i.id,
            'title': i.title,
            'name': i.CUSTOMER.name,
            'date': i.date,
            'image': i.image,
            'code': i.code_file,
            'type': i.type,
        })
        print(l)
    return JsonResponse({'status': 'ok', 'data': l})






import google.generativeai as genai
from PIL import Image
from django.conf import settings
import base64, os
from datetime import datetime
from django.http import JsonResponse
from .models import Customer, History

#
# def android_upload_image(request):
#
#     photo = request.POST['photo']
#     title = request.POST['title']
#     file_type = request.POST['type']
#     lid = request.POST['lid']
#
#     # ====== Save Uploaded Image ======
#     date2 = datetime.now().strftime('%Y%m%d-%H%M%S')
#
#     # ✔ Corrected: Save inside MEDIA_ROOT/image/
#     image_folder = os.path.join(settings.MEDIA_ROOT, "image")
#     os.makedirs(image_folder, exist_ok=True)
#
#     file_path = os.path.join(image_folder, f"{date2}.jpg")
#     with open(file_path, "wb") as f:
#         f.write(base64.b64decode(photo))
#
#     # DB path to return
#     db_image_path = f"/media/image/{date2}.jpg"
#
#     # Gemini config
#     genai.configure(api_key="AIzaSyCPddfWEs9_aUCjLtxARW1GSAMFgg_J0QY")
#     img = Image.open(file_path)
#
#     # ===== Generate Code =====
#     # ✔ Corrected: Save inside MEDIA_ROOT/code/
#     code_output_folder = os.path.join(settings.MEDIA_ROOT, "code")
#     os.makedirs(code_output_folder, exist_ok=True)
#
#     if file_type.lower() == "html":
#         model = genai.GenerativeModel('gemini-2.5-flash')
#         prompt = (
#             "This is a drawing of a form UI. Generate a complete standalone HTML page "
#             "with full HTML structure. Do not include explanation."
#         )
#         response = model.generate_content([img, prompt])
#         code_output = response.text.strip()
#         code_filename = f"{date2}.html"
#
#     elif file_type.lower() == "python":
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         prompt = (
#             "This is a hand-drawn form UI. Generate full Python Tkinter code only."
#         )
#         response = model.generate_content([img, prompt])
#         code_output = response.text.strip()
#         code_filename = f"{date2}.py"
#
#     elif file_type.lower() == "flutter":
#         model = genai.GenerativeModel("gemini-2.5-flash")
#         prompt = (
#             "This is a hand-drawn mobile UI. Generate full Flutter Dart code only."
#         )
#         response = model.generate_content([img, prompt])
#         code_output = response.text.strip()
#         code_filename = f"{date2}.dart"
#
#     else:
#         return JsonResponse({"status": "error", "message": "Invalid file type"})
#
#     # Remove markdown ``` if present
#     code_output = code_output.replace("```", "").strip()
#
#     # Final code path
#     code_path = os.path.join(code_output_folder, code_filename)
#     with open(code_path, "w", encoding="utf-8") as f:
#         f.write(code_output)
#
#     # DB code path
#     db_file_path = f"/media/code/{code_filename}"
#
#     # ===== Save History =====
#     History.objects.create(
#         date=datetime.now().date(),
#         image=db_image_path,
#         title=title,
#         type=file_type,
#         code_file=db_file_path,
#         CUSTOMER_id=Customer.objects.get(USER_id=lid).id
#     )
#
#     # Full URL for Flutter
#     full_url = request.build_absolute_uri(db_file_path)
#     return JsonResponse({'status': 'ok', 'file_url': full_url})

from django.http import JsonResponse

#
# def android_upload_image(request):
#     photo = request.POST['photo']
#     file_type = request.POST['type']
#
#     # Step 1: Image Processing
#     processed_img = process_image(photo)
#
#     # Step 2: Detect Components
#     components = detect_components(processed_img)
#
#     # Step 3: Layout Analysis
#     layout = analyze_layout(components)
#
#     # Step 4: Code Generation
#     if file_type == "html":
#         code = generate_html(layout)
#         filename = "output.html"
#     else:
#         code = generate_flutter(layout)
#         filename = "output.dart"
#
#     # Step 5: Save + Export
#     file_path = save_code(code, filename)
#     zip_file = export_zip(file_path)
#
#     return JsonResponse({
#         "status": "ok",
#         "components": components,
#         "layout": layout,
#         "code": code,
#         "zip": zip_file
#     })


#
# import os
# import base64
# import json
# from datetime import datetime
#
# from django.http import JsonResponse
# from django.conf import settings
# from PIL import Image
# import google.generativeai as genai
# import cv2
# import numpy as np
# from ultralytics import YOLO
# from huggingface_hub import hf_hub_download
#
# # Assuming your models are in the same app
# # from your_app.models import Customer, History  # Uncomment when ready
#
# # Load YOLO Model from Hugging Face (OmniParser-v2.0)
# UI_MODEL = None
# try:
#     model_path = hf_hub_download(
#         repo_id="microsoft/OmniParser-v2.0",
#         filename="icon_detect/model.pt",
#     )
#
#     UI_MODEL = YOLO(model_path)
#     print("YOLO model loaded successfully. Classes:", UI_MODEL.names)
# except Exception as load_err:
#     print(f"Error loading YOLO model: {load_err}")
#     UI_MODEL = None  # Fallback to pure Gemini
#
# def android_upload_image(request):
#     if request.method != 'POST':
#         return JsonResponse({"status": "error", "message": "Only POST allowed"})
#
#     try:
#         photo_base64 = request.POST.get('photo')
#         title = request.POST.get('title', 'Untitled')
#         file_type = request.POST.get('type', 'flutter').lower()
#         lid = request.POST.get('lid')
#
#         if not photo_base64:
#             return JsonResponse({"status": "error", "message": "No photo provided"})
#
#         if not lid:
#             return JsonResponse({"status": "error", "message": "lid (user ID) required"})
#
#         date_str = datetime.now().strftime('%Y%m%d-%H%M%S')
#
#         # 1. Image Processing Module
#         image_folder = os.path.join(settings.MEDIA_ROOT, "image")
#         os.makedirs(image_folder, exist_ok=True)
#         file_path = os.path.join(image_folder, f"{date_str}.jpg")
#
#         img_bytes = base64.b64decode(photo_base64)
#         with open(file_path, "wb") as f:
#             f.write(img_bytes)
#
#         img_cv = cv2.imread(file_path)
#         if img_cv is None:
#             return JsonResponse({"status": "error", "message": "Invalid image"})
#
#         img_cv_resized = cv2.resize(img_cv, (640, 640))
#         img_pil = Image.fromarray(cv2.cvtColor(img_cv_resized, cv2.COLOR_BGR2RGB))
#
#         db_image_path = f"/media/image/{date_str}.jpg"
#
#         # 2. UI Component Detection Module (YOLO)
#         detections = []
#         if UI_MODEL is not None:
#             results = UI_MODEL(img_cv_resized, conf=0.20)  # Adjusted threshold
#             for r in results:
#                 for box in r.boxes:
#                     x1, y1, x2, y2 = map(int, box.xyxy[0])
#                     conf = float(box.conf)
#                     if conf < 0.20:
#                         continue
#                     cls_id = int(box.cls)
#                     label = UI_MODEL.names.get(cls_id, 'interactable')
#                     detections.append({
#                         "label": label,
#                         "bbox": [x1, y1, x2, y2],
#                         "confidence": conf
#                     })
#
#         detections.sort(key=lambda d: d['bbox'][1])
#         detection_json = json.dumps(detections, indent=2)
#
#         # 3. Gemini Config & Dynamic Prompt
#         api_key = "AIzaSyDWNDRbPqFkLeUQ03jyqgcdKUuXs6mWqUQ"  # Hardcoded for now (remove later)
#         genai.configure(api_key=api_key)
#
#         model_name = 'gemini-2.5-flash'  # or 'gemini-2.5-flash' if available
#         model = genai.GenerativeModel(model_name)
#
#         # Dynamic prompt based on file_type
#         if file_type == 'flutter':
#             prompt = f"""
# You are an expert Flutter developer.
# Screenshot of a UI is provided.
# Detected interactable regions (from OmniParser):
# {detection_json}
#
# Infer exact UI elements (buttons, text fields, images, navbar, cards, text, layout), colors, spacing, text content.
# Generate **complete, standalone Flutter Dart code** that exactly recreates this UI.
# Rules:
# - Use Material 3 (useMaterial3: true)
# - Responsive using MediaQuery
# - Exact colors with Color(0xFF...)
# - Widgets: TextField, ElevatedButton/FilledButton, Image.asset placeholder, AppBar if navbar
# - Output ONLY Dart code - no explanations, no markdown fences.
# """
#             ext = 'dart'
#
#         elif file_type == 'html':
#             prompt = f"""
# You are an expert web developer.
# Screenshot of a UI is provided.
# Detected interactable regions:
# {detection_json}
#
# Infer elements, text, colors, layout.
# Generate **complete standalone HTML page** with inline CSS to recreate this UI exactly.
# Rules:
# - Modern HTML5 + CSS (flexbox/grid)
# - Responsive (media queries if needed)
# - Exact colors, spacing
# - Output ONLY full HTML code - no explanations, no fences.
# """
#             ext = 'html'
#
#         elif file_type == 'python':
#             prompt = f"""
# You are an expert Python GUI developer.
# Screenshot of a UI is provided.
# Detected interactable regions:
# {detection_json}
#
# Generate **complete Python Tkinter code** to recreate this UI form.
# Rules:
# - Use Tkinter
# - Output ONLY Python code - no explanations, no fences.
# """
#             ext = 'py'
#
#         else:
#             return JsonResponse({"status": "error", "message": f"Invalid file type: {file_type}"})
#
#         # Generate code
#         response = model.generate_content([img_pil, prompt])
#
#         code_output = response.text.strip()
#         code_output = code_output.replace("```dart", "").replace("```html", "").replace("```python", "").replace("```", "").strip()
#
#         if not code_output:
#             return JsonResponse({"status": "error", "message": "No code generated from Gemini"})
#
#         # Save Generated Code
#         code_folder = os.path.join(settings.MEDIA_ROOT, "code")
#         os.makedirs(code_folder, exist_ok=True)
#         code_filename = f"{date_str}.{ext}"
#         code_path = os.path.join(code_folder, code_filename)
#
#         with open(code_path, "w", encoding="utf-8") as f:
#             f.write(code_output)
#
#         db_code_path = f"/media/code/{code_filename}"
#
#         # Save to History (uncomment when models are ready)
#         # try:
#         customer = Customer.objects.get(USER_id=lid)
#         History.objects.create(
#             date=datetime.now().date(),
#             image=db_image_path,
#             title=title,
#             type=file_type,
#             code_file=db_code_path,
#             CUSTOMER_id=customer.id
#         )
#         # except Exception as db_err:
#         #     print(f"DB save error: {db_err}")
#
#         full_url = request.build_absolute_uri(db_code_path)
#
#         return JsonResponse({
#             'status': 'ok',
#             'file_url': full_url,
#             'detections_count': len(detections),
#             'code_preview': code_output[:400] + '...' if len(code_output) > 400 else code_output
#         })
#
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": f"Server error: {str(e)}"})




import os
import base64
import json
from datetime import datetime

from django.http import JsonResponse
from django.conf import settings
from PIL import Image
import google.generativeai as genai
import cv2
import numpy as np
from ultralytics import YOLO
from huggingface_hub import hf_hub_download

# Uncomment these when your models are ready
# from your_app.models import Customer, History  # replace 'your_app' with actual app name

# Load YOLO Model (OmniParser-v2.0)
UI_MODEL = None
try:
    model_path = hf_hub_download(
        repo_id="microsoft/OmniParser-v2.0",
        filename="icon_detect/model.pt",
    )
    UI_MODEL = YOLO(model_path)
    print("YOLO model loaded OK. Classes:", UI_MODEL.names)
except Exception as e:
    print(f"YOLO load failed: {e}")
    UI_MODEL = None

def android_upload_image(request):
    if request.method != 'POST':
        return JsonResponse({"status": "error", "message": "Only POST allowed"})

    try:
        photo_base64 = request.POST.get('photo')
        title = request.POST.get('title', 'Untitled')
        file_type = request.POST.get('type', 'flutter').lower()
        lid = request.POST.get('lid')

        if not photo_base64:
            return JsonResponse({"status": "error", "message": "No photo provided"})

        if not lid:
            return JsonResponse({"status": "error", "message": "lid required"})

        date_str = datetime.now().strftime('%Y%m%d-%H%M%S')

        # 1. Save & Process Image
        image_folder = os.path.join(settings.MEDIA_ROOT, "image")
        os.makedirs(image_folder, exist_ok=True)
        file_path = os.path.join(image_folder, f"{date_str}.jpg")

        img_bytes = base64.b64decode(photo_base64)
        with open(file_path, "wb") as f:
            f.write(img_bytes)

        img_cv = cv2.imread(file_path)
        if img_cv is None:
            return JsonResponse({"status": "error", "message": "Invalid image"})

        img_cv_resized = cv2.resize(img_cv, (640, 640))
        img_pil = Image.fromarray(cv2.cvtColor(img_cv_resized, cv2.COLOR_BGR2RGB))

        db_image_path = f"/media/image/{date_str}.jpg"

        # 2. YOLO Detection
        detections = []
        if UI_MODEL:
            print("Running YOLO detection...")
            results = UI_MODEL(img_cv_resized, conf=0.20)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf)
                    if conf < 0.20:
                        continue
                    cls_id = int(box.cls)
                    label = UI_MODEL.names.get(cls_id, 'interactable')
                    detections.append({
                        "label": label,
                        "bbox": [x1, y1, x2, y2],
                        "confidence": conf
                    })

        detections.sort(key=lambda d: d['bbox'][1])
        detection_json = json.dumps(detections, indent=2)
        print(f"Detections found: {len(detections)}")

        # 3. Gemini Setup
        api_key = "AIzaSyDWNDRbPqFkLeUQ03jyqgcdKUuXs6mWqUQ"  # Hardcoded – change to env later
        genai.configure(api_key=api_key)

        model_name = 'gemini-2.5-flash'  # FIXED – this is the correct stable model
        model = genai.GenerativeModel(model_name)

        # Dynamic Prompt (shortened for faster response & less lag)
        if file_type == 'flutter':
            prompt = f"""
Expert Flutter developer here.
UI screenshot provided + {len(detections)} detected regions: {detection_json}
Infer all elements, text, colors, layout.
Generate clean, complete Flutter Dart code (Material 3, responsive).
Output ONLY Dart code – nothing else.
"""
            ext = 'dart'

        elif file_type == 'html':
            prompt = f"""
Expert web developer.
UI screenshot + {len(detections)} detected regions: {detection_json}
Infer elements, text, colors, layout.
Generate complete standalone HTML + inline CSS (flex/grid, responsive).
Output ONLY HTML code – no explanations, no markdown.
"""
            ext = 'html'

        elif file_type == 'python':
            prompt = f"""
Expert Python GUI developer.
UI screenshot + {len(detections)} detected regions: {detection_json}
Generate complete Tkinter Python code to recreate UI.
Output ONLY Python code – nothing else.
"""
            ext = 'py'

        else:
            return JsonResponse({"status": "error", "message": f"Invalid type: {file_type}"})

        print(f"Generating {file_type.upper()} code...")

        # Generate
        response = model.generate_content([img_pil, prompt])
        code_output = response.text.strip()
        code_output = code_output.replace("```", "").strip()

        if not code_output:
            return JsonResponse({"status": "error", "message": "Empty response from Gemini"})

        # Save code
        code_folder = os.path.join(settings.MEDIA_ROOT, "code")
        os.makedirs(code_folder, exist_ok=True)
        code_filename = f"{date_str}.{ext}"
        code_path = os.path.join(code_folder, code_filename)

        with open(code_path, "w", encoding="utf-8") as f:
            f.write(code_output)

        db_code_path = f"/media/code/{code_filename}"

        # History save – safe version
        try:
            customer = Customer.objects.get(USER_id=lid)
            History.objects.create(
                date=datetime.now().date(),
                image=db_image_path,
                title=title,
                type=file_type,
                code_file=db_code_path,
                CUSTOMER_id=customer.id
            )
            print("History saved successfully")
        except Exception as db_err:
            print(f"History save skipped: {str(db_err)}")

        full_url = request.build_absolute_uri(db_code_path)

        return JsonResponse({
            'status': 'ok',
            'file_url': full_url,
            'detections_count': len(detections),
            'code_preview': code_output[:400] + '...' if len(code_output) > 400 else code_output
        })

    except Exception as e:
        print(f"Server error: {str(e)}")  # log to console
        return JsonResponse({"status": "error", "message": f"Server error: {str(e)}"})