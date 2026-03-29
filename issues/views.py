import json
from django.http import JsonResponse
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue
from django.views.decorators.csrf import csrf_exempt


REPORTERS_FILE = 'reporters.json'
ISSUES_FILE = 'issues.json'

def create_reporter(request):
    if request.method == 'POST':
        
        # Step 1 - read and parse the request body
        data = json.loads(request.body)
        
        # Step 2 - create a Reporter object
        reporter = Reporter(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            team=data['team']
        )
        
        # Step 3 - validate
        try:
            reporter.validate()
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        # Step 4 - read existing reporters from file
        with open(REPORTERS_FILE, 'r') as f:
            reporters = json.load(f)
        
        # Step 5 - append new reporter and write back
        reporters.append(reporter.to_dict())
        with open(REPORTERS_FILE, 'w') as f:
            json.dump(reporters, f, indent=2)
        
        # Step 6 - return response
        return JsonResponse(reporter.to_dict(), status=201)
    

def get_reporters(request):
        if request.method == 'GET':
            with open(REPORTERS_FILE, 'r') as f:
                reporters = json.load(f)
            return JsonResponse({'reporters': reporters})
        
    
def get_reporter_by_id(request):
        if request.method == 'GET':
            with open(REPORTERS_FILE, 'r') as f:
                reporters = json.load(f)

            reporter_id = request.GET.get('id')
            if not reporter_id:
                return JsonResponse({'error': 'ID is required'}, status=400)
            reporter_id = int(reporter_id)
            for reporter in reporters:
                if reporter['id'] == reporter_id:
                    return JsonResponse(reporter)
            return JsonResponse({'error': 'Reporter not found'}, status=404)

def create_issue(request):
    if request.method == 'POST':
        # Step 1 - read and parse the request body
        data = json.loads(request.body)
        #step 2 - create an Issue object based on priority
        if data['priority'] == 'critical':
            issue = CriticalIssue(
                id=data['id'],
                title=data['title'],
                description=data['description'],
                status=data['status'],
                priority=data['priority'],
                reporter_id=data['reporter_id']
            )
        elif data['priority'] == 'low':
            issue = LowPriorityIssue(
                id=data['id'],
                title=data['title'],
                description=data['description'],
                status=data['status'],
                priority=data['priority'],
                reporter_id=data['reporter_id']
            )
        else:
            issue = Issue(
                id=data['id'],
                title=data['title'],
                description=data['description'],
                status=data['status'],
                priority=data['priority'],
                reporter_id=data['reporter_id']
            )

        try:
            issue.validate()
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        with open(ISSUES_FILE, 'r') as f:
            issues = json.load(f)
        
        issues.append(issue.to_dict())
        with open(ISSUES_FILE, 'w') as f:
            json.dump(issues, f, indent=2)
        
        response_data = issue.to_dict()
        response_data['message'] = issue.describe()
        return JsonResponse(response_data, status=201)
    
def get_issues(request):
    if request.method == 'GET':
        with open(ISSUES_FILE, 'r') as f:
            issues = json.load(f)
        return JsonResponse({'issues': issues})
     
        
def get_issue_by_id(request):
    if request.method == 'GET':
        with open(ISSUES_FILE, 'r') as f:
            issues = json.load(f)

        issue_id = request.GET.get('id')
        if not issue_id:
            return JsonResponse({'error': 'ID is required'}, status=400)
        issue_id = int(issue_id)
        for issue in issues:
            if issue['id'] == issue_id:
                return JsonResponse(issue)
        return JsonResponse({'error': 'Issue not found'}, status=404)
    

def get_issues_by_status(request):
    if request.method == 'GET':
        with open(ISSUES_FILE, 'r') as f:
            issues = json.load(f)

        status = request.GET.get('status')
        if not status:
            return JsonResponse({'error': 'Status is required'}, status=400)

        filtered_issues = [issue for issue in issues if issue['status'] == status]
        return JsonResponse({'issues': filtered_issues})
    


@csrf_exempt
def reporters(request):
    if request.method == 'POST':
        return create_reporter(request)
    elif request.method == 'GET':
        if 'id' in request.GET:
            return get_reporter_by_id(request)
        return get_reporters(request)


@csrf_exempt
def issues(request):
    if request.method == 'POST':
        return create_issue(request)
    elif request.method == 'GET':
        if 'id' in request.GET:
            return get_issue_by_id(request)
        if 'status' in request.GET:
            return get_issues_by_status(request)
        return get_issues(request)
