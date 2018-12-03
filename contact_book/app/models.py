from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator


# potem zapytac tomka czy jest dopuszczalne tworzenie m2m w 2 grupach tak żeby jedna odwoływala sie do drugiej
# w sensie Group będzie miała kolumne people a Person będzie miało kolumne groups


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(
        'app.Person', verbose_name="Group members", blank=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    groups = models.ManyToManyField(
        'app.Group', verbose_name="Groups", blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


CHOICES = (
    (1, 'Home'),
    (2, 'Business')
)


class Email(models.Model):
    adress = models.EmailField(unique=True)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name="email adress")
    email_type = models.IntegerField(
        choices=CHOICES, verbose_name="email type")

    def __str__(self):
        return f"{self.adress}-{self.person.name} {self.person.surname}"


class Phone(models.Model):
    number = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(r'^\d{9}$|^\d{3} \d{3} \d{3}$',
                           'Invalid number pattern'),
        ], verbose_name="Phone number", unique=True)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name="Person")
    phone_type = models.IntegerField(
        choices=CHOICES, verbose_name="Phone type")

    def __str__(self):
        return f"{self.number}-{self.person.name} {self.person.surname}"
