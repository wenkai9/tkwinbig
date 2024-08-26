from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from .models import order_indo, payment_info
from datetime import datetime
import uuid


@csrf_protect
@transaction.atomic
def generate_order(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            total_amount = request.POST.get('total_amount')
            payment_way = request.POST.get('payment_way')
            order_comment = request.POST.get('order_comment')

            # 生成唯一订单ID
            order_id = uuid.uuid4().hex

            # 创建订单
            order = order_indo.objects.create(
                order_id=order_id,
                total_amount=total_amount,
                order_status='待支付',  # 假设初始状态为待支付
                user_id=user_id,
                payment_way=payment_way,
                order_comment=order_comment,
                createAt=datetime.now()
            )

            return JsonResponse({'order_id': order_id, 'total_amount': total_amount, 'order_comment': order_comment},
                                status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': '只允许POST请求'}, status=405)


@csrf_protect
@transaction.atomic
def process_payment(request):
    if request.method == 'POST':
        try:
            order_id = request.POST.get('order_id')

            # 获取订单
            order = order_indo.objects.select_for_update().get(order_id=order_id)

            # 将订单状态更新为'已支付'
            order.order_status = '已支付'
            order.save()

            # 创建支付记录
            payment_info.objects.create(
                order=order,
                user=order.user,
                payment_way=order.payment_way,
                total_amount=order.total_amount,
                payment_status='已支付',  # 假设支付成功
                createAt=datetime.now()
            )

            return JsonResponse({'success': '支付成功'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': '只允许POST请求'}, status=405)


@csrf_protect
def display_order(request, order_id):
    try:
        # 获取订单
        order = order_indo.objects.get(order_id=order_id)

        # 准备订单信息
        order_info = {
            'order_id': order.order_id,
            'total_amount': order.total_amount,
            'order_status': order.order_status,
            'user_id': order.user_id,
            'payment_way': order.payment_way,
            'order_comment': order.order_comment,
            'createAt': order.createAt.strftime("%Y-%m-%d %H:%M:%S"),
            'updateAt': order.updateAt.strftime("%Y-%m-%d %H:%M:%S")
        }

        return JsonResponse(order_info, status=200)
    except order_indo.DoesNotExist:
        return JsonResponse({'error': '订单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
