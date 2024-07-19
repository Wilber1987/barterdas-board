import logging

from barter_auth.v2.utils import get_month_dates

from django.db.models import Sum, F

from barter_auth.models import (
    BarterUser,
    UnilevelNetwork,
    BarterPlan,
    BarterTradingPlan,
)
from global_settings.models import (
    KitPlanUnilevelPercentage,
    TradingUnilevelPercentage,
    KitPlan,
    CapsByDirectUsers,
)
from transactions.models import (
    Transaction,
    MonthlyTradingEarningsPerLeader,
    ReInvestments,
    KitPlanNetWorkEarnings,
    TradingNetWorkEarnings,
    MonthlyTradingEarnings,
    TradingEarnings,
)
from transactions.utils.user_balance_utils import get_count_users_direct

logger = logging.getLogger("django")


def get_renueve_co_founder(user: BarterUser):
    co_founder_earning = (
        user.co_founder_earning_by_trading.all().aggregate(Sum("earnings"))[
            "earnings__sum"
        ]
        - user.co_founder_earning_by_trading.all().aggregate(Sum("earnings_paid"))[
            "earnings_paid__sum"
        ]
        if user.co_founder_earning_by_trading.count() > 0
        else 0
    )

    co_founder_earning += (
        user.co_founder_earning_by_products.all().aggregate(Sum("earnings"))[
            "earnings__sum"
        ]
        - user.co_founder_earning_by_products.all().aggregate(Sum("earnings_paid"))[
            "earnings_paid__sum"
        ]
        if user.co_founder_earning_by_products.count() > 0
        else 0
    )
    return co_founder_earning


def get_capital_co_founder(user: BarterUser):
    result = user.transactions.filter(
        transaction_type=Transaction.TRANSACTION_TYPE[2][0],
        transaction_status=Transaction.TRANSACTION_STATUS[1][0],
    ).aggregate(Sum("amount"))["amount__sum"]
    result = result if result else 0
    result += (
        user.re_investments.filter(
            type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[1][0]
        ).aggregate(Sum("amount"))["amount__sum"]
        if user.re_investments.filter(
            type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[1][0]
        ).count()
        > 0
        else 0
    )
    return result


def get_capital_trading(user: BarterUser):
    result = user.transactions.filter(
        transaction_type=Transaction.TRANSACTION_TYPE[1][0],
        transaction_status=Transaction.TRANSACTION_STATUS[1][0],
    ).aggregate(Sum("amount"))["amount__sum"]
    result = result if result else 0
    result += (
        user.re_investments.filter(
            type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[0][0]
        ).aggregate(Sum("amount"))["amount__sum"]
        if user.re_investments.filter(
            type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[0][0]
        ).count()
        > 0
        else 0
    )
    return result


def get_renueve_trading_network(user: BarterUser):
    result = user.monthly_trading_earnings.filter(
        status=MonthlyTradingEarningsPerLeader.STATUS[0][0]
    ).aggregate(earnings__sum=Sum(F("earnings") - F("earnings_paid")))["earnings__sum"]
    return result if result else 0


def get_renueve_trading_personal(user: BarterUser):
    result = user.cumulative_revenues.all().aggregate(Sum("total_to_withdraw"))[
        "total_to_withdraw__sum"
    ]
    return result if result else 0


def get_renueve_trading_total(user: BarterUser):
    result = get_renueve_trading_personal(user) + get_renueve_trading_network(user)
    return result if result else 0


def generate_kitplan_unilevel_earnings(transaction: Transaction):
    user: BarterUser = transaction.user
    earning_levels: KitPlanUnilevelPercentage = (
        KitPlanUnilevelPercentage.objects.filter(enabled=True)
    )
    network: UnilevelNetwork = UnilevelNetwork.objects.filter(
        user_in_network=user, level__in=earning_levels.values("level")
    )

    dataset = [
        KitPlanNetWorkEarnings(
            unilevel_network=net,
            kit_plan_unilevel_network=earning_levels.filter(level=net.level).first(),
            level=net.level,
            level_earnings_percentage=earning_levels.filter(level=net.level)
            .first()
            .earnings_percentage,
            transaction=transaction,
            current_investment=transaction.amount,
            earnings=transaction.amount
            * earning_levels.filter(level=net.level).first().earnings_percentage,
            calculation_process=f"Kit Plan {transaction.amount} * {earning_levels.filter(level=net.level).first().earnings_percentage}({net.level})",
        )
        for net in network
    ]

    KitPlanNetWorkEarnings.objects.bulk_create(dataset)

    transaction.calculated_earnings = True
    transaction.save()
    print(
        f"Agregadas ganancias de red para la transaccion {transaction.id} {transaction}"
    )


