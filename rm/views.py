import logging

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.db.models.functions import Now
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views import View
from django.views.generic import ListView, TemplateView

from rm.constants import FileStatus
from rm.forms import UploadFileForm
from rm.models import StageContract, InterfaceCall
from rm.interface_file_util import check_file_and_interface_type

logger = logging.getLogger(__name__)

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


def process_file(file, user):
    """
    Process the file, register it with the user, find out the type

    """
    # First things first, create the InterfaceCall, with the user
    interfaceCall = InterfaceCall(filename=file.name,
                                  status=FileStatus.NEW,
                                  date_time_creation=Now(),
                                  user=user,
                                  username=user.username,
                                  user_email=user.email)
    try:
        # check the file and try to find out what type it is
        interfaceFile = check_file_and_interface_type(file)

        # register InterfaceDefinition
        interfaceCall.interface_definition = interfaceFile.get_interface_definition()
        interfaceCall.save()

        # process the file!
        interfaceFile.process(interfaceCall)

    except Exception as ex:

        interfaceCall.status = FileStatus.ERROR.name
        interfaceCall.message = ex.__str__()
        interfaceCall.save()
        return "ERROR", ex.__str__()

    return "OK", "File has been processed"


@permission_required('rm.upload_contract_file', raise_exception=True)
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']

            status, msg = process_file(file, request.user)

            if status == "ERROR":
                form.add_error("file", msg)
                return render(request, 'rm/upload.html', {'form': form})
            else:
                return HttpResponseRedirect('/interfacecalls')
    else:
        form = UploadFileForm()
    return render(request, 'rm/upload.html', {'form': form})


class ContractListView(PermissionRequiredMixin, ListView):
    permission_required = 'rm.view_contract'
    raise_exception = True

    model = StageContract
    context_object_name = 'contract_list'
    template_name = 'contract_list.html'

    def get_queryset(self):
        user = self.request.user
        # if user.is_superuser:
        return StageContract.objects.all()
        # else:
        #     return StageContract.objects.filter(contract_owner=user.name_in_negometrix)

class InterfaceCallListView(ListView):
    model = InterfaceCall
    context_object_name = 'interface_call_list'
    template_name = 'rm/interface_call_list.html'
    # ordering = ['-date_time_creation'] is done through DataTables in JavaScript (see custom.css)

@permission_required('rm.view_contract', raise_exception=True)
def interface_call_details(request, pk: int):
    logger.debug(f"interface_call_details: pk: {pk}")
    interfaceCall = InterfaceCall.objects.get(pk=pk)
    logger.debug("interface_call: " + interfaceCall.__str__())

    contracts = interfaceCall.contracts()

    raw_data = interfaceCall.rawdata_set.all()
    context = {
        'interface_call': interfaceCall,
        'contract_list': contracts,
        'received_data': raw_data,
    }
    template = loader.get_template('rm/interface_call_details.html')
    return HttpResponse(template.render(context, request))


class RefreshDataSets(View):
    pass