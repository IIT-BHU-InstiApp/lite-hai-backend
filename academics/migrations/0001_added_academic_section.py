# Generated by Django 2.2.13 on 2021-12-11 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('academics', '0001_initial'), ('academics', '0002_auto_20211206_2130'), ('academics', '0003_auto_20211210_1744'),
                ('academics', '0004_auto_20211211_2054'), ('academics', '0005_auto_20211211_2057'), ('academics', '0006_auto_20211211_2108')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProffsAndHODs',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=60)),
                ('year_of_joining', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='AcademicSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('bce', 'Biochemical Engineering'), ('bme', 'Biomedical Engineering'), ('cer', 'Ceramic Engineering'), ('che', 'Chemical Engineering'), ('chy', 'Chemistry'), ('civ', 'Civil Engineering'), ('cse', 'Computer Science and Engineering'), ('ece', 'Electronics Engineering'), (
                    'eee', 'Electrical Engineering'), ('mat', 'Mathematics and Computing'), ('mec', 'Mechanical Engineering'), ('met', 'Metallurgical Engineering'), ('min', 'Mining Engineering'), ('mst', 'Materials Science and Technology'), ('phe', 'Pharmaceutical Engineering and Technology'), ('phy', 'Physics'), ('hss', 'Humanistic Studies')], max_length=60)),
                ('year_of_joining', models.CharField(max_length=10)),
                ('schedule_url', models.URLField()),
            ],
        ),
        migrations.AlterModelTable(
            name='proffsandhods',
            table='Proffs and HODs',
        ),
        migrations.AlterModelOptions(
            name='proffsandhods',
            options={'verbose_name': 'Proffs and HODs',
                     'verbose_name_plural': 'Proffs and HODs'},
        ),
        migrations.RemoveField(
            model_name='proffsandhods',
            name='year_of_joining',
        ),
        migrations.AddField(
            model_name='proffsandhods',
            name='proffs_and_HODs',
            field=models.URLField(default='https://www.iitbhu.ac.in/dept'),
        ),
        migrations.AlterModelTable(
            name='proffsandhods',
            table=None,
        ),
        migrations.RenameModel(
            old_name='ProffsAndHODs',
            new_name='ProfsAndHODs',
        ),
        migrations.AlterModelOptions(
            name='profsandhods',
            options={'verbose_name': 'Profs and HODs',
                     'verbose_name_plural': 'Profs and HODs'},
        ),
        migrations.RenameField(
            model_name='profsandhods',
            old_name='proffs_and_HODs',
            new_name='profs_and_HODs',
        ),
        migrations.CreateModel(
            name='StudyMaterials',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_url', models.URLField()),
                ('department', models.CharField(choices=[('bce', 'Biochemical Engineering'), ('bme', 'Biomedical Engineering'), ('cer', 'Ceramic Engineering'), ('che', 'Chemical Engineering'), ('chy', 'Chemistry'), ('civ', 'Civil Engineering'), ('cse', 'Computer Science and Engineering'), ('ece', 'Electronics Engineering'), ('eee', 'Electrical Engineering'), (
                    'mat', 'Mathematics and Computing'), ('mec', 'Mechanical Engineering'), ('met', 'Metallurgical Engineering'), ('min', 'Mining Engineering'), ('mst', 'Materials Science and Technology'), ('phe', 'Pharmaceutical Engineering and Technology'), ('phy', 'Physics'), ('hss', 'Humanistic Studies')], default='cse', max_length=60)),
            ],
            options={
                'verbose_name_plural': 'Study Materials',
            },
        ),
        migrations.AlterField(
            model_name='profsandhods',
            name='department',
            field=models.CharField(choices=[('bce', 'Biochemical Engineering'), ('bme', 'Biomedical Engineering'), ('cer', 'Ceramic Engineering'), ('che', 'Chemical Engineering'), ('chy', 'Chemistry'), ('civ', 'Civil Engineering'), ('cse', 'Computer Science and Engineering'), ('ece', 'Electronics Engineering'), ('eee', 'Electrical Engineering'), (
                'mat', 'Mathematics and Computing'), ('mec', 'Mechanical Engineering'), ('met', 'Metallurgical Engineering'), ('min', 'Mining Engineering'), ('mst', 'Materials Science and Technology'), ('phe', 'Pharmaceutical Engineering and Technology'), ('phy', 'Physics'), ('hss', 'Humanistic Studies')], max_length=60),
        ),
        migrations.AlterField(
            model_name='profsandhods',
            name='department',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='studymaterials',
            name='department',
            field=models.CharField(choices=[('bce', 'Biochemical Engineering'), ('bme', 'Biomedical Engineering'), ('cer', 'Ceramic Engineering'), ('che', 'Chemical Engineering'), ('chy', 'Chemistry'), ('civ', 'Civil Engineering'), ('cse', 'Computer Science and Engineering'), ('ece', 'Electronics Engineering'), ('eee', 'Electrical Engineering'), (
                'mat', 'Mathematics and Computing'), ('mec', 'Mechanical Engineering'), ('met', 'Metallurgical Engineering'), ('min', 'Mining Engineering'), ('mst', 'Materials Science and Technology'), ('phe', 'Pharmaceutical Engineering and Technology'), ('phy', 'Physics'), ('hss', 'Humanistic Studies')], max_length=60),
        ),
    ]
