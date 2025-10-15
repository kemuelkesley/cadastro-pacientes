from faker import Faker
import csv

# Para testes
fake = Faker('pt_BR')

def create_fake_users_csv(numer_fake):
    with open('users_fake.csv', 'w', newline='') as csvfile:
        fieldnames = ['nome', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for _ in range(numer_fake):
            writer.writerow({'nome': fake.name(), 'email': fake.email()})

        return 'users_fake.csv criado com sucesso!'

if __name__ == '__main__':
    print(create_fake_users_csv(10))       