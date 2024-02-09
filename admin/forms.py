from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User,Hostel,Room,RoomChange,Notice,Billing
from django.core.exceptions import ValidationError

class UserForm(UserCreationForm):
    ...
    # def __init__(self, *args, **kwargs):
    #     # self.user = kwargs.pop("user")
    #     super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "mobile_number",
            "address",
            "gender",
            "image",
        )


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        # exclude = ['UserID']
        # fields = "__all__"
        fields = ['name','note']

    def clean_name(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("name")
        if (
            username
            and self._meta.model.objects.filter(name__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "name": "Name Already taken"
                    }
                )
            )
        else:
            return username


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        # exclude = ['UserID']
        # fields = "__all__"
        fields = ['name','note','floor',"hostel"]

    def clean_name(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("name")
        if (
            username
            and self._meta.model.objects.filter(name__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "name": "Name Already taken"
                    }
                )
            )
        else:
            return username


class ChangeRoomForm(forms.ModelForm):
    class Meta:
        model = RoomChange
        # exclude = ['UserID']
        # fields = "__all__"
        fields = ['user','room']


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        # exclude = ['UserID']
        # fields = "__all__"
        fields = ['user','date','notice']
class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['user','date','amount','remark']