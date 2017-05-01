from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Choice, Question
import json

# Common base class for FC
class FusionCharts:

   #constructorOptions = {}
   constructorTemplate = """
     <script type="text/javascript">
         FusionCharts.ready(function () {
             new FusionCharts(__constructorOptions__);
         });
     </script>"""
   renderTemplate = """
     <script type="text/javascript">
         FusionCharts.ready(function () {
             FusionCharts("__chartId__").render();
         });
     </script>
   """
   # constructor
   def __init__(self, type, id, width, height, renderAt, dataFormat, dataSource): 
      self.constructorOptions = {}  
      self.constructorOptions['type'] = type
      self.constructorOptions['id'] = id
      self.constructorOptions['width'] = width
      self.constructorOptions['height'] = height
      self.constructorOptions['renderAt'] = renderAt
      self.constructorOptions['dataFormat'] = dataFormat
      #dataSource = unicode(dataSource, errors='replace')
      self.constructorOptions['dataSource'] = dataSource
   # render the chart created
   # It prints a script and calls the FusionCharts javascript render method of created chart   
   def render(self):
    self.readyJson = json.dumps(self.constructorOptions)
    self.readyJson = FusionCharts.constructorTemplate.replace('__constructorOptions__', self.readyJson)
    self.readyJson = self.readyJson + FusionCharts.renderTemplate.replace('__chartId__', self.constructorOptions['id'])
    self.readyJson = self.readyJson.replace('\\n', '')
    self.readyJson = self.readyJson.replace('\\t', '')

    if(self.constructorOptions['dataFormat'] == 'json'):
      self.readyJson = self.readyJson.replace('\\', '')
      self.readyJson = self.readyJson.replace('"{', "{")
      self.readyJson = self.readyJson.replace('}"', "}")
      
    return self.readyJson
   
   
   
    
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    dataSource = {}
    dataSource['chart'] = { 
		"caption": "Poll Results",
        "xAxisName": "Choice",
        "yAxisName": "Votes",
        "theme": "fint"
    }
    dataSource['data'] = []
    for choice in question.choice_set.all():
        data = {}
        data['label'] = choice.choice_text
        data['value'] = choice.votes
        dataSource['data'].append(data)
    column2D = FusionCharts("column2D", "ex1", "600", "400", "chart-1", "json", dataSource)
    return render(request, 'polls/results.html', {'output': column2D.render(), 'question': question})
        	
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
# Create your views here.
