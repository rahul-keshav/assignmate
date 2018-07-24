from django.shortcuts import render,redirect,reverse,get_object_or_404,render_to_response
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Assignment,Questions,Assignment_answered_by,\
    Studymaterial,Blogsite,Blog_page
from django.contrib.auth.models import User
from assignment.forms import QuestionForm,DocumentForm,Blog_site_Form,BlogForm
from django.core.paginator import Paginator
from django.urls import reverse_lazy


from django.db.models import Q
import re


# Create your views here.

def index(request):
    list_assignment=[]
    for useraccount in request.user.is_following.all():
        user=useraccount.user
        print(user)
        for assignment in user.assignment_set.all():
            list_assignment.append(assignment)

    return render(request,'assignment/index.html',{'list_assignment':list_assignment})

def view_list_assignment(request):
    assignment=Assignment.objects.all()
    paginator=Paginator(assignment,10)
    page=request.GET.get('page')
    assignment=paginator.get_page(page)
    return render(request,'assignment/assignment_page.html',{'assignment':assignment})

def view_list_my_assignment(request,pk=None):
    if pk:
        user=User.objects.get(pk=pk)
    else:
        user = request.user
    studymaterial = Studymaterial.objects.all()
    args={'user':user,'studymaterial': studymaterial}
    return render(request,'assignment/my_assignment_page.html',args)

class AssignmentUpdate(UpdateView):
    model = Assignment
    fields = ['title','discription']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('assignment:my_assignment_page')

class AssignmentCreate(CreateView):
    model = Assignment
    fields = ['title','discription']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class QuestionView(DetailView):
    template_name = 'assignment/question_paper.html'
    model = Assignment

class QuestionAdd(TemplateView):
    template_name = 'assignment/add_question_form.html'

    def get(self, request, *args, **kwargs):
        form=QuestionForm
        assignment = request.user.assignment_set.all
        args={'form':form,'assignment':assignment}
        return render(request,self.template_name,args)

    def post(self,request,pk):
        form=QuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False)
            question.assignment=Assignment.objects.get(pk=pk)
            question.save()

            text=form.cleaned_data['question']
            form=QuestionForm
            args={'pk':pk}
            return redirect(reverse('assignment:assignment_page'))

        args={'form':form,'text':text}
        render(request,self.template_name,args)

class QuestionUpdate(UpdateView):
    model = Questions
    fields = ['question','answer','option_a','option_b','option_c','option_d','positive_marks','negative_marks']
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('assignment:my_assignment_page')

class QuestionDelete(DeleteView):
    model = Questions
    success_url = reverse_lazy('assignment:my_assignment_page')

def assignment_check(request,assignment_id):
    assignment=get_object_or_404(Assignment,pk=assignment_id)
    marks=0
    total_marks=0
    forloopcounter = 1
    answersting=''
    for question in assignment.questions_set.all():

        post_input='inlineRadioOptions'+str(forloopcounter)

        answersting=answersting+request.POST[post_input]

        if request.POST[post_input]=='z':
         forloopcounter = forloopcounter + 1
         total_marks=total_marks+question.positive_marks

        elif question.answer==request.POST[post_input]:
         marks=marks+question.positive_marks
         forloopcounter = forloopcounter+1
         total_marks = total_marks + question.positive_marks

        elif question.answer!= request.POST[post_input]:
         marks = marks - question.negative_marks
         total_marks = total_marks + question.positive_marks
         forloopcounter = forloopcounter+1

    print(answersting)
    print(marks)

    p = Assignment_answered_by(name_of_assignment=assignment.title,assignment_id=assignment.id,user=request.user,answer_string=answersting,
                               marks=marks,total_marks=total_marks)
    p.save()

    return redirect(reverse('assignment:assignment_page'))

def answersheet(request,ass_id, ans_id):
    assignment=Assignment.objects.get(pk=ass_id)
    assignment_answered_by=Assignment_answered_by.objects.get(pk=ans_id)
    answer= assignment_answered_by.answer_string
    list1 = []
    for i in answer:
        list1.append(i)
    return render(request,'assignment/answersheetpage.html',{'assignment':assignment,'answer':list1} )

def studymaterial_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('assignment:my_assignment_page'))
    else:
        form = DocumentForm()
    return render(request, 'assignment/studymaterial_upload.html',{'form': form})

def add_blog_site(request):
    if request.method=='POST':
        form=Blog_site_Form(request.POST,request.FILES)

        if form.is_valid():
            blog_site=form.save(commit=False)
            blog_site.user = request.user
            blog_site.save()
            return redirect(reverse('assignment:blog_site_list'))
        else:
            return redirect(reverse('assignment:assignment_page'))
    else:
        form=Blog_site_Form()
        return render(request,'assignment/add_blog_site.html',{'form':form})

def blog_site_list(request,pk=None):
    if pk:
        user=User.objects.get(pk=pk)
    else:
        user=request.user


    return render(request,'assignment/blog_site_list.html',{'user':user,})

def view_blog_site(request,pk):
    blog_site=Blogsite.objects.get(pk=pk)
    blogs=blog_site.blog_page_set.all
    return render(request,'assignment/blog_site.html',{'blog_site':blog_site,'blogs':blogs})

def add_blog(request,pk):
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)

        if form.is_valid():
            blog=form.save(commit=False)
            blog.blog_site=Blogsite.objects.get(pk=pk)
            blog.save()

            return redirect(reverse('assignment:blog_site',args=[pk]))

    else:
        form=BlogForm()
        return render(request,'assignment/add_blog.html',{'form': form,})

def blog(request,pk):
    blog=Blog_page.objects.get(pk=pk)
    return render(request,'assignment/blog.html',{'blog':blog})

def result(request):
    result=request.user.assignment_answered_by_set.order_by('-submitted')
    return render(request,'assignment/result.html',{'result':result,})


#
# serch function starts
#



def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title',])
        found_entries = Assignment.objects.filter(entry_query).order_by('-user')
        entry_query_studymaterial = get_query(query_string, ['name','subject' ])
        found_entries_studymaterial = Studymaterial.objects.filter(entry_query_studymaterial).order_by('-name')
        found_entries=found_entries


    return render_to_response('assignment/searchresult.html',
                          { 'query_string': query_string,'found_entries_studymaterial':found_entries_studymaterial, 'found_entries':found_entries,

                            'user':request.user },
                          # context_instance=RequestContext(request)
                              )
# search function ends