def total_earnings_kitplan(user):
    current_earnings = KitPlanNetWorkEarnings.objects.filter(
        unilevel_network__user=user
    ).aggregate(Sum("earnings"))["earnings__sum"]
    current_earnings = float(current_earnings) if current_earnings else 0
    return current_earnings


def max_earnings_kitplan(user):
    max_earnings = user.plans.filter(
        transaction__transaction_status=Transaction.TRANSACTION_STATUS[1][0]
    ).aggregate(
        total_multiplication=Sum(F("transaction__amount") * F("plan__earnings_cap"))
    )[
        "total_multiplication"
    ]
    max_earnings = float(max_earnings) if max_earnings else 0
    return max_earnings


def mark_cap_plans_as_reached(user: BarterUser):
    plans = user.plans.filter(
        transaction__transaction_status=Transaction.TRANSACTION_STATUS[1][0]
    ).distinct()
    for plan in plans:
        plan.cap_reached = True
    BarterPlan.objects.bulk_update(plans, ["cap_reached"])


def mark_cap_trading_plans_as_reached(user: BarterUser):
    plans = user.bartertradingplan_set.filter(
        transaction__transaction_status=Transaction.TRANSACTION_STATUS[1][0]
    ).distinct()
    for plan in plans:
        plan.cap_reached = True
    BarterTradingPlan.objects.bulk_update(plans, ["cap_reached"])


def get_kit_plan_earning_available(user: BarterUser, earning):
    """
    Obtener la ganancia disponible para el usuario cuando se le paga por un kitplan de su red
    Considerando gananciasActuales, gananciaMaximaAPagar y gananciaAPagar, la función retorna la ganancia disponible
    Si gananciasActuales >= gananciaMaximaAPagar, entonces la función retorna 0
    Si gananciasActuales + gananciaAPagar >= gananciaMaximaAPagar, entonces la función retorna gananciaMaximaAPagar - gananciasActuales
    Si gananciasActuales + gananciaAPagar < gananciaMaximaAPagar, entonces la función retorna gananciaAPagar
    @param user: usuario al que se le pagará
    @param earning: ganancia a pagar
    @return: ganancia disponible
    """
    print(f"Verificando si {user} puede obtener más ganancias del plan con {earning}")
    # si el usuario es raíz, no validar
    if user.root_barter_user.count() > 0:
        print(f"El usuario {user} es raíz, no se validará")
        return earning

    # calculando la capacidad máxima que el usuario puede obtener de los planes verificados
    max_earnings = max_earnings_kitplan(user)

    # calculando las ganancias que ya ha obtenido el usuario
    current_earnings = total_earnings_kitplan(user)

    print(
        f"Ganancias actuales de kitplan {user} {current_earnings}: maximo: {max_earnings}"
    )

    # si las ganancias actuales son mayores o iguales a las ganancias máximas, no se puede obtener más ganancias
    if current_earnings >= max_earnings:
        print(f"El usuario {user} ya no puede obtener más ganancias")
        mark_cap_plans_as_reached(user)
        return 0
    # si las ganancias actuales más las ganancias a pagar son mayores o iguales a las ganancias máximas
    # se puede obtener la diferencia
    elif current_earnings + earning >= max_earnings:
        print(
            f"El usuario {user} puede obtener {max_earnings - current_earnings} de ganancias"
        )
        return max_earnings - current_earnings
    # si las ganancias actuales más las ganancias a pagar son menores a las ganancias máximas,
    # se puede obtener las ganancias a pagar
    else:
        print(f"El usuario {user} puede obtener {earning} de ganancias")
        return earning


def mark_as_calculated(transaction):
    if not transaction.calculated_earnings:
        transaction.calculated_earnings = True
        transaction.save()
        print(f"La transacción {transaction} ya fue procesada")


def verify_cap_by_direct_users(user: BarterUser, level: int):
    """
    Verificar si el usuario ya no puede obtener más ganancias por el cap de usuarios directos
    @param user:  usuario a verificar
    @param level:  nivel a verificar
    @return:  True si puede obtener más ganancias, False en caso contrario
    """
    count = get_count_users_direct(user)
    level = CapsByDirectUsers.objects.filter(level_to_win=level).first()
    if level is None:
        return False
    return count >= level.count_of_direct_users


