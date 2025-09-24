from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils import timezone
from faker import Faker
import random

from apps.accounts.models import Persona, Personal

fake = Faker("es_ES")

class Command(BaseCommand):
    help = "Generar usuarios masivos para SmartCondominio"

    def add_arguments(self, parser):
        parser.add_argument("--total", type=int, default=5000, help="Número de usuarios a generar")

    def handle(self, *args, **options):
        total = options["total"]

        # Crear roles si no existen
        roles = {
            "Administrador": Group.objects.get_or_create(name="Administrador")[0],
            "Residente": Group.objects.get_or_create(name="Residente")[0],
            "Staff": Group.objects.get_or_create(name="Staff")[0],
        }

        self.stdout.write(f"🚀 Creando {total} usuarios de prueba...")

        for i in range(total):
            username = f"user{i+1}"
            email = f"user{i+1}@condominio.com"
            password = "123456789"

            user = User.objects.create_user(username=username, email=email, password=password)

            # 70% residentes, 30% staff
            if random.random() < 0.7:
                user.groups.add(roles["Residente"])
                persona = Persona.objects.create(
                    user=user,
                    ci=fake.unique.random_number(digits=7),
                    nombres=fake.first_name(),
                    apellidos=fake.last_name(),
                    telefono=fake.phone_number(),
                    fecha_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=70),
                    tipo=random.choice([
                        Persona.Tipo.PADRE,
                        Persona.Tipo.MADRE,
                        Persona.Tipo.HIJO,
                        Persona.Tipo.CONYUGE,
                        Persona.Tipo.OTRO
                    ]),
                )
                # 10% chance de asignar jefe
                if i > 10 and random.random() < 0.1:
                    jefe = Persona.objects.order_by("?").first()
                    if jefe and jefe != persona:
                        persona.jefe = jefe
                        persona.save()

            else:
                user.groups.add(roles["Staff"])
                Personal.objects.create(
                    user=user,
                    nombre=fake.first_name(),
                    apellidos=fake.last_name(),
                    cargo=random.choice(["Seguridad", "Limpieza", "Mantenimiento"]),
                    sueldo=round(random.uniform(2000, 5000), 2),
                    fecha_contratacion=timezone.now().date(),
                    tipo=random.choice([
                        Personal.Tipo.SEGURIDAD,
                        Personal.Tipo.LIMPIEZA,
                        Personal.Tipo.MANTENIMIENTO
                    ]),
                )

            if (i+1) % 500 == 0:
                self.stdout.write(f"➡️ {i+1}/{total} usuarios creados")

        self.stdout.write(self.style.SUCCESS(f"✅ {total} usuarios generados con éxito"))
