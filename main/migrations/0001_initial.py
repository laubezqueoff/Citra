# Generated by Django 3.1.2 on 2021-03-20 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('description', models.CharField(max_length=20)),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='users')),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(max_length=20)),
                ('password', models.TextField(max_length=20)),
                ('name', models.TextField(max_length=40)),
                ('phoneNumber', models.IntegerField()),
                ('email', models.TextField(max_length=30)),
                ('zipCode', models.IntegerField()),
                ('registerDate', models.DateField()),
                ('isBanned', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('picture', models.ImageField(upload_to='products')),
                ('description', models.TextField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PromotionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('schedule', models.TextField(max_length=50)),
                ('description', models.TextField(max_length=60)),
                ('picture', models.ImageField(upload_to='shops')),
                ('address', models.CharField(max_length=40)),
                ('durationBooking', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.owner')),
            ],
        ),
        migrations.CreateModel(
            name='ShopType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.owner')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shop')),
                ('subscriptionType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.subscriptiontype')),
            ],
        ),
        migrations.AddField(
            model_name='shop',
            name='shopType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shoptype'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(verbose_name=range(1, 5))),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=60)),
                ('date', models.DateField()),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.owner')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.product')),
                ('promotionType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.promotiontype')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shop')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='productType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.producttype'),
        ),
        migrations.AddField(
            model_name='product',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shop'),
        ),
        migrations.AddField(
            model_name='owner',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person'),
        ),
        migrations.CreateModel(
            name='ForumMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=60)),
                ('date', models.DateField()),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customuser')),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person'),
        ),
        migrations.CreateModel(
            name='CustomAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person')),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=60)),
                ('isSentByUser', models.BooleanField()),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.chat')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.shop'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.customuser'),
        ),
    ]
