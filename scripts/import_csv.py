from barter_auth.models import BarterUser, Referral
import csv

def run():
    with open("importar_test_normal.csv", "r") as data_list:
        reader = csv.DictReader(data_list, delimiter=';')
        inserted = 0

        for data in reader:
            try:
                if BarterUser.objects.filter(email=data["email"]).first() is not None:
                    with open("log.txt", "a") as log_file:
                        log_file.write(f"{data['email']} could not be inserted, an user with the same email already exists\n")

                leader = BarterUser.objects.get(referral_code=data["referral_code"])

                if leader is not None:
                    new_user = BarterUser()
                    attrs = vars(new_user)
                    print(', '.join("%s: %s" % item for item in attrs.items()))
                    new_user.email = data["email"]
                    new_user.username = data["email"]
                    new_user.set_password(data["password"])
                    new_user.phone_number = data["phone_number"]
                    new_user.first_name = data["name"]
                    new_user.save()

                    new_referral = Referral()
                    new_referral.user = new_user
                    new_referral.investment = leader
                    new_referral.transaction_hash = data["hash"]
                    new_referral.amount = data["investment"]
                    new_referral.category = "common"
                    new_referral.save()

                    inserted += 1
                else:
                    with open("log.txt", "a") as log_file:
                        log_file.write(f"{data['email']} could not be inserted, no leader exist with the referral code: {data['referral_code']}\n")
            except Exception as e:
                with open("log.txt", "a") as log_file:
                        log_file.write(f"{data['email']} could not be inserted, exception: {e}\n")
            print(f"Inserted: {inserted}")