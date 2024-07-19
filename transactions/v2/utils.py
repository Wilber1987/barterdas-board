from django.db.models import Sum, F
from decimal import Decimal
from barter_auth.models import BarterUser
from transactions.models import DetailCoFounderEarningByProducts, DetailCoFounderEarningByTrading, MonthlyTradingEarningsPerLeader, KitPlanNetWorkEarnings

def calculate_accumulative_earnings(user: BarterUser, year: int):
    # region HELPERS
    def _assignMonthLabel(data_list: list):
        month_label = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 
            7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        for data in data_list:
            data['label'] = month_label[data['month']]

    def _aggregateSum(data: list, group_by: str, sum: str):
        temp = []
        for rec in data:
            found = False
            for temp_rec in temp:
                found = temp_rec[group_by] == rec[group_by] 
                if found: 
                    temp_rec[sum] = temp_rec[sum] + rec[sum]
                    break
            if not found: temp.append(rec)
        return temp

    def _addZeroEarning(data:list):
        for index in range(1,13):
            found = False
            for rec in data:
                found = rec['month'] == index
                if found: break
            if not found: data.append({'month': index, 'value': Decimal('0.00')})
    # endregion

    # region Data structure
    cofounder = {'id': 'cofounder_earnings',
     'label': 'Ganancias Cofundador',
     'data': []}
    trading = {'id': 'trading_earnings',
        'label': 'Ganancias Trading',
        'data': []}
    kitplan = {'id': 'kitplan_earnings',
        'label': 'Ganancias Kit Plan',
     'data': []}
    # endregion

    # region COFOUNDER
    cofounder['data'] = list(DetailCoFounderEarningByTrading.objects.filter(
        user=user,
        co_founder_earning_by_trading__year=year
    ).values(
        month=F('co_founder_earning_by_trading__month'), 
    ).annotate(value=Sum('earnings')).union(DetailCoFounderEarningByProducts.objects.filter(
        user=user, 
        co_founder_earning_by_products__year=year
    ).values(
        month=F('co_founder_earning_by_products__month'),
    ).annotate(value=Sum('earnings'))))

    # Aggregate SUM for earning grouping by month
    cofounder['data'] = _aggregateSum(cofounder['data'], 'month', 'value')
    # endregion

    # region TRADING
    trading['data'] = list(MonthlyTradingEarningsPerLeader.objects.filter(
        user=user,
        monthly_trading_earnings__year=year
    ).values(
        month=F('monthly_trading_earnings__month'),
    ).annotate(value=Sum('earnings')))

    #TODO: TradingNetworkEarnings missing
    # endregion

    # region KIT PLAN
    kitplan['data'] = list(KitPlanNetWorkEarnings.objects.filter(
        unilevel_network__user=user,
        created_at__year=year
    ).values(
        month=F('created_at__month'),
    ).annotate(value=Sum('earnings')))
    # endregion

    # region Assign Zero Earnings
    _addZeroEarning(cofounder['data'])
    _addZeroEarning(trading['data'])
    _addZeroEarning(kitplan['data'])
    # endregion

    # region Assign Month label for each earning
    _assignMonthLabel(cofounder['data'])
    _assignMonthLabel(trading['data'])
    _assignMonthLabel(kitplan['data'])
    # endregion

    data = {'year': year, 'earnings': [cofounder, trading, kitplan] }

    return data