def create_kit_plan_earning_through_transactions(
    transaction: Transaction, network: UnilevelNetwork
):
    if KitPlanNetWorkEarnings.objects.filter(
        transaction=transaction, unilevel_network=network
    ).exists():
        print(
            f"El detalle de plan de ganancia para la transacción {transaction} ya existe en {network}"
        )
        mark_as_calculated(transaction)
        return
    # para obtener el nivel de ganancia, se debió crear el registro en BarterPlan, conteniendo el KitPlan seleccionado
    # en caso de no existir, no se debe hacer nada
    if transaction.kit_plans.first() is None:
        print(f"La transacción {transaction} no tiene un Kit Plan asociado")
        mark_as_calculated(transaction)
        return
    # obtener el kit_plan seleccionado
    kit_plan: KitPlan = (
        network.user.plans.order_by("-plan__price").first().plan
        if network.user.plans.count() > 0
        else None
    )
    if kit_plan is None:
        print(f"El usuario {network.user} no tiene un Kit Plan seleccionado")
        mark_as_calculated(transaction)
        return

    # por regla de negocio, si no se encuentra el nivel, no hacer nada
    level_object = KitPlanUnilevelPercentage.objects.filter(
        level=network.level, kit_plan=kit_plan, enabled=True
    ).first()

    if level_object is None:
        print(f"No existe porcentaje habilitado para el Nivel {network.level}")
        mark_as_calculated(transaction)
        return

    # por regla de negocio, si por cierta cantidad de usuarios en la red activos, no se puede aplicar la ganancia
    # no hacer nada
    if not verify_cap_by_direct_users(network.user, network.level):
        print(
            f"El usuario {network.user} ya no puede obtener más ganancias [Cap de usuarios directos]"
        )
        mark_as_calculated(transaction)
        return

    percentage = level_object.earnings_percentage
    # calcular la ganancia
    earning = float(transaction.amount) * float(percentage)

    # antes de agregar el detalle, verificar si puede seguir obteniendo ganancias (verificar por el cap de ganancias)
    # si no puede seguir obteniendo ganancias, no hacer nada

    earning = get_kit_plan_earning_available(network.user, earning)
    if earning == 0:
        print(f"El usuario {network.user} ya no puede obtener más ganancias")
        mark_as_calculated(transaction)
        return

    # agregar texto que describa el proceso de calculo
    description = f"Kit Plan ${transaction.amount} * {round(percentage * 100, 2)}% (Nivel {level_object.level}) = Ganancia de ${earning}"

    # insertar en el detalle
    KitPlanNetWorkEarnings.objects.create(
        unilevel_network=network,
        transaction=transaction,
        kit_plan_unilevel_network=level_object,
        level=network.level,
        level_earnings_percentage=percentage,
        current_investment=transaction.amount,
        earnings=earning,
        calculation_process=description,
    )

    transaction.calculated_earnings = True
    transaction.save()


def get_max_trading_earnings(user: BarterUser):
    # calculando la capacidad máxima que el usuario puede obtener de sus planes de trading verificados
    max_earnings = BarterTradingPlan.objects.filter(
        user=user, transaction__transaction_status=Transaction.TRANSACTION_STATUS[1][0]
    ).aggregate(total_multiplication=Sum(F("transaction__amount") * F("plan__cap")))[
        "total_multiplication"
    ]
    max_earnings = float(max_earnings) if max_earnings else 0

    return max_earnings


def get_current_trading_earnings(user: BarterUser):
    # calculando las ganancias que ya ha obtenido el usuario
    current_earnings = TradingEarnings.objects.filter(user=user).aggregate(
        Sum("earnings")
    )["earnings__sum"]
    current_earnings = float(current_earnings) if current_earnings else 0

    current_network_earnings = TradingNetWorkEarnings.objects.filter(
        unilevel_network__user=user
    ).aggregate(Sum("earnings"))["earnings__sum"]
    current_network_earnings = (
        float(current_network_earnings) if current_network_earnings else 0
    )

    return current_earnings + current_network_earnings


def create_trading_earning_through_monthly_percentage_with_network(
    trading_earning: TradingEarnings,
):
    # obtener el nivel de la red
    if trading_earning.calculated_earnings:
        logger.warning(
            f"La ganancia de red de trading por {trading_earning} ya fue procesada"
        )
        return []

    networks = trading_earning.user.unilevel_network_in.all()
    # TODO: replace with user balance when its done
    networks = networks.filter(
        user__transactions__transaction_type="trading",
        user__transactions__transaction_status=1,
    ).all()

    if networks is None or networks.count() == 0:
        logger.warning(f"No existe una red para el usuario {trading_earning.user}")
        return []
    to_create = []
    for network in networks:
        level_object = TradingUnilevelPercentage.objects.filter(
            level=network.level, enabled=True
        ).first()
        if level_object is None:
            logger.warning(
                f"No existe porcentaje habilitado para el Nivel {network.level}"
            )
            continue
        percentage = level_object.earnings_percentage
        earning = float(trading_earning.earnings) * float(percentage)
        description = f"Ganancia Diaria ${trading_earning.earnings} * {round(percentage * 100, 2)}% (Nivel {level_object.level}) = Ganancia de ${earning}"
        to_create.append(
            TradingNetWorkEarnings(
                unilevel_network=network,
                trading_unilevel_network=level_object,
                trading_earnings=trading_earning,
                level=network.level,
                level_earnings_percentage=percentage,
                trading_percentage=trading_earning.trading_percentage,
                current_investment=trading_earning.earnings,
                earnings=earning,
                calculation_process=description,
            )
        )
    return to_create


