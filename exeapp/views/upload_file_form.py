from django import forms
from exeapp.models import Package, User
import tempfile


class UploadFileForm(forms.Form):
    title = "Upload File"
    file = forms.FileField()


def upload_temp_zip(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # handle_uploaded_file(request.FILES['file'])
        if form.is_valid():
            if handle_uploaded_file(request.FILES['file'], request.user.username):
                return True
            else:
                return False
    else:
        return False


def handle_uploaded_file(f, user_name):
    temp_zip = tempfile.NamedTemporaryFile(mode='w+b', suffix='.zip', prefix='', delete=False)
    for chunk in f.chunks():
        temp_zip.write(chunk)
    print(temp_zip.name)
    p = Package.objects.import_package(f, User.objects.get(username=user_name))
    if p:
        return True
    else:
        return False