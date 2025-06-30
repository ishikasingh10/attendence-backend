from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate
from .models import *
from .serializers import *
from datetime import timedelta
import uuid
from collections import defaultdict


@api_view(['POST'])
def login_employee(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        try:
            employee = Employee.objects.get(user=user)
            return Response(EmployeeSerializer(employee).data)
        except Employee.DoesNotExist:
            return Response({"error": "Not registered as employee"}, status=403)
    return Response({"error": "Invalid credentials"}, status=401)


@api_view(['GET'])
def get_attendance(request):
    username = request.GET.get("username")
    date = request.GET.get("date")
    month = request.GET.get("month")

    try:
        employee = Employee.objects.get(user__username=username)
        logs = Attendance.objects.filter(employee=employee)

        if date:
            logs = logs.filter(date=date)
        elif month:
            year, mon = month.split('-')
            logs = logs.filter(date__year=year, date__month=mon)

        response = []
        for log in logs.order_by('-date'):
            response.append({
                "date": log.date,
                "day": log.date.strftime("%A"),
                "check_in": log.check_in_time.strftime("%H:%M:%S") if log.check_in_time else "—",
                "check_out": log.check_out_time.strftime("%H:%M:%S") if log.check_out_time else "—",
            })

        return Response(response)

    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)


@api_view(['POST'])
def generate_qr(request):
    username = request.data.get("username")
    mode = request.data.get("mode")
    try:
        employee = Employee.objects.get(user__username=username)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)

    token = str(uuid.uuid4())
    expires_at = timezone.now() + timedelta(minutes=2)

    qr = QRCodeSession.objects.create(
        token=token,
        employee=employee,
        mode=mode,
        expires_at=expires_at
    )
    return Response(QRCodeSessionSerializer(qr).data)


@api_view(['POST'])
def cancel_qr(request):
    token = request.data.get("token")
    try:
        qr = QRCodeSession.objects.get(token=token)
        qr.is_active = False
        qr.save()
        return Response({"status": "cancelled"})
    except QRCodeSession.DoesNotExist:
        return Response({"error": "Invalid token"}, status=404)


@api_view(['POST'])
def mark_attendance(request):
    token = request.data.get("token")
    try:
        qr = QRCodeSession.objects.get(token=token, is_active=True)
        if qr.is_expired():
            return Response({"error": "QR expired"}, status=400)

        current_time = timezone.now()
        attendance, _ = Attendance.objects.get_or_create(
            employee=qr.employee, date=current_time.date()
        )

        if qr.mode == "checkin" and not attendance.check_in_time:
            attendance.check_in_time = current_time
        elif qr.mode == "checkout" and not attendance.check_out_time:
            attendance.check_out_time = current_time
        else:
            return Response({"error": "Already marked"}, status=400)

        attendance.save()
        qr.is_active = False
        qr.save()

        return Response({
            "status": "marked",
            "employee": qr.employee.user.username,
            "mode": qr.mode,
            "time": current_time
        })
    except QRCodeSession.DoesNotExist:
        return Response({"error": "Invalid token"}, status=404)


def live_qr_display(request):
    active_qrs = QRCodeSession.objects.filter(is_active=True, expires_at__gt=timezone.now())
    
    grouped = defaultdict(dict)
    for qr in active_qrs:
        key = qr.employee.user.username
        grouped[key]["employee"] = qr.employee
        grouped[key][qr.mode] = qr  # adds either 'checkin' or 'checkout'

    # ⚠️ Convert defaultdict to normal dict to avoid Django rendering issues
    return render(request, 'qr_app/live_qr.html', {
        'grouped_qrs': dict(grouped),  # 👈 Fix here
        'now': timezone.now()
    })