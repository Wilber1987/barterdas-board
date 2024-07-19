# Clases generadas din�micamente
from barter_backend.core.EntityClass import EntityClass
from barter_backend.core.EntityClass import FilterData
from barter_backend.model.EntityModel import (Barter_auth_unilevelnetwork,
                                              Transactions_tradingearnings,
                                              Transactions_tradingnetworkearnings,
                                              Transactions_reinvestments,
                                              Transactions_withdrawal,
                                              Transactions_transaction)


class Barter_auth_barteruser(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.last_login: str = None
        self.is_superuser: bool = None
        self.is_staff: bool = None
        self.is_active: bool = None
        self.date_joined: str = None
        self.is_co_founder: bool = None
        self.verified: bool = None
        self.leadership_pool_type_id: int = None
        self.referred_by_id: int = None
        self.can_fill_kyc: bool = None
        self.country: str = None
        self.zip_code: str = None
        self.password: str = None
        self.phone_number: str = None
        self.address: str = None
        self.username: str = None
        self.first_name: str = None
        self.last_name: str = None
        self.city: str = None
        self.referral_code: str = None
        self.profile_image: str = None
        self.email: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def getTradingEarnings(self):
        # Obtener ganancias de operaciones comerciales del usuario
        user_trading_earnings = Transactions_tradingearnings(
            user_id=self.id, enabled=True).Get()

        # Obtener reinversiones del usuario relacionadas con el comercio
        reinvestments = Transactions_reinvestments(
            user_id=self.id, type_re_investment="Trading").Get()

        # Obtener retiros aprobados y pendientes del usuario relacionados con el comercio
        user_approved_and_pending_withdrawals = Transactions_withdrawal(
            user_id=self.id, source_of_profit="TRADING").Where([
                FilterData("transaction_status", "in", [0, 1])
            ])

        # Calcular ganancias totales del usuario
        user_current_earnings = 0
        if user_trading_earnings.__len__ != 0:
            user_current_earnings += sum(map(lambda e: e.earnings,
                                             user_trading_earnings))

        # Obtener la red de usuarios asociada al usuario
        network = list(map(lambda n: n.id, Barter_auth_unilevelnetwork(
            user_id=self.id).Get()))

        # Obtener ganancias de red del usuario
        if len(network) != 0:
            user_network_earnings = Transactions_tradingnetworkearnings(enabled=True).Where([
                FilterData("unilevel_network_id", "in", network)
            ])

            if user_network_earnings.__len__ != 0:
                user_current_earnings += sum(map(lambda e: e.earnings,
                                                 user_network_earnings))

        # Restar reinversiones del total de ganancias
        if reinvestments.__len__ != 0:
            user_current_earnings -= sum(map(lambda e: e.amount,
                                             reinvestments))

        # Restar retiros aprobados y pendientes del total de ganancias
        if user_approved_and_pending_withdrawals.__len__ != 0:
            user_current_earnings -= sum(map(lambda e: e.amount,
                                             user_approved_and_pending_withdrawals))

        # Devolver ganancias totales del usuario
        return user_current_earnings
