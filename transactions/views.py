from django.db.models import Sum, F
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from decimal import Decimal

from barter_auth.models import PlansEarnings
from transactions.handlers import get_renueve_co_founder, get_capital_trading, get_renueve_trading_personal, \
    get_renueve_trading_network, get_capital_co_founder, get_renueve_trading_total
from transactions.models import TransactionType, Transaction, Withdrawal, TransactionScreenshot, \
    MonthlyTradingEarningsPerLeader, DetailCoFounderEarningByTrading, \
    DetailCoFounderEarningByProducts, ReInvestments, UserDailyTradingRevenue, TradingEarnings, TradingNetWorkEarnings, KitPlanNetWorkEarnings
from transactions.serializers import TransactionTypeSerializer, ListTransactionSerializer, \
    WriteTransactionSerializer, WithdrawalSerializer, \
    GeneralDetailCoFounderEarningByTradingSerializer, GeneralDetailCoFounderEarningByProductsSerializer, \
    ReInvestmentsSerializer, ReInvestmentsAvailableSerializer
    
from barter_auth.v2.utils import calculate_user_balance


# Create your views here.
class TransactionTypeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Transaction.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListTransactionSerializer
        if self.action == 'create':
            return WriteTransactionSerializer
        return ListTransactionSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        print(serializer.validated_data)

        if len(TransactionScreenshot.objects.filter(transaction=instance, voucher_screenshot=serializer.validated_data[
            'voucher_screenshot'])) == 0:
            screenshot = TransactionScreenshot(
                transaction=instance,
                voucher_screenshot=serializer.validated_data['voucher_screenshot'],
                transaction_date=serializer.validated_data['transaction_date']
            )
            screenshot.save()

        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=True)
    def by_user(self, request, pk=None):
        if pk:
            transactions = Transaction.objects.filter(user_id=pk)

            page = self.paginate_queryset(transactions)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(transactions, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def by_hash(self, request):

        transaction_hash = request.query_params.get('transaction_hash', None)
        transactions = Transaction.objects.filter(transaction_hash=transaction_hash)
        page = self.paginate_queryset(transactions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)


class WithdrawalViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer

    @action(detail=True)
    def by_user(self, request, pk=None):
        if pk:
            withdrawals = Withdrawal.objects.filter(user_id=pk)

            page = self.paginate_queryset(withdrawals)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(withdrawals, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        # obteniendo ganancias del usuario
        user = request.user
        total_revenue = 0

        try:
            amount = float(request.data['amount'])

            if amount < 10:
                return Response(data={
                    'message': 'El monto a retirar debe ser un valor mayor a 10'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(data={
                'message': 'El monto a retirar debe ser un valor mayor a 10'
            }, status=status.HTTP_400_BAD_REQUEST)

        if request.data['source_of_profit'] == 'TRADING':
            user_revenue = calculate_user_balance(user)
            total_revenue = (user_revenue['trading']['current_earnings']
                             + user_revenue['trading']['current_network_earnings'])

            pending_withdrawals_amount = user.withdrawals.filter(
                transaction_status__in=[0],
                source_of_profit='TRADING'
            ).aggregate(Sum('amount'))['amount__sum']

            if pending_withdrawals_amount:
                total_revenue -= Decimal(pending_withdrawals_amount)
        elif request.data['source_of_profit'] == 'KIT_PLAN':
            total_revenue = calculate_user_balance(user)['kitplan']['current_network_earnings']

            pending_withdrawals_amount = user.withdrawals.filter(
                transaction_status=0,
                source_of_profit='KIT_PLAN'
            ).aggregate(Sum('amount'))['amount__sum']

            pending_withdrawals_amount = float(pending_withdrawals_amount) if pending_withdrawals_amount else 0
            total_revenue = float(total_revenue) if total_revenue else 0

            total_revenue -= pending_withdrawals_amount

        elif request.data['source_of_profit'] == 'CO_FOUNDER':
            total_revenue = 0

            cofounder_earnings_by_trading = user.co_founder_earning_by_trading.all()
            cofounder_earnings_by_product = user.co_founder_earning_by_products.all()

            if cofounder_earnings_by_trading:
                total_revenue += cofounder_earnings_by_trading.aggregate(Sum('earnings'))['earnings__sum']
            if cofounder_earnings_by_product:
                total_revenue += cofounder_earnings_by_product.aggregate(Sum('earnings'))['earnings__sum']

            total_revenue = float(total_revenue) if total_revenue else 0

            pending_withdrawals_amount = user.withdrawals.filter(
                transaction_status__in=[0, 1],
                source_of_profit='CO_FOUNDER'
            ).aggregate(Sum('amount'))['amount__sum']

            total_revenue -= float(pending_withdrawals_amount) if pending_withdrawals_amount else 0

            re_investments = ReInvestments.objects.filter(
                user=user,
                type_re_investment='Co-Founder'
            ).aggregate(Sum('amount'))['amount__sum']

            re_investments = float(re_investments) if re_investments else 0

            total_revenue -= re_investments

        if total_revenue < float(request.data['amount']):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'message': f"No tienes suficiente dinero para retirar, lo m\u00e1ximo que puedes retirar es {Decimal(f'{total_revenue:.2f}')}"
                            })
        return super().create(request, *args, **kwargs)


class CoFounderEarningByTradingView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GeneralDetailCoFounderEarningByTradingSerializer

    def get_queryset(self):
        return DetailCoFounderEarningByTrading.objects.filter(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GeneralDetailCoFounderEarningByTradingSerializer({
            'details': queryset,
            'total': queryset.aggregate(Sum('earnings'))['earnings__sum'],
            'total_paid': queryset.aggregate(Sum('earnings_paid'))['earnings_paid__sum']
        })
        return Response(serializer.data)


class CoFounderEarningByProductView(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GeneralDetailCoFounderEarningByProductsSerializer

    def get_queryset(self):
        return DetailCoFounderEarningByProducts.objects.filter(user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GeneralDetailCoFounderEarningByProductsSerializer({
            'details': queryset,
            'total': queryset.aggregate(Sum('earnings'))['earnings__sum'],
            'total_paid': queryset.aggregate(Sum('earnings_paid'))['earnings_paid__sum']
        })
        return Response(serializer.data)


class ReInvestmentsView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ReInvestmentsSerializer

    def get_queryset(self):
        return ReInvestments.objects.filter(user=self.request.user)

    def list(self, *args, **kwargs):
        print('Logged as: ', self.request.user)
        queryset = self.get_queryset()
        serializer = ReInvestmentsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # return Response(data={
        #     'message': 'Operacion inhabilitada temporalmente'
        # }, status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = request.user.id
        amount = 0.0
        try:
            amount = float(request.data['amount'])
        except (ValueError, TypeError):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'El monto debe ser un número'})

        if amount < 10:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'El monto minimo de reinversion debe ser mayor o igual a 10'})

        # if request.data['type_re_investment'] == 'Trading' and amount > get_renueve_trading_total(
        #         request.user):
        #     return Response(status=status.HTTP_400_BAD_REQUEST,
        #                     data={'message': f'No tienes suficiente dinero para reinvertir'})

        # region trading reinvestments
        if request.data['type_re_investment'] == 'Trading':
            user_current_earnings = 0

            # user_trading_earnings = UserDailyTradingRevenue.objects.filter(
            #     user=request.user
            # )
            user_trading_earnings = TradingEarnings.objects.filter(
                user=request.user,
                enabled=True
            )
            reinvestments = ReInvestments.objects.filter(
                user=request.user,
                type_re_investment='Trading'
            )
            user_approved_and_pending_withdrawals = Withdrawal.objects.filter(
                user=request.user,
                source_of_profit='TRADING',
                transaction_status__in=[0, 1]  # Pending and approved
            )
            # user_network_earnings = MonthlyTradingEarningsPerLeader.objects.filter(
            #     user=request.user
            # )
            user_network_earnings = TradingNetWorkEarnings.objects.filter(
                unilevel_network__user=request.user,
                enabled=True
            )
            if user_trading_earnings:
                user_current_earnings += user_trading_earnings.aggregate(Sum('earnings'))['earnings__sum']
            if user_approved_and_pending_withdrawals:
                user_current_earnings -= user_approved_and_pending_withdrawals.aggregate(Sum('amount'))['amount__sum']

            if user_network_earnings:
                user_current_earnings += user_network_earnings.aggregate(Sum('earnings'))['earnings__sum']
            if reinvestments:
                user_current_earnings -= reinvestments.aggregate(Sum('amount'))['amount__sum']

            if amount > user_current_earnings:
                return Response(data={
                    'message': 'No tienes suficientes fondos para reinvertir'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return super().create(request, *args, **kwargs)
        # endregion
        # elif request.data['type_re_investment'] == 'CoFounder' and amount > get_renueve_co_founder(
        #         request.user):
        elif request.data['type_re_investment'] == 'Co-Founder':
            user_current_earnings = 0
            
            cofounder_earnings_by_trading = DetailCoFounderEarningByTrading.objects.filter(
                user=request.user 
            )
            cofounder_earnings_by_product = DetailCoFounderEarningByProducts.objects.filter(
                user=request.user
            )
            cofounder_earnings_withdrawals = Withdrawal.objects.filter(
                user=request.user,
                transaction_status__in=[0, 1],
                source_of_profit='CO_FOUNDER'
            )
            cofounder_earnings_reinvestments = ReInvestments.objects.filter(
                user=request.user,
                type_re_investment='Co-Founder'
            )
            
            if cofounder_earnings_by_trading:
                user_current_earnings += cofounder_earnings_by_trading.aggregate(Sum('earnings'))['earnings__sum']
            if cofounder_earnings_by_product:
                user_current_earnings += cofounder_earnings_by_product.aggregate(Sum('earnings'))['earnings__sum']
            if cofounder_earnings_withdrawals:
                user_current_earnings -= cofounder_earnings_withdrawals.aggregate(Sum('amount'))['amount__sum']
            if cofounder_earnings_reinvestments:
                user_current_earnings -= cofounder_earnings_reinvestments.aggregate(Sum('amount'))['amount__sum']
                
            if amount > user_current_earnings:
                return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'No tienes suficiente dinero para reinvertir'})
            else:
                return super().create(request, *args, **kwargs)

    # create get customize call 'available' to get the available amount to reinvest
    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        # capital_trading = get_capital_trading(request.user)

        # region trading

        user_balance_calculated = calculate_user_balance(request.user)
        print(user_balance_calculated)

        capital_trading = 0
        capital_trading = user_balance_calculated['trading']['balance']

        earnings_trading = user_balance_calculated['trading']['current_earnings']
        network_earnings = user_balance_calculated['trading']['current_network_earnings']

        user_approved_and_pending_withdrawals = Withdrawal.objects.filter(
            user=request.user,
            source_of_profit='TRADING',
            transaction_status__in=[0]  # Pending withdrawals only
        )

        if user_approved_and_pending_withdrawals:
            earnings_trading -= user_approved_and_pending_withdrawals.aggregate(Sum('amount'))['amount__sum']

        # Negative earnings value validation
        if earnings_trading < 0:
            network_earnings += earnings_trading  # The negative value in earnings_trading is substracted from network_earnings
            earnings_trading = 0

        if network_earnings < 0:
            network_earnings = 0

        total = earnings_trading + network_earnings  # + earnings_network
        # endregion

        # region cofounder

        cofounder_balance = user_balance_calculated['cofounder']['balance']
        cofounder_earnings_balance = user_balance_calculated['cofounder']['current_earnings']

        cofounder_earnings_withdrawals = Withdrawal.objects.filter(
            user=request.user,
            source_of_profit='CO_FOUNDER',
            transaction_status__in=[0]  # Pending
        )

        if cofounder_earnings_withdrawals:
            cofounder_earnings_balance -= cofounder_earnings_withdrawals.aggregate(Sum('amount'))['amount__sum']

        if cofounder_earnings_balance < 0:
            cofounder_earnings_balance = 0
        # endregion

        list = [
            ReInvestmentsAvailableSerializer({
                'plan': 'Trading',
                'capital': capital_trading,
                'earnings': earnings_trading,
                'network_earnings': network_earnings,
                'total': total
            }).data,
            ReInvestmentsAvailableSerializer({
                'plan': 'Co-Founder',
                'capital': cofounder_balance,
                'earnings': cofounder_earnings_balance,
                'network_earnings': 0,
                'total': cofounder_earnings_balance}).data
        ]
        return Response(list)


router = DefaultRouter()
router.register('api/transaction_type', TransactionTypeViewSet, basename='TransactionType')
router.register('api/transaction', TransactionViewSet, basename='Transaction')
router.register('api/withdrawal', WithdrawalViewSet, basename='Withdrawal')
router.register('api/co_founder/earnings/trading', CoFounderEarningByTradingView, basename='CoFounderEarningByTrading')
router.register('api/co_founder/earnings/products', CoFounderEarningByProductView, basename='CoFounderEarningByProduct')
router.register('api/re_investments', ReInvestmentsView, basename='ReInvestments')