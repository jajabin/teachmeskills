import logging

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView, FormView

from applications.stats.views import increment_page_visit
from project.utils.night_mode import set_night_mode, get_theme
from project.utils import project_utils as pu, user_utils as uu, file_utils as fu, json_utils as ju, paths as paths, \
    responds as responds, errors as errors, instances as instances


class CVView(TemplateView):
    def get(self, request) -> HttpResponse:
        increment_page_visit(request.path)

        page_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)
        context = {**theme, **page_content}

        return render(self.request, paths.CV_HTML, context)


class JobView(TemplateView):
    def get(self, request) -> HttpResponse:
        increment_page_visit(request.path)

        page_content = ju.read_json_file(paths.CV_JOB_JSON)
        resume_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)
        context = {**theme, **page_content, **resume_content}

        return render(self.request, paths.CV_JOB_HTML, context)


class EducationView(TemplateView):
    def get(self, request) -> HttpResponse:
        increment_page_visit(request.path)

        page_content = ju.read_json_file(paths.CV_EDUCATION_JSON)
        resume_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)
        context = {**theme, **page_content, **resume_content}

        return render(self.request, paths.CV_EDUCATION_HTML, context)


class SkillsView(TemplateView):
    def get(self, request) -> HttpResponse:
        increment_page_visit(request.path)

        page_content = ju.read_json_file(paths.CV_SKILLS_JSON)
        resume_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)
        context = {**theme, **page_content, **resume_content}

        return render(self.request, paths.CV_SKILLS_HTML, context)


class ProjectsView(FormView):
    template_name = paths.CV_PROJECTS_HTML

    def get_context_data(self, **kwargs):
        increment_page_visit(self.request.path)

        page_content = ju.read_json_file(paths.CV_PROJECTS_JSON)
        projects = pu.get_projects(page_content)
        resume_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)

        context = {**theme,
                   **page_content,
                   **resume_content,
                   "projects": projects}

        return context


class ProjectForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    date = forms.CharField(required=False)
    description = forms.CharField(max_length=500, required=False)


class AddProjectView(FormView):
    template_name = paths.CV_PROJECTS_ADDITING_HTML
    form_class = ProjectForm

    def get_success_url(self):
        return "/cv/projects"

    def get_context_data(self, **kwargs):
        increment_page_visit(self.request.path)

        resume_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)

        context = super().get_context_data(**kwargs)
        context.update({**theme, **resume_content})

        return context

    # @csrf_exempt
    def form_valid(self, form):
        pu.add_project(paths.CV_PROJECTS_JSON, form.cleaned_data)
        return super().form_valid(form)


class SingleProjectView(TemplateView):

    def get(self, request, project_id):
        increment_page_visit(self.request.path)

        page_content = ju.read_json_file(paths.CV_PROJECTS_JSON)
        project = pu.build_project(page_content, project_id)
        resume_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)

        context = {**theme,
                   **page_content,
                   **resume_content,
                   "project": project}

        return render(self.request, paths.CV_PROJECT_HTML, context)

    # @csrf_exempt
    def post(self, request, project_id):
        pu.remove_project(paths.CV_PROJECTS_JSON, project_id)
        return HttpResponseRedirect("/cv/projects/")


class EditProjectView(FormView):
    template_name = paths.CV_PROJECT_EDITING_HTML
    form_class = ProjectForm

    def get_success_url(self, **kwargs):
        return "/cv/project/" + self.kwargs["project_id"]

    def get_context_data(self, **kwargs):
        increment_page_visit(self.request.path)

        page_content = ju.read_json_file(paths.CV_PROJECTS_JSON)
        project = pu.build_project(page_content, self.kwargs["project_id"])
        resume_content = ju.read_json_file(paths.CV_JSON)
        theme = get_theme(self.request)

        context = {**theme, **page_content, **resume_content, "project": project}

        return context

    # @csrf_exempt
    def form_valid(self, form):
        pu.edit_project(paths.CV_PROJECTS_JSON, self.kwargs["project_id"], form.cleaned_data)
        return super().form_valid(form)


class NightModeView(View):
    @csrf_exempt
    def post(self, request):
        return set_night_mode(request, instances.ENDPOINT_REDIRECTS[request.path])
