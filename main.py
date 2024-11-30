import pandas as pd
import matplotlib.pyplot as plt

from registration_bureau import RegistrationBureau
from voter import Voter
from commission import Commission


def main():
    # Завантаження даних виборців і кандидатів
    voters_df = pd.read_excel('data/voters.xlsx')
    candidates_df = pd.read_excel('data/candidates.xlsx')
    voter_names_list = voters_df['Voters'].tolist()
    candidate_names_list = candidates_df['Candidates'].tolist()

    rb = RegistrationBureau(voter_names_list)

    commission = Commission(rb.get_all_voters(), candidate_names_list)

    print("Систему запущено")
    print(f"Знайдено {len(voter_names_list)} виборців")
    print(f"Знайдено {len(candidate_names_list)} кандидатів")

    while True:
        # ----------------------- Авторизація виборця -----------------------
        print('\nЗареєструйтесь, для цього введіть свій номер виборця')
        print(f'Всього зареєстровано {len(voter_names_list)} виборців')

        voters_num = input("Введіть номер виборця ")

        # Перевірка валідності введеного номера
        if str(voters_num).isdigit():
            voters_num = int(voters_num)
        else:
            raise ValueError("Ви неправильно ввели свій номер за списком")

        if not (1 <= voters_num <= len(voter_names_list)):
            raise ValueError(f"Номер виборця має бути від 1 до {len(voter_names_list)}")

        # Створюємо об'єкт виборця
        current_voter_id = rb.get_voter_id(voter_names_list[voters_num - 1])
        current_voter = Voter(current_voter_id)

        print('\nАвторизація успішна!\n')

        # ----------------------- Процес голосування -----------------------
        print('Список кандидатів:')
        for name in candidate_names_list:
            print(name)

        voters_choice = input("Введіть номер кандидата за якого будете голосувати ")

        # Перевірка валідності вибору кандидата
        if str(voters_choice).isdigit():
            voters_choice = int(voters_choice)
        else:
            raise ValueError("Ви неправильно ввели номер кандидата")

        if not (1 <= voters_choice <= len(candidate_names_list)):
            raise ValueError(f"Номер кандидата має бути від 1 до {len(candidate_names_list)}")

        # Генерування зашифрованого бюлетеня і підпису
        encrypted_ballot, ballot_sig, public_key = current_voter.generate_ballot(
            commission.public_comm_key,
            voters_choice
        )

        # Передача інформації комісії
        commission.count_vote(encrypted_ballot, ballot_sig, public_key)

        # ----------------------- Результати голосування -----------------------
        code = input("Введіть 1 якщо хочете продовжити, 2 якщо завершити голосування ")

        if str(code).isdigit():
            code = int(code)
        else:
            raise ValueError("Ви неправильно ввели код")

        if code == 1:
            continue
        elif code == 2:
            candidates_results, number_of_voted, counted_ballots = commission.get_results()

            # Візуалізуємо результати голосувань
            plt.figure(figsize=(10, 6))
            plt.bar(candidates_results['Name'], candidates_results['Votes_Count'])
            plt.title('Голоси кандидатів')
            plt.xlabel('Кандидати')
            plt.ylabel('Кількість голосів')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

            index_of_winner = candidates_results['Votes_Count'].idxmax()
            print("\nРезультати голосування")
            print(f"Найбільше голосів у {candidates_results.loc[index_of_winner, 'Name']}")
            print(f"Явка склала {number_of_voted} чол. або {number_of_voted / len(voter_names_list) * 100}%")

            print("\nЗараховані бюлетені")
            for voter_id, ballot_id in counted_ballots.items():
                print(f"ID виборця: {voter_id}; ID бюлетеня: {ballot_id}")

            exit()
        else:
            ValueError("Код повинен бути 1 або 2")




if __name__ == "__main__":
    main()