def create_trading_earning_through_monthly_percentage_by_transaction(
    monthly_trading: MonthlyTradingEarnings, transaction: Transaction
):
    date_first_day, date_last_day, last_day = get_month_dates(
        monthly_trading.month, monthly_trading.year
    )
    days = last_day
    if (
        transaction.transaction_type != Transaction.TRANSACTION_TYPE[1][0]
        or transaction.transaction_status != Transaction.TRANSACTION_STATUS[1][0]
        or transaction.wallet_deposit_date > date_last_day
    ):
        return None

    # si existe un TradingEarnings para esta transacción y este porcentaje de trading, no hacer nada
    if TradingEarnings.objects.filter(
        transaction=transaction, trading_percentage=monthly_trading
    ).exists():
        logger.warning(
            f"El detalle de plan de ganancia para la transacción {transaction} ya existe en {monthly_trading}"
        )
        if not transaction.calculated_earnings:
            transaction.calculated_earnings = True
            transaction.save()
        return None

    # obtener el porcentaje de ganancia a aplicar
    # si la transacción se hizo en este mes, se debe de calcular un porcentaje proporcional
    if date_first_day <= transaction.wallet_deposit_date <= date_last_day:
        days = (transaction.wallet_deposit_date - date_first_day).days + 1
        percentage = float(monthly_trading.roi) * float((last_day - days) / last_day)
    else:
        percentage = float(monthly_trading.roi)

    return TradingEarnings(
        user=transaction.user,
        trading_percentage=monthly_trading,
        trading_percentage_used=percentage,
        transaction=transaction,
        current_investment=transaction.amount,
        earnings=float(transaction.amount) * percentage,
        calculation_process=f"Dias de inversión: {last_day - days} / {last_day} = {round((last_day - days) / last_day * 100, 2)}%",
    )


def create_trading_earning_through_monthly_percentage_by_re_investment(
    monthly_trading: MonthlyTradingEarnings, re_investment: ReInvestments
):
    date_first_day, date_last_day, last_day = get_month_dates(
        monthly_trading.month, monthly_trading.year
    )
    days = last_day

    # si existe un TradingEarnings para esta reinversión y este porcentaje de trading, no hacer nada
    if TradingEarnings.objects.filter(
        reinvestment=re_investment, trading_percentage=monthly_trading
    ).exists():
        logger.warning(
            f"El detalle de plan de ganancia para la reinversión {re_investment} ya existe en {monthly_trading}"
        )
        return None

    # obtener el porcentaje de ganancia a aplicar
    # si la transacción se hizo en este mes, se debe de calcular un porcentaje proporcional
    percentage_to_show = 1
    if date_first_day <= re_investment.created_at <= date_last_day:
        days = (re_investment.created_at - date_first_day).days + 1
        percentage_to_show = float((last_day - days) / last_day)
        percentage = float(monthly_trading.roi) * percentage_to_show
    else:
        percentage = float(monthly_trading.roi)

    return TradingEarnings(
        user=re_investment.user,
        trading_percentage=monthly_trading,
        trading_percentage_used=percentage,
        reinvestment=re_investment,
        current_investment=re_investment.amount,
        earnings=float(re_investment.amount) * percentage,
        calculation_process=f"Dias de inversión: {(last_day - days) if days != last_day else last_day}"
        f" / {last_day} = {round(percentage_to_show * 100, 2)}%",
    )


