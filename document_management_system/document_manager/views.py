from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.urls import reverse
from django.contrib import messages	
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document
from django.utils import timezone
from django.views import generic
# Create your views here.

# def index(request):
# 	return render(request, 'document_manager/index.html')

class IndexView(generic.ListView):
	"""
	generic List view to show docs list of the month
	"""
	
	model = Document
	template_name = 'document_manager/index.html'
	context_object_name = 'todays_pdf_list'

	def get_context_data(self, *args, **kwargs):

		if self.request.user.username != "":
			for_user = User.objects.get(username=self.request.user.username)
			users_pdfs = Document.objects.filter(user=for_user)
			users_pdfs_of_today = users_pdfs.filter(created_at__date=timezone.now())
			# print(users_pdfs)
			context = {'todays_pdf_list':users_pdfs_of_today}
		else:
			context = {'todays_pdf_list':""}

		return context



@login_required
def upload(request):
	"""
	View for handling file uplods
	"""

	doc_form  = DocumentForm()

	if request.method == "POST":

		doc_form = DocumentForm(request.POST,request.FILES)
		user = request.user.username
		user_obj = User.objects.get(username=user)
		todays_pdfs = Document.objects.filter(user=user_obj.pk).filter(created_at__date=timezone.now())
		users_today_uploads = todays_pdfs.count()

		if users_today_uploads == 5:
			messages.info(request, "You can Only upload 5 docs/day !")
			return redirect(reverse('upload'))

		else:

			if doc_form.is_valid():
				if request.FILES['PDF'].size > 5242880:
					messages.info(request, "Size can't be more than 5 MiB")
					return redirect(reverse('upload'))
				else:	
					doc_obj = doc_form.save(commit=False)
					doc_obj.user = user_obj
					doc_obj.save()
					# breakpoint()
					messages.success(request, "Uploaded Successfully")
					return redirect(reverse('upload'))
			else:
				messages.error(request, "Error Occured")
				return redirect(reverse('upload'))

	else:
		
		context = {'form':doc_form}
		return render(request, 'document_manager/upload.html', context)

@login_required
def report(request):
	"""
	function to generate report of documents
	and sort by name, date, year, month
	"""
	user_docs = Document.objects.filter(user=User.objects.get(username=request.user.username))
	# breakpoint()
	daily_uploads = user_docs.filter(created_at__day=timezone.now().strftime("%d"))
	monthly_uploads = user_docs.filter(created_at__month=timezone.now().strftime("%m"))
	yearly_uploads = user_docs.filter(created_at__year=timezone.now().strftime("%Y"))

	daily_count = daily_uploads.count()
	monthly_count = monthly_uploads.count()
	yearly_count = yearly_uploads.count()
	# breakpoint()

	if 'doc_name' in request.GET:
		pdf_list = user_docs.filter(name__icontains=request.GET['doc_name'])
	elif 'month' in request.GET:
		pdf_list = user_docs.filter(created_at__month=request.GET['month'])
		# breakpoint()
	elif 'year' in request.GET:
		pdf_list = user_docs.filter(created_at__year=request.GET['year'])
	elif 'from' in request.GET and 'to' in request.GET:
		# breakpoint()
		pdf_list = user_docs.filter(created_at__range=[request.GET['from'],request.GET['to']])

	else:
		pdf_list = user_docs
	context = {'daily_count': daily_count, 'monthly_count': monthly_count, 'yearly_count': yearly_count, 'pdf_list':pdf_list}

	return render(request, 'document_manager/report.html', context)