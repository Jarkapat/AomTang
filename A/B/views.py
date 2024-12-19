from django.shortcuts import render

from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render, redirect
import logging
from B.models import CustomUser
from django.contrib.auth import login, authenticate ,logout


class HomeView(TemplateView):
    template_name = 'home_page.html'

class HV(TemplateView):
    template_name = 'H.html'

# Create your models here.
logger = logging.getLogger(__name__)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Debug: แสดงค่าที่รับจากฟอร์ม
        logger.debug(f"Received username: {username}")
        logger.debug(f"Received password1: {password1}")
        logger.debug(f"Received password2: {password2}")
        
        # ตรวจสอบว่ารหัสผ่านตรงกันหรือไม่
        if password1 != password2:
            logger.debug("Passwords do not match!")
            messages.error(request, 'รหัสผ่านไม่ตรงกัน')
            return redirect('register')  # กลับไปที่หน้า register
        
        try:
            # Debug: ลองสร้างผู้ใช้ใหม่
            logger.debug("Creating new CustomUser...")
            user = CustomUser.objects.create_user(username=username, password=password1)
            user.save()
            
            # Debug: ผู้ใช้ถูกสร้างแล้ว
            logger.debug(f"User created: {user}")
            
            messages.success(request, 'บัญชีผู้ใช้ถูกสร้างเรียบร้อยแล้ว!')
            return redirect('login')  # ไปที่หน้า login
        except Exception as e:
            # ถ้ามีข้อผิดพลาด ให้แสดงข้อผิดพลาด
            logger.error(f"Error occurred while creating user: {e}")
            messages.error(request, f'เกิดข้อผิดพลาด: {e}')
            return redirect('login')
    
    # ถ้าไม่ได้ส่งข้อมูลด้วย POST ก็ให้ render หน้า register
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Debug: แสดงข้อมูลที่ผู้ใช้กรอก
        print(f"Username: {username}")
        print(f"Password: {password}")  # ระวังการแสดงรหัสผ่านใน log จริง

        user = authenticate(request, username=username, password=password)
        
        # Debug: ตรวจสอบผลลัพธ์จากการ authenticate
        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            request.session[user.id] = user.id
            request.session['username'] = user.username
            request.session['is_authenticated'] = True
            messages.success(request, 'เข้าสู่ระบบสำเร็จ')
            print("Redirecting to route_list")
            return redirect('H')
        else:
            print("Authentication failed")
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    
    return render(request, 'login.html')