# Generated by Django 4.2.7 on 2023-12-28 12:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('celular', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='BR')),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('data_exclusao', models.DateTimeField(blank=True, null=True, verbose_name='Data de Exclusão')),
                ('usuario_criacao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contatos_criados', to=settings.AUTH_USER_MODEL, verbose_name='Quem criou?')),
                ('usuario_exclusao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contatos_excluidos', to=settings.AUTH_USER_MODEL, verbose_name='Quem excluiu?')),
            ],
        ),
    ]
