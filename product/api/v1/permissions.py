from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.v1.serializers.user_serializer import SubscriptionSerializer
from users.models import Balance, Subscription


def make_payment(user, course):
    user_balance = get_object_or_404(Balance, user=user)

    if user_balance.amount < course.price:
        return {"status": "failed", "message": "Недостаточно средств для покупки курса."}

    user_balance.amount -= course.price
    user_balance.save()

    return {"status": "success", "message": "Оплата прошла успешно."}


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        course_id = view.kwargs.get('course_id')
        return Subscription.objects.filter(user=request.user, course_id=course_id).exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return Subscription.objects.filter(user=request.user, course=obj).exists()

class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
