from typing import List
import logging

from barter_auth.v2.utils import calculate_user_balance
import logging
from typing import List

from barter_auth.v2.utils import calculate_user_balance
from global_settings.models import KitPlan, TradingPlans

log = logging.getLogger('django')  # default logger for django

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q, Sum, F
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, viewsets, status
from rest_framework.serializers import CharField, DictField, DateField, EmailField
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

import barter_auth.helpers

from barter_auth.handlers import send_activate_user, activate_user, send_recovery_password, recover_password
from barter_auth.models import BarterUser, Referral, BarterPlan, BarterUserSecurityProfile, BarterUserNode, \
    BarterTradingPlan
from barter_auth.serializers import RegisterSerializer, BarterUserSerializer, BarterUserProfileSerializer, \
    ReferralListSerializer, BarterPlanSerializer, BarterUserSecurityProfileSerializer, \
    BarterUserChangePasswordSerializer, BarterUserCheckEmailSerializer, BarterTradingPlanSerializer, \
    BarterUserNodeSerializer
from barter_auth.utils import generate_referral_code
from barter_auth.v2.utils import get_month_dates
from transactions.handlers import get_capital_trading
from transactions.models import Transaction

from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiParameter, PolymorphicProxySerializer, inline_serializer

# Create your views her
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        referral_code = self.request.query_params.get('referral_code')

        request.data['referral_code'] = generate_referral_code()
        if referral_code:
            try:
                referred_from = BarterUser.objects.get(referral_code=referral_code)
            except BarterUser.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, 
                                data={'message': 'El codigo de referido no es valido.'})
            
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            user.referred_by = referred_from
            user.save()
            
            barter_auth.helpers.add_user_to_network(user)

            dni_image = request.data.get('dni_image')
            dni_back_image = request.data.get('dni_back_image')
            terms_and_conditions: bool = request.data.get('terms_and_conditions')

            if not terms_and_conditions:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'message': 'Tu debes de aceptar terminos y condiciones'})

            security_profile = BarterUserSecurityProfile.objects.create(
                user=user, dni_image=dni_image, dni_back_image=dni_back_image, terms_and_conditions=terms_and_conditions
            )

            security_profile.save()
            category = request.data.get('category') or "common"

            node = BarterUserNode.objects.create(user=referred_from, investment=user, category=category)
            node.save()

            transactions = request.data.get('transactions')

            for transaction in transactions:
                obj = Transaction.objects.create(
                    user=user,
                    transaction_hash=transaction['transactionHash'],
                    description='Initial Investment', amount=transaction['amount'],
                    transaction_status=0)
                obj.save()

            send_activate_user(user)

            return Response({
                'user': BarterUserSerializer(user, context=self.get_serializer_context()).data,
                'token': AuthToken.objects.create(user)[1]
            })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dni_image = request.data.get('dni_image')
        dni_back_image = request.data.get('dni_back_image')
        terms_and_conditions: bool = request.data.get('terms_and_conditions')

        if not terms_and_conditions or dni_image == '' or dni_back_image == '':
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'Tu debes de completar el perfil'})

        user = serializer.save()

        security_profile = BarterUserSecurityProfile.objects.create(
            user=user, dni_image=dni_image, dni_back_image=dni_back_image, terms_and_conditions=terms_and_conditions
        )

        security_profile.save()

        transactions = request.data.get('transactions')

        for transaction in transactions:
            obj = Transaction.objects.create(
                user=user,
                transaction_hash=transaction['transactionHash'],
                description='Initial Investment', amount=transaction['amount'],
                transaction_status=0)
            obj.save()

        send_activate_user(user)

        return Response({
            'user': BarterUserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })

@extend_schema_view(
    get=extend_schema(parameters=[OpenApiParameter(allow_blank=False, name='token', required=True, type=str, location=OpenApiParameter.QUERY, description='Token need to pass as URL parameter.')], responses={200: OpenApiResponse(description='message: Usuario activado correctamente'), 400: OpenApiResponse(description='message: URL inválida, revise o llene el formulario de recuperación nuevamente.')})
)
class ActivateUserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        if activate_user(token):
            return Response(status=status.HTTP_200_OK, data={
                'message': 'Usuario activado correctamente'
            })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'message': 'URL inválida, revise o llene el formulario de recuperación nuevamente.'
            })

@extend_schema_view(
    post=extend_schema(methods=['POST'], request=inline_serializer(name='RecoveryPasswordSendSerializer', fields={'email': EmailField()}), responses={200: OpenApiResponse(description='message: Si el correo está en nuestros registros, debió haber llegado un correo para cambio de contraseña.')}),
    put=extend_schema(methods=['PUT'], parameters=[OpenApiParameter(allow_blank=False, required=True, name='token', type=str)], request=inline_serializer(name='RecoveryPasswordSerializer', fields={'password': CharField(style={'input_type': 'password'})}), responses={200: OpenApiResponse(description='message: Contraseña cambiada exitosamente'), 400: OpenApiResponse(description='message: URL inválida, revise o intente nuevamente.')})
)
class RecoveryPasswordAPIView(APIView):

    @action(url_path='recovery-password', detail=False, methods=['post'])
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = BarterUser.objects.get(email=email)
            send_recovery_password(user)
        except BarterUser.DoesNotExist:
            pass
        return Response(status=status.HTTP_200_OK, data={
            'message': 'Si el correo está en nuestros registros, debió haber llegado un correo para cambio de contraseña.'
        })

    @action(url_path='recovery-password', detail=False, methods=['put'])
    def put(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        password = request.data.get('password')
        if recover_password(token, password):
            return Response(status=status.HTTP_200_OK, data={
                'message': 'Contraseña cambiada exitosamente'
            })
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'message': 'URL inválida, revise o intente nuevamente.'
            })


class CheckEmailAPIView(generics.GenericAPIView):
    serializer_class = BarterUserCheckEmailSerializer

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            user = BarterUser.objects.get(email=email)
            return Response(status=status.HTTP_200_OK, data=True)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND, data=False)

@extend_schema_view(
    post=extend_schema(request=inline_serializer(name='ChangePasswordSerializer', fields={'email': EmailField(), 'old_password': CharField(), 'new_password': CharField()}), responses={200: OpenApiResponse(description='message: Contraseña cambiada correctamente.'), 400: OpenApiResponse(description="- error: User doesn't exist\n- error: Missing fields\n- error: Something got wrong") })
)
class ChangePasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            old_password = request.data.get('old_password')
            new_password = request.data.get('new_password')

            if not old_password or not new_password or not email:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={
                    'error': 'Missing fields'
                })

            user = BarterUser.objects.get(email=email)

            if not user.check_password(old_password):
                raise Exception('Old password is incorrect')

            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK, data={
                'message': 'Contraseña cambiada correctamente.'
            })
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'error': "User doesn't exist"
            })
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                'error': "Something got wrong"
            })

@extend_schema_view(
    post=extend_schema(request=AuthTokenSerializer, responses={200: inline_serializer(name='LoginApiSerializer', fields= { **BarterUserSerializer().fields.fields, 'token': CharField(), 'expire': DateField(), 'user': BarterUserSerializer()})})
)
class LoginAPIView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user)

        user_serializer = BarterUserSerializer(user)
        auth_data = super(LoginAPIView, self).post(request, format=None).data

        user_data = {**user_serializer.data, **auth_data}
        return Response(user_data)


class BarterUserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BarterUserProfileSerializer
    queryset = BarterUser.objects.all()

    @action(detail=True)
    def plans_balance(self, request, pk=None):
        try:
            user = BarterUser.objects.get(pk=pk)
            # Get all transactions that doesn't involve kit plans and trading
            transactions = user.transactions.filter(~Q(description__icontains='Kit Plan'),
                                                    ~Q(description__icontains='Trading'),
                                                    transaction_status=1).aggregate(Sum('amount'))
            # if amount is None, set it to 0
            transactions_amount = transactions['amount__sum'] if transactions['amount__sum'] else 0
            # Get all transactions related to kit plans
            kit_plans = user.transactions.filter(description__icontains='Kit Plan', transaction_status=1).aggregate(
                Sum('amount'))
            # if amount is None, set it to 0
            kit_plans_amount = kit_plans['amount__sum'] if kit_plans['amount__sum'] else 0
            # Get all transactions related to trading plans
            trading_plans = get_capital_trading(user)
            # if amount is None, set it to 0
            kit_plans_amount = kit_plans['amount__sum'] if kit_plans['amount__sum'] else 0

            # co_founder_earning = get_renueve_co_founder(user)
            # co_founder_capital = get_capital_co_founder(user)

            co_founder_capital = 0
            cofounder_transactions = Transaction.objects.filter(
                user=user,
                transaction_status=1,
                transaction_type='co-founder'
            )

            cofounder_reinvestments = user.re_investments.filter(
                type_re_investment='Co-Founder'
            )

            if cofounder_transactions:
                co_founder_capital += cofounder_transactions.aggregate(Sum('amount'))['amount__sum']
            if cofounder_reinvestments:
                co_founder_capital += cofounder_reinvestments.aggregate(Sum('amount'))['amount__sum']

            co_founder_earning = 0
            cofounder_earnings_by_trading = user.co_founder_earning_by_trading.all()
            cofounder_earnings_by_product = user.co_founder_earning_by_products.all()
            cofounder_earnings_withdrawals = user.withdrawals.filter(
                transaction_status=1,
                source_of_profit='CO_FOUNDER'
            )

            if cofounder_earnings_by_trading:
                co_founder_earning += cofounder_earnings_by_trading.aggregate(Sum('earnings'))['earnings__sum']
            if cofounder_earnings_by_product:
                co_founder_earning += cofounder_earnings_by_product.aggregate(Sum('earnings'))['earnings__sum']
            if cofounder_earnings_withdrawals:
                co_founder_earning -= cofounder_earnings_withdrawals.aggregate(Sum('amount'))['amount__sum']
            if cofounder_reinvestments:
                co_founder_earning -= cofounder_reinvestments.aggregate(Sum('amount'))['amount__sum']

            # Get all kit plans and calculate revenue
            user_kit_plans = user.plans.all()
            user_kit_plans_revenue = 0

            for plan in user_kit_plans:
                user_kit_plans_revenue += plan.yearly_revenue

            trading_inversions_revenue = calculate_user_balance(user)['trading']['current_earnings']

            data = {
                'kit_plan': kit_plans_amount,
                'trading_plan': trading_plans,
                'transactions': transactions_amount,
                'kit_plan_revenue': user_kit_plans_revenue,
                'trading_daily_revenue': trading_inversions_revenue,
                'co_founder_earning': co_founder_earning,
                'co_founder_capital': co_founder_capital,
                'total_revenue': user_kit_plans_revenue + (
                    trading_inversions_revenue if trading_inversions_revenue is not None else 0)
            }

            # Validate that the balances are not negative. If it is negative, it changes to 0 and notifies via log.
            for key in data:
                if data[key] < 0:
                    log.error(
                        f'Negative Balance ({data[key]}) in "{key}" for the user: "{user.get_full_name}" with email: "{user.email}". Showing "{key}" as 0.')
                    data[key] = 0

            return Response(status=status.HTTP_200_OK, data=data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.__dict__)

    @action(detail=True, url_path='summary-trading', methods=['get'])
    def summary_trading(self, request, pk=None):
        user = BarterUser.objects.get(pk=pk)
        total_revenue = calculate_user_balance(user)['trading']['current_network_earnings']
        total_revenue = float(total_revenue) if total_revenue else 0
        return Response(status=status.HTTP_200_OK, data={
            'total_revenue': total_revenue
        })

    @staticmethod
    def get_network_trading_revenue(nodes: List[BarterUserNode], percentage: float):
        total = 0
        user_nodes = [node for node in nodes if node.investment.has_trading_plan]
        users_in_level = len(user_nodes)
        for user in user_nodes:
            total += user.investment.bartertradingplan_set.all().aggregate(Sum('trading_amount'))['trading_amount__sum']
        divide_total = float(total) * 0.7

        network_total = divide_total * 0.15

        data = {
            'count': users_in_level,
            'revenue': round(network_total * percentage, 2),
            'percentage': percentage
        }

        return data

    @action(detail=True, url_path='summary-plans', methods=['get'])
    def summary_plans(self, request, pk=None):
        """
        Get all plans and its status, by level
        @param request:
        @param pk:  User id
        @return:
        """
        barter_user = BarterUser.objects.get(pk=pk)

        revenue = calculate_user_balance(barter_user)['kitplan']['current_network_earnings']


        total_revenue = {
            'total_revenue': revenue
        }

        return Response(status=status.HTTP_200_OK, data={
            'data': total_revenue,
            'total_revenue': total_revenue['total_revenue']
        })

    @staticmethod
    def get_kit_plan_revenue(user_nodes: list, percentage: float):
        # is a list of BarterUserNode objects
        total = 0
        # remove if user_node is not a kit plan
        user_nodes = [user_node for user_node in user_nodes if user_node.investment.has_plan]
        for user_node in user_nodes:
            # total plans
            total += user_node.investment.plans.all().aggregate(Sum('selected_plan'))['selected_plan__sum']

        # round to 2 decimals
        return round(total * percentage * 0.2, 2), len(user_nodes)

    @action(detail=True)
    def trading_revenue_history(self, request, pk=None):
        try:
            user = BarterUser.objects.get(pk=pk)
            history = []

            # Old earning
            for user_renueve in user.earnings.all():
                history.append({
                    'date': user_renueve.earnings_date,
                    'traded_amount': user_renueve.current_investment,
                    'percentage': user_renueve.earnings_percentage,
                    'traded_revenue': user_renueve.earnings
                })
            # New earning
            for user_renueve in user.trading_earnings.filter(enabled=True):
                month, year = user_renueve.trading_percentage.month, user_renueve.trading_percentage.year 
                _, date_last_day, _ = get_month_dates(month=month, year=year)

                history.append({
                    'date': date_last_day.date(),
                    'traded_amount': user_renueve.current_investment,
                    'percentage': user_renueve.trading_percentage_used,
                    'traded_revenue': user_renueve.earnings
                })
            return Response(status=status.HTTP_200_OK, data=history)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, url_path='confirm-password')
    def confirm_password(self, request, pk=None):
        try:
            user = BarterUser.objects.get(pk=pk)
            return Response(data=check_password(request.data.get("password"), user.password), status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, url_path='send-active-key')
    def send_active_key(self, request, pk=None):
        try:
            user = BarterUser.objects.get(pk=pk)
            if user.verified:
                return Response(data={"message": "Usuario ya activo."}, status=status.HTTP_200_OK)
            send_activate_user(user)
            return Response(data={"message": "Revise su correo por favor."}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ReferralViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ReferralListSerializer
    queryset = Referral.objects.all()

    @action(detail=True)
    def user_branches(self, request, pk=None):
        if pk:
            user = BarterUser.objects.get(pk=pk)

            referrals = user.branch.all()

            serializer = ReferralListSerializer(referrals, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class BarterNodesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BarterUserNodeSerializer
    queryset = BarterUserNode.objects.all()

    @action(detail=True)
    def network(self, request, pk=None):
        try:
            if pk:
                user = BarterUser.objects.get(pk=pk)
                nodes = user.node_branch.all()
                serializer = BarterUserNodeSerializer(nodes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise Exception(e)


class BarterPlanViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BarterPlanSerializer
    queryset = BarterPlan.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = BarterPlanSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            plan = serializer.validated_data

            # se obtiene el kitplan mas cercano al precio seleccionado (siempre debería haber uno)
            kit_plan = KitPlan.objects.filter(price__gte=plan['selected_plan'], enabled=True).order_by('price').first()
            if not kit_plan:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'No Kit Plan found'})

            serializer.validated_data['plan'] = kit_plan

            wallet_provider = request.data.get('wallet_provider', '--')
            wallet_address = request.data.get('wallet_address', '--')
            transaction_type = request.data.get('transaction_type', 'invest')
            transaction_network = request.data.get('transaction_network', '--')
            voucher_screenshot = request.data.get('voucher_screenshot', '--')

            transaction = Transaction.objects.create(
                user_id=plan['user'].id,
                transaction_hash=plan['transaction_hash'],
                description=f"${plan['selected_plan']} Kit Plan",
                transaction_status=0,
                amount=plan['selected_plan'],
                wallet_address=wallet_address,
                wallet_provider=wallet_provider,
                transaction_type=transaction_type,
                transaction_network=transaction_network,
                voucher_screenshot=voucher_screenshot
            )
            transaction.save()

            # se guarda la transaccion en el plan
            serializer.validated_data['transaction'] = transaction
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e

    @action(detail=True)
    def by_user(self, request, pk=None):
        if pk:
            plans = BarterPlan.objects.filter(user_id=pk)

            page = self.paginate_queryset(plans)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(plans, many=True)

            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class BarterTradingPlanViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BarterTradingPlanSerializer
    queryset = BarterTradingPlan.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = BarterTradingPlanSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            plan = serializer.validated_data

            # se obtiene el trading plan mas cercano al precio seleccionado (siempre debería haber uno)
            trading_plan = TradingPlans.objects.filter(
                price__gte=plan['trading_amount'], enabled=True).order_by('price').first()
            if not trading_plan:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'No Trading Plan found'})

            serializer.validated_data['plan'] = trading_plan

            wallet_provider = request.data.get('wallet_provider', '--')
            wallet_address = request.data.get('wallet_address', '--')
            transaction_type = request.data.get('transaction_type', 'invest')
            transaction_network = request.data.get('transaction_network', '--')
            voucher_screenshot = request.data.get('voucher_screenshot', '--')

            transaction = Transaction.objects.create(
                user_id=plan['user'].id,
                transaction_hash=plan['transaction_hash'],
                description=f"Inversion Trading ${plan['trading_amount']}",
                transaction_status=0,
                amount=plan['trading_amount'],
                wallet_provider=wallet_provider,
                wallet_address=wallet_address,
                transaction_type=transaction_type,
                transaction_network=transaction_network,
                voucher_screenshot=voucher_screenshot
            )
            transaction.save()

            # se guarda la transaccion en el plan
            serializer.validated_data['transaction'] = transaction
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise e

    @action(detail=True)
    def by_user(self, request, pk=None):
        if pk:
            plans = BarterTradingPlan.objects.filter(user_id=pk)

            page = self.paginate_queryset(plans)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(plans, many=True)

            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)


class BarterUserSecurityProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = BarterUserSecurityProfileSerializer
    queryset = BarterUserSecurityProfile.objects.all()


class BarterUserChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = BarterUserChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                user = BarterUser.objects.get(email=serializer.data.get('email'))

                user.set_password(serializer.data.get('new_password'))
                user.save()

                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Contraseña cambiada correctamente',
                    'data': []
                }

                return Response(response)

            except BarterUser.DoesNotExist:
                return Response({"email": ["Email does not exist."]}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


router = DefaultRouter()
router.register('api/users', BarterUserViewSet, basename='Users')
router.register('api/user_profiles', BarterUserSecurityProfileViewSet, basename='Security Profile')
router.register('api/network', BarterNodesViewSet, basename='Referrals')
router.register('api/plans', BarterPlanViewSet, basename='Plans')
router.register('api/trading_plans', BarterTradingPlanViewSet, basename='Trading Plans')