def create_trading_earning_through_monthly_percentage(
    monthly_trading: MonthlyTradingEarnings,
):
    date_first_day, date_last_day, last_day = get_month_dates(
        monthly_trading.month, monthly_trading.year
    )

    # Get transactions with date before the cut-off date.
    transactions = Transaction.objects.filter(
        transaction_type=Transaction.TRANSACTION_TYPE[1][0],
        transaction_status=Transaction.TRANSACTION_STATUS[1][0],
        wallet_deposit_date__lte=date_last_day,
    )

    re_investments = ReInvestments.objects.filter(
        type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[0][0],
        created_at__lte=date_last_day,
    )

    to_create = []

    # Call create_trading_earning_through_monthly_percentage for each transaction and save on list
    for transaction in transactions:  # crear reporte por transacción
        object_to_create = (
            create_trading_earning_through_monthly_percentage_by_transaction(
                monthly_trading, transaction
            )
        )
        to_create.append(object_to_create)  # Personal trading earnings

    for re_investment in re_investments:  # crear reporte por reinversión
        object_to_create = (
            create_trading_earning_through_monthly_percentage_by_re_investment(
                monthly_trading, re_investment
            )
        )
        to_create.append(object_to_create)  # Personal trading earnings

    # eliminar los registros que sean None
    to_create = list(filter(lambda x: x is not None, to_create))
    # validar que las ganancias no sobrepasen a la capacidad máxima del usuario
    users = set(map(lambda x: x.user, to_create))
    user_with_max_earnings = {}
    for user in users:
        user_with_max_earnings[user.id] = {
            "max_earnings": get_max_trading_earnings(user),
            "earnings": get_current_trading_earnings(user),
        }

    # eliminar los reportes que sobrepasen la capacidad máxima del usuario
    for earning in to_create:
        # si el usuario es raíz, no se valida
        if earning.user.root_barter_user.count() > 0:
            continue
        total_earnings = user_with_max_earnings[earning.user.id]["earnings"]
        # si las ganancias totales son mayores a la capacidad máxima, se elimina el registro
        if total_earnings >= user_with_max_earnings[earning.user.id]["max_earnings"]:
            to_create.remove(earning)
            continue
        # si las ganancias totales más las ganancias de la transacción son mayores a
        # la capacidad máxima, se ajusta el valor de las ganancias
        elif (
            total_earnings + float(earning.earnings)
            >= user_with_max_earnings[earning.user.id]["max_earnings"]
        ):
            earning.earnings = (
                user_with_max_earnings[earning.user.id]["max_earnings"] - total_earnings
            )
            earning.calculation_process += " - Se ajustó el valor de las ganancias"

        # se actualiza el valor de las ganancias totales del usuario
        user_with_max_earnings[earning.user.id]["earnings"] += float(earning.earnings)

    TradingEarnings.objects.bulk_create(to_create)

    # una vez que se han creado los reportes de ganancias personales, se crean los reportes de ganancias de red
    to_create_network = []
    # se recorren los reportes de ganancias personales
    for earning in to_create:
        to_create_network += (
            create_trading_earning_through_monthly_percentage_with_network(earning)
        )

    # validar que las ganancias no sobrepasen a la capacidad máxima del usuario
    users = set(map(lambda x: x.unilevel_network.user, to_create_network))
    user_with_max_earnings = {}
    for user in users:
        user_with_max_earnings[user.id] = {
            "max_earnings": get_max_trading_earnings(user),
            "earnings": get_current_trading_earnings(user),
        }

    for earning in to_create_network:
        if earning.unilevel_network.user.root_barter_user.count() > 0:
            continue
        total_earnings = user_with_max_earnings[earning.unilevel_network.user.id][
            "earnings"
        ]
        # si las ganancias totales son mayores a la capacidad máxima, se elimina el registro
        if (
            total_earnings
            >= user_with_max_earnings[earning.unilevel_network.user.id]["max_earnings"]
        ):
            to_create_network.remove(earning)
            # marcar al usuario como que ya no puede recibir más ganancias
            mark_cap_trading_plans_as_reached(earning.unilevel_network.user)
            continue
        # si las ganancias totales más las ganancias de la transacción son mayores a
        # la capacidad máxima, se ajusta el valor de las ganancias
        elif (
            total_earnings + float(earning.earnings)
            >= user_with_max_earnings[earning.unilevel_network.user.id]["max_earnings"]
        ):
            earning.earnings = (
                user_with_max_earnings[earning.unilevel_network.user.id]["max_earnings"]
                - total_earnings
            )
            earning.calculation_process += " - Se ajustó el valor de las ganancias"

        # se actualiza el valor de las ganancias totales del usuario
        user_with_max_earnings[earning.unilevel_network.user.id]["earnings"] += float(
            earning.earnings
        )

    TradingNetWorkEarnings.objects.bulk_create(to_create_network)

    # Set calculated_earnings field of TradingEarnings to True when the operations is successful.
    to_create = list(
        map(lambda x: setattr(x, "calculated_earnings", True) or x, to_create)
    )
    TradingEarnings.objects.bulk_update(to_create, ["calculated_earnings"])
