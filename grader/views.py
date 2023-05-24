import logging
# Create your views here.
import json
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

from grader.project_info import get_project_info, get_solution_text
from grader.evaluator import evaluate
logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello")


def generate_prompt(project_name, project_info):
    return


@csrf_exempt
def evaluate_project(request, project_name):
    valid_projects = {'fruit_search', 'software_test'}

    if request.method != 'POST' or project_name not in valid_projects:
        return HttpResponseNotFound("resource not found")

    body = json.loads(request.body)

    if not body['link']:
        return HttpResponseBadRequest("No link found")

    context_prompt = get_project_info(project_name)

    if not context_prompt:
        logger.error('empty context prompt')
        return HttpResponseServerError

    solution_text = get_solution_text(project_name, body['link'])

    if not solution_text:
        logger.error('empty context prompt')
        return HttpResponseServerError

    evaluation = evaluate(f"{context_prompt} \n\n {solution_text}")
    return HttpResponse(evaluation)
