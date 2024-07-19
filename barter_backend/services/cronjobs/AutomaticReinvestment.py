from datetime import datetime

from barter_backend.core.EntityClass import FilterData
from barter_backend.model.Barter_auth_barteruser import *
from barter_backend.model.EntityModel import (Transactions_reinvestments,
                                              Transactions_transaction)


class AutomaticReinvestment():
    def do(self):
        try:
            print(f"go to do--->")
            # Obtener IDs de usuarios con transacciones de comercio exitosas
            transactions = list(map(lambda n: n.user_id, Transactions_transaction(
                transaction_type="trading", transaction_status=1).Get()))

            # Si no hay transacciones, salir
            if len(transactions) == 0:
                return

            # Obtener información de usuarios con transacciones exitosas
            users = Barter_auth_barteruser().Where(
                [FilterData("id", "in", transactions)])

            # Iterar sobre usuarios
            for user in users:                
                # Obtener ganancias comerciales del usuario
                amount = user.getTradingEarnings()

                # Verificar si las ganancias son suficientes para reinvertir
                if amount >= 10:
                    # Imprimir información y realizar reinversión
                    print(f"Usuario: {user.id}, Ganancias: {amount}")
                    Transactions_reinvestments(
                        amount=amount,
                        created_at=datetime.now(),
                        type_re_investment="Trading",
                        user_id=user.id
                    ).Save()
                else:
                    print("No hay suficientes fondos para reinvertir")

            print(f"End go to do--->")

        except Exception as e:
            # Manejar excepciones e imprimir mensaje de error
            print(f"An exception occurred: {str(e)}")