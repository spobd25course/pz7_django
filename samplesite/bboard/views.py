from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Bb, Rubric
from .forms import BbForm
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.template.loader import render_to_string


class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context


def index(request):
    bbs = Bb.objects.all()
    form = BbForm()
    return render(request, 'bboard/index.html', {'bbs': bbs, 'form': form})



def rubric_bbs(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric
    }
    return render(request, 'bboard/rubric_bbs.html', context)

class BbUpdateView(UpdateView):
    model = Bb
    form_class = BbForm
    template_name = 'bboard/bb_edit.html'
    success_url = reverse_lazy('index')

class BbDeleteView(DeleteView):
    model = Bb
    template_name = 'bboard/bb_delete.html'
    success_url = reverse_lazy('index')

def ajax_add(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'errors': 'Только POST запрос.'})

    form = BbForm(request.POST, request.FILES)

    if form.is_valid():
        bb = form.save()

        html = render_to_string('bboard/_bb_item.html', {'bb': bb}, request=request)
        return JsonResponse({'ok': True, 'html': html})

    errors_text = ''
    for field, errors in form.errors.items():
        errors_text += f'{field}: {" ".join(errors)}; '

    return JsonResponse({'ok': False, 'errors': errors_text})
