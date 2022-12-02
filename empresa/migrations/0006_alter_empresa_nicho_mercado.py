# Generated by Django 4.1.3 on 2022-12-01 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0005_alter_vagas_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresa',
            name='nicho_mercado',
            field=models.CharField(choices=[('M', 'Marketing'), ('N', 'Nutrição'), ('D', 'Design'), ('T', 'Tecnologia'), ('CC', 'Construção Cívil')], max_length=3),
        ),
    ]
