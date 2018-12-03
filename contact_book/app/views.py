from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import Group, Person, Email, Phone, CHOICES
from .forms import CreatePersonForm


class Home(View):
    def get(self, request):
        people = Person.objects.all()
        return render(request, 'home.html', {
            'title': 'Homepage',
            'people': people,
        })

# jeden kontakt


class PersonInfo(View):
    def get(self, request, id):
        person = Person.objects.get(pk=id)
        phones = Phone.objects.filter(person=person)
        emails = Email.objects.filter(person=person)
        person_groups = Group.objects.filter(person=person)
        return render(request, 'personinfo.html', {
            'person': person,
            'phones': phones,
            'emails': emails,
            'person_groups': person_groups
        })


# jeden kontakt
def modify_person(request, id, msg=''):

    if request.method == 'GET':

        # sprawdzanie czy nie ma żadnych parametrów w urlu
        if request.GET.get('msg'):
            if request.GET['msg'] == 'group_removed':
                msg = 'Group has been removed'
            elif request.GET['msg'] == 'number_removed':
                msg = 'Number has been removed'
            elif request.GET['msg'] == 'email_removed':
                msg = 'Email has been removed'
    else:
        # edycja imienia i nazwiska
        person = Person.objects.get(pk=id)
        if request.POST.get('modfify') == 'Update':
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            if name and surname:
                person.name = name
                person.surname = surname
                person.save()
            msg = "Profile has been updated!"
        # dodawanie nowej grupy
        elif request.POST.get('modify') == 'Add group':
            group_id = request.POST.get('new_group')
            if group_id:
                group = Group.objects.get(id=int(group_id))
                person.groups.add(group)
                group = Group.objects.get(pk=group_id)
                group.members.add(person)
                person.save()
                group.save()

                msg = 'Group has been added!'
        # dodawanie nowego numeru
        elif request.POST.get('modify') == 'Add Phone':
            # sprawdzenie czy taki numer juz istnieje
            number = request.POST.get('add_number')
            try:
                Phone.objects.get(number=number)
                exist = True
            except:
                exist = False
            number_type = request.POST.get('number_type')
            if not exist:
                if number and number_type:
                    number = Phone.objects.create(
                        number=number,
                        phone_type=number_type,
                        person=person
                    )
                    msg = 'Phone number has been added!'
            else:
                msg = 'This phone number already exists!'
        # dodawanie nowego maila
        elif request.POST.get('modify') == 'Add Email':
            email_adress = request.POST.get('add_email')
            # sprawdzanie czy juz nie istanieje taki adres
            try:
                Email.objects.get(adress=email_adress)
                exist = True
            except:
                exist = False
            email_type = request.POST.get('email_type')

            if not exist:
                if email_adress and email_type:
                    email = Email.objects.create(
                        adress=email_adress,
                        email_type=email_type,
                        person=person
                    )
                    msg = 'Email has been added!'
            else:
                msg = 'This email adress already exists!'

    person = Person.objects.get(pk=id)
    person_groups = Group.objects.filter(person=person)
    phones = Phone.objects.filter(person=person)
    emails = Email.objects.filter(person=person)
    groups = Group.objects.all()
    types = CHOICES
    return render(request, 'modifyperson.html', {
        'person': person,
        'groups': groups,
        'person_groups': person_groups,
        'emails': emails,
        'phones': phones,
        'types': types,
        'msg': msg
    })


#  grupy


class Groups(View):
    def get(self, request, msg=''):
        if request.GET.get('msg'):
            msg = 'Group has been succesfully deleted'
        groups = Group.objects.all()
        return render(request, 'groups.html', {
            'groups': groups,
            'msg': msg
        })


# jedna grupa
class GroupInfo(View):
    def get(self, request, id):
        group = Group.objects.get(pk=id)
        members = Person.objects.filter(group=group)
        return render(request, 'groupinfo.html', {
            'group': group,
            'members': members
        })


# usuwanie

def delete_person(request, id):
    person = Person.objects.get(pk=id)
    person.delete()
    return redirect(reverse('home'))


def delete_group(request, id):
    group = Group.objects.get(pk=id)
    group.delete()
    return redirect('/groups/?msg=group_removed')


def delete_person_group(request, person_id, group_id):
    person = Person.objects.get(pk=person_id)
    group = Group.objects.get(pk=group_id)
    person.groups.remove(group)

    return redirect('/modify/{}/?msg=group_removed'.format(person_id))


def delete_email(request, person_id, email_id):
    person = Person.objects.get(pk=person_id)
    email = Email.objects.get(pk=email_id)
    email.delete()

    return redirect('/modify/{}/?msg=email_removed'.format(person_id))


def delete_phone(request, person_id, number_id):
    person = Person.objects.get(pk=person_id)
    number = Phone.objects.get(pk=int(number_id))
    number.delete()

    return redirect('/modify/{}/?msg=number_removed'.format(person_id))


# dodawanie

class AddContact(View):
    def get(self, request, msg=''):
        form = CreatePersonForm()
        return render(request, 'add_contact.html', {
            'form': form,
            'msg': msg
        })

    def post(self, request):
        form = CreatePersonForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            phone_number = form.cleaned_data['phone_num']
            phone_type = form.cleaned_data['phone_type']
            email = form.cleaned_data['email']
            email_type = form.cleaned_data['email_type']

            person = Person.objects.create(
                name=name,
                surname=surname
            )

            Phone.objects.create(
                person=person,
                number=phone_number,
                phone_type=phone_type
            )

            Email.objects.create(
                person=person,
                adress=email,
                email_type=email_type,
            )
            msg = 'New Contact has been created !'
        else:
            msg = 'Invalid data try again.'
        return self.get(request, msg)


class AddGroup(View):
    def get(self, request, msg=''):
        return render(request, 'add_group.html', {
            'msg': msg
        })

    def post(self, request):
        name = request.POST.get('name')

        if name:
            try:
                Group.objects.get(name=name)
                exist = True
            except:
                exist = False

            if exist:
                msg = 'Group already exist!'
            else:
                Group.objects.create(
                    name=name
                )
                msg = 'Created group {}'.format(name)
        else:
            msg = 'You have to fill the field!'
        return self.get(request, msg)
