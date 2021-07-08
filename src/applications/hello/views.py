from datetime import datetime

from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import View

from applications.hello.models import HelloModel
from project.utils.night_mode import set_night_mode, get_theme
from project.utils import user_utils as uu, paths as paths, instances as instances
from project.utils.stats_utils import increment_visit
from project.utils.user_utils import create_user


class HelloForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    age = forms.IntegerField(required=False)


@increment_visit
class HelloView(FormView):

    template_name = paths.HELLO_HTML
    form_class = HelloForm

    def get_success_url(self):
        return instances.ENDPOINT_REDIRECTS[self.request.path]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.session.get(instances.NAME_key)
        age = self.request.session.get(instances.AGE_key)
        year = None
        if age is not None:
            year = datetime.now().year - int(age)

        user_session = {instances.NAME_key: name,
                        instances.YEAR_key: year}
        theme = get_theme(self.request)
        context.update({**user_session, **theme})
        return context

    # @csrf_exempt
    def form_valid(self, form):
        name = form.cleaned_data[instances.NAME_key]
        age = form.cleaned_data[instances.AGE_key]

        create_user(name, age)

        self.request.session[instances.NAME_key] = name
        self.request.session[instances.AGE_key] = age

        # uu.write_user_session(form.cleaned_data, self.request.session.session_key)
        return super().form_valid(form)


class NightModeView(View):
    @csrf_exempt
    def post(self, request):
        return set_night_mode(request, instances.ENDPOINT_REDIRECTS[request.path])
