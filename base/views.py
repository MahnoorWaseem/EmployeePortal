from django.shortcuts import render,redirect
from base.models import EmpInfo,Attendance,Admininfo
from base.forms import EmpForm, MyForm, Search, Email,empSearch,SearchEmpinfo,EmailAdmin
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime,timedelta
from django.contrib import messages
from django.core.mail import send_mail
import functools
import operator
from django.conf import settings


# Create your views here.
def home(request):
    return render(request,'index.html')

def signup(request):  
    if request.method == "POST":  
        form = EmpForm(request.POST,request.FILES)  
        dept=request.POST['dept']
        eid=request.POST['eid']
        data = EmpInfo.objects.filter(eid=eid)

        if (data.exists()):
            messages.error(request,'Employee ID must not be repeating!')
            return redirect('/signup')

        if form.is_valid():  
            try:  
                messages.success(request,'Account created Successfully!')
                form.save() 
                # dept=EmpInfo(dept=dept)
                # dept.save()
                print('eid is==',eid)
                mydata = EmpInfo.objects.filter(eid=eid)
                for object in mydata:
                # print(object.ename)
                    object.dept=dept
                    object.save()

                form = EmpForm()  
                # return render(request,'signup.html',{'form':form})  
                return redirect('/adminMEdashboard')  
            except:  
                messages.error(request,'Kindly provide valid details!')
                return redirect('/adminMEdashboard')
                  
    else:  
        form = EmpForm()  
    return render(request,'signup.html',{'form':form})  

# def signin(request):
#     if request.user.is_authenticated:
#         return render(request, 'dashboard.html')
#     if request.method == 'POST':
#         eid = request.POST['eid']
#         password = request.POST['password']
#         user = authenticate(request, eid=eid, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/dashboard') 
#         else:
#             msg = 'Error Login'
#             form = EmpForm(request.POST)
#             return render(request, 'home.html', {'form': form, 'msg': msg})
#     else:
#         form = EmpForm()
#         return render(request, 'home.html', {'form': form})
    

def signin(request):
    if request.method == "POST":  
        form = MyForm(request.POST)  
        if form.is_valid():
            # global eid
            eid = form.cleaned_data['eid']
            password=form.cleaned_data['password']
        mydata = EmpInfo.objects.filter(eid=eid, password=password).values()
        if mydata.exists():
            print('Row Found')
            # return redirect('/dashboard')
            # response=HttpResponse("Cookies Set!")
            # response.set_cookie('eid',eid)
            # print(response)

            request.session['eid']=eid
            request.session['loggedin']='Yes'
            print('session set')
            # profile = EmpInfo.objects.filter(eid=eid, password=password)
            return redirect('/dashboard')
        else:
            print('No row found')
            return redirect('/signin')


    else:  
        form = MyForm()  
    return render(request,'signin.html',{'form':form})  

# def sendEmailToClient():
#     subject=""
#     message=""
#     fromEmail = settings.EMAIL_HOST_USER
#     toEmail= [settings.EMAIL_HOST_USER]

#     send_mail(subject, message, fromEmail, toEmail, fail_silently=False,)

def sendemail(request):
    eid=request.session['eid']
    myrow=EmpInfo.objects.filter(eid=eid)
    for obj in myrow:
        ename=obj.ename
    subject=f"Message from {ename}, Employee Id: {eid}, SSGC"
    if request.method=='POST':
        email=request.POST['email']

    msg=email

    send_mail(
    subject,
    msg,
    "ssgcmanager90@gmail.com",
    ["ssgcmanager90@gmail.com"],
    fail_silently=False,)
    messages.success(request,'Message sent Successfully!')
    return redirect('dashboard')


def sendemailatt(request):
    eid=request.session['eid']
    myrow=EmpInfo.objects.filter(eid=eid)
    for obj in myrow:
        ename=obj.ename
    subject=f"Message from {ename}, Employee Id: {eid}, SSGC"
    if request.method=='POST':
        email=request.POST['email']

    msg=email

    send_mail(
    subject,
    msg,
    "ssgcmanager90@gmail.com",
    ["ssgcmanager90@gmail.com"],
    fail_silently=False,)
    messages.success(request,'Message sent Successfully!')
    return redirect('myattendance')


def sendemailpro(request):
    eid=request.session['eid']
    myrow=EmpInfo.objects.filter(eid=eid)
    for obj in myrow:
        ename=obj.ename
    subject=f"Message from {ename}, Employee Id: {eid}, SSGC"
    if request.method=='POST':
        email=request.POST['email']

    msg=email

    send_mail(
    subject,
    msg,
    "ssgcmanager90@gmail.com",
    ["ssgcmanager90@gmail.com"],
    fail_silently=False,)
    messages.success(request,'Message sent Successfully!')
    return redirect('myprofile')


def dashboard(request):
    loggedin=request.session['loggedin']
    if(loggedin=='Yes'):
        date = datetime.now()
        day = date.day
        month = date.month
        day=str(day)
        month=str(month)
        if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
            month= f"0{month}"

        if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
            day= f"0{day}"

        # type cast
        year = date.year
        
        dayno = date.weekday()
        print(dayno)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
        dayname = days[dayno]
        
        
        # current_date = f"{day}/{month}/{year}, {dayname}"
        current_date = f"{month}/{day}/{year}"
        eid=request.session['eid']
        profile = EmpInfo.objects.filter(eid=eid)
        emailform=Email()
        # mydata2 = Attendance.objects.filter(eid_id=eid,date=current_date,workinghr__isnull=True)
        show = Attendance.objects.filter(eid_id=eid, date=current_date)
        # if not(mydata2.exists()):
        #     list1=[]
        #     for obj in show:
        #         startime2=obj.workinghr
        #         dt = datetime.strptime(startime2,"%H:%M:%S")
        #         total_sec = dt.hour*3600 + dt.minute*60 + dt.second  # total seconds calculation
        #         td = timedelta(seconds=total_sec)           # timedelta construction
        #         print(td)  
        #         list1.append(td)
        #         print('working hr type',type(td))
        #     res=functools.reduce(operator.add,list1)
        #     return render(request,'dashboardfinalcopy.html',{'res':res, 'show':show, 'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform}) 

        return render(request,'dashboardfinalcopy.html',{'show':show, 'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform}) 
    else:
        return HttpResponse('Kindly login First!')

def timein(request):
    loggedin=request.session['loggedin']
    eid=request.session['eid']
    if(loggedin=='Yes'):
        date = datetime.now()
        day = date.day
        month = date.month
        day=str(day)
        month=str(month)
        if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
            month= f"0{month}"

        if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
            day= f"0{day}"
        year = date.year
        dayno = date.weekday()
        print(dayno)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
        dayname = days[dayno]
        
        hr = date.hour
        min = date.minute
        
        current_date = f"{month}/{day}/{year}"
        current_time = f"{hr}:{min}"

        startime=datetime.strptime(current_time,"%H:%M")
        breakbegin=datetime.strptime('13:30','%H:%M')
        breakend=datetime.strptime('14:30','%H:%M')

        show = Attendance.objects.filter(eid_id=eid, date=current_date)
        profile = EmpInfo.objects.filter(eid=eid)
        emailform=Email()

        if ((startime>=breakbegin) and  (startime<=breakend)):
            messages.error(request,'You cannot timein during break hours')
            return redirect('dashboard')

        context={'current_date':current_date,'current_time':current_time}
        mydata = Attendance.objects.filter(eid_id=eid,date=current_date,timeout__isnull=True)

      

        if (mydata.exists()):
            messages.error(request, 'You cannot timein again. Kindly timeout first.')
            return redirect('dashboard')

        att=Attendance(eid_id=eid,date=current_date,timein=current_time)    
        att.save()
        
        messages.success(request,f'You Checked in at {current_time}')
        return redirect('dashboard')
        # return render(request,'dashboardfinalcopy.html',{'show':show,'date':current_date,'dayname':dayname,'profile':profile,'emailform':emailform})
    else:
        return redirect('/signin')

def timeout(request):
    date = datetime.now()
    
    day = date.day
    month = date.month
    year = date.year
    
    dayno = date.weekday()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    dayname = days[dayno]
    
    day=str(day)
    month=str(month)
    if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
        month= f"0{month}"

    if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
        day= f"0{day}"

    hr = date.hour
    min = date.minute
    
    # current_date2 = f"{day}/{month}/{year}, {dayname}"
    current_date2 = f"{month}/{day}/{year}"
    current_time2 = f"{hr}:{min}"
   

    # lasttime=datetime.strptime("13:42","%H:%M")
    # breakbegin=datetime.strptime('13:30','%H:%M')
    # breakend=datetime.strptime('14:30','%H:%M')

    # if ((lasttime>=breakbegin) and  (lasttime<=breakend)):
    #     print('null')
    #     return HttpResponse('You cannot timeout during break hours')
    
    print(current_date2, current_time2)
    context={'current_date':current_date2,'current_time2':current_time2}
    
    # att=Attendance(timeout=current_time)   #where  current_date==current_date2
    # att.save()
    

    # eid= request.COOKIES['eid']
    # print(eid)

    eid=request.session['eid']
    # current_time=request.session['current_time']
    
    print(eid)

    show = Attendance.objects.filter(eid_id=eid, date=current_date2)
    profile = EmpInfo.objects.filter(eid=eid)
    list1=[]
    # for obj in show:
    #     startime2=obj.workinghr
    #     dt = datetime.strptime(startime2,"%H:%M:%S")
    #     total_sec = dt.hour*3600 + dt.minute*60 + dt.second  # total seconds calculation
    #     td = timedelta(seconds=total_sec)           # timedelta construction
    #     print(td)  
    #     list1.append(td)
    #     print('working hr type',type(td))
    # res=functools.reduce(operator.add,list1)
    # print('res',res)
    emailform=Email()

    mydata = Attendance.objects.filter(eid_id=eid,date=current_date2,timeout__isnull=True)
    if not(mydata.exists()):
        messages.error(request,'Kindly timein first! ')
        return redirect('dashboard')

    
    startime=datetime.strptime(current_time2,"%H:%M")
    breakbegin=datetime.strptime('13:30','%H:%M')
    breakend=datetime.strptime('14:30','%H:%M')

    
    if ((startime>=breakbegin) and  (startime<=breakend)):
        messages.error(request,'You cannot timeout during break hours')
        return redirect('dashboard')
        
        

    print('my data',mydata)
    for object in mydata:
        # print(object.ename)
        object.timeout=current_time2
        object.save()

    myrow=Attendance.objects.filter(eid_id=eid,date=current_date2,timeout=current_time2)
    for obj in myrow:
        checkin=obj.timein
    
    startime=datetime.strptime(checkin,"%H:%M")
    endtime=datetime.strptime(current_time2,"%H:%M")

    # duration=endtime-startime
    print('s>e',startime>endtime)
    print('e>s',endtime>startime)
    # print('duraion is :', duration)

    if ((startime<breakbegin) and (endtime>breakend)):
        finaltimeout=endtime-timedelta(hours=1)
        duration=finaltimeout-startime
    else:
        duration=endtime-startime
        # minus one hr

    for obj in myrow:
        obj.workinghr=duration
        obj.save()

    show = Attendance.objects.filter(eid_id=eid, date=current_date2)
    profile = EmpInfo.objects.filter(eid=eid)
    eid=request.session['eid']
    list1=[]
    for obj in show:
        startime2=obj.workinghr
        dt = datetime.strptime(startime2,"%H:%M:%S")
        total_sec = dt.hour*3600 + dt.minute*60 + dt.second  # total seconds calculation
        td = timedelta(seconds=total_sec)           # timedelta construction
        print(td)  
        list1.append(td)
        print('working hr type',type(td))
    res=functools.reduce(operator.add,list1)
    print('res',res)
    emailform=Email()

    messages.success(request,f'You Checked out at {current_time2}')
    return render(request,'dashboardfinalcopy.html',{'show2':show,'date':current_date2,'dayname':dayname,'profile':profile,'res':res,'emailform':emailform})

def logout(request):
    request.session['eid']=""
    request.session['loggedin']='logout'
    return redirect('/index')


# admin panel

def searchatt(request):
    date = datetime.now()
    day = date.day
    month = date.month
    day=str(day)
    month=str(month)
    if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
        month= f"0{month}"

    if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
        day= f"0{day}"

    # type cast
    year = date.year
    
    dayno = date.weekday()
    print(dayno)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    dayname = days[dayno]
    
    
    # current_date = f"{day}/{month}/{year}, {dayname}"
    current_date = f"{month}/{day}/{year}"
    eid=request.session['eid']
    profile = Admininfo.objects.filter(eid=eid)
    emailform=Email()
    sform=Search()
    sform2=empSearch()


    if request.method == "POST":  
        form = Search(request.POST)  
        if form.is_valid():
            eid = form.cleaned_data['search']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            
            
        if (month=='jan' or month=='Jan'):
            monthno='01'
        elif(month=='feb' or month=='Feb'):
            monthno='02'
        elif(month=='mar' or month=='Mar'):
            monthno='03'
        elif(month=='apr' or month=='Apr'):
            monthno='04'
        elif(month=='may' or month=='May'):
            monthno='05'
        elif(month=='jun' or month=='Jun' or month=='jun' or month=='Jun'):
            monthno='06'
        elif(month=='july' or month=='July' or month=='jul' or month=='Jul'):
            monthno='07'
        elif(month=='aug' or month=='Aug'):
            monthno='08'
        elif(month=='sep' or month=='Sep'):
            monthno='09'
        elif(month=='oct' or month=='Oct'):
            monthno='10'
        elif(month=='nov' or month=='Nov'):
            monthno='11'
        elif(month=='dec' or month=='Dec'):
            monthno='12'
        
        # mydata = Attendance.objects.filter(eid=eid)
        record = EmpInfo.objects.filter(eid=eid)
        for object in record:
            print(object.ename)
            ename=object.ename
        mydata = Attendance.objects.filter(eid=eid,date__startswith=monthno,date__endswith=year)
        # print(mydata.ename)
        form = Search() 

        if not (mydata.exists()):
            msg=f"No Record Found for EmpID: {eid} in Month of {month}, {year} "
            messages.success(request,msg)
            return render(request,'adminATTdashboard.html',{'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'sform':sform,'sform2':sform2 })
        
        return render(request,'show.html',{'att':mydata,'ename':ename,'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'sform':sform,'sform2':sform2})  

    # else:  
    #     form = Search()  
    # return render(request,'admin.html',{'form':form}) 
   
# def show(request):
#     if request.method == "POST":  
#         form = Search(request.POST)  
#         if form.is_valid():
#             eid = form.cleaned_data['search']
#         mydata = Attendance.objects.filter(eid=eid)
#         return render(request,'show.html',{'att':mydata}) 

#     else:  
#         form = Search()  
#     return render(request,'admin.html',{'form':form}) 

def myattendance(request):
    date = datetime.now()
    day = date.day
    month = date.month
    day=str(day)
    month=str(month)
    if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
        month= f"0{month}"
    if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
        day= f"0{day}"
    year = date.year
    dayno = date.weekday()
    print(dayno)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    dayname = days[dayno]
    # current_date = f"{day}/{month}/{year}, {dayname}"
    current_date = f"{month}/{day}/{year}"
    eid=request.session['eid']
    profile = EmpInfo.objects.filter(eid=eid)
    emailform=Email()   

    if (month=='01'):
        monthname='January'
    elif(month=='02'):
        monthname='Febuary'
    elif(month=='03'):
        monthname='March'
    elif(month=='04'):
        monthname='April'
    elif(month=='05'):
        monthname='May'
    elif(month=='06'):
        monthname='June'
    elif(month=='07'):
        monthname='July'
    elif(month=='08'):
        monthname='August'
    elif(month=='09'):
        monthname='September'
    elif(month=='10'):
        monthname='October'
    elif(month=='11'):
        monthname='November'
    elif(month=='12'):
        monthname='December'
        
    mydata = Attendance.objects.filter(eid=eid,date__startswith=month,date__endswith=year)

    return render(request,'attendancedashboard.html',{ 'monthname':monthname,'year':year, 'mydata':mydata, 'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform}) 

def myprofile(request):
    date = datetime.now()
    day = date.day
    month = date.month
    day=str(day)
    month=str(month)
    if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
        month= f"0{month}"
    if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
        day= f"0{day}"
    year = date.year
    dayno = date.weekday()
    print(dayno)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    dayname = days[dayno]
    # current_date = f"{day}/{month}/{year}, {dayname}"
    current_date = f"{month}/{day}/{year}"
    eid=request.session['eid']
    profile = EmpInfo.objects.filter(eid=eid)
    emailform=Email()   

        
    mydata = EmpInfo.objects.filter(eid=eid)

    return render(request,'profiledashboard.html',{'mydata':mydata, 'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform}) 


# admin ME

def adminlogin(request):
    if request.method == "POST":  
        form = MyForm(request.POST)  
        if form.is_valid():
            # global eid
            eid = form.cleaned_data['eid']
            password=form.cleaned_data['password']
        mydata = Admininfo.objects.filter(eid=eid, password2=password).values()
        if mydata.exists():
            print('Row Found')

            request.session['eid']=eid
            request.session['loggedin']='Yes'
            print('session set')
            # profile = EmpInfo.objects.filter(eid=eid, password=password)
            # return HttpResponse('Admin Login Succesful')
            return redirect('/viewattendanceAdmin')
        else:
            print('No row found')
            return redirect('/admin')


    else:  
        form = MyForm()  
    return render(request,'adminsignin.html',{'form':form})  





def adminMEdashboard(request):
    loggedin=request.session['loggedin']
    if loggedin=='Yes':
        date = datetime.now()
        day = date.day
        month = date.month
        day=str(day)
        month=str(month)
        if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
            month= f"0{month}"

        if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
            day= f"0{day}"

        # type cast
        year = date.year
        
        dayno = date.weekday()
        print(dayno)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
        dayname = days[dayno]
        
        
        # current_date = f"{day}/{month}/{year}, {dayname}"
        current_date = f"{month}/{day}/{year}"
        eid=request.session['eid']
        profile = Admininfo.objects.filter(eid=eid)
        emailform=EmailAdmin()
        # mydata2 = Attendance.objects.filter(eid_id=eid,date=current_date,workinghr__isnull=True)
        # if not(mydata2.exists()):
        #     list1=[]
        #     for obj in show:
        #         startime2=obj.workinghr
        #         dt = datetime.strptime(startime2,"%H:%M:%S")
        #         total_sec = dt.hour*3600 + dt.minute*60 + dt.second  # total seconds calculation
        #         td = timedelta(seconds=total_sec)           # timedelta construction
        #         print(td)  
        #         list1.append(td)
        #         print('working hr type',type(td))
        #     res=functools.reduce(operator.add,list1)
        #     return render(request,'dashboardfinalcopy.html',{'res':res, 'show':show, 'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform}) 
        employees=EmpInfo.objects.all()
        EmpinfoForm=SearchEmpinfo()
        show='yes'
        return render(request,'adminMEdashboard.html',{'employees':employees, 'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'EmpinfoForm':EmpinfoForm,'show':show}) 
    else:
        return redirect('/admin')
def edit(request,slug):
    date = datetime.now()
    day = date.day
    month = date.month
    day=str(day)
    month=str(month)
    if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
        month= f"0{month}"

    if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
        day= f"0{day}"
    year = date.year
    
    dayno = date.weekday()
    print(dayno)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    dayname = days[dayno]
    current_date = f"{month}/{day}/{year}"
    eid=request.session['eid']
    profile = Admininfo.objects.filter(eid=eid)
    emailform=Email()
    employee=EmpInfo.objects.get(eid=slug)
    return render(request, 'edit.html',{'employee':employee, 'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform})

def update(request,slug):
     employee=EmpInfo.objects.get(eid=slug)
     eid=request.POST['eid']
     dept=request.POST['dept']
     form=EmpForm(request.POST,request.FILES,instance=employee)
     if form.is_valid():
         messages.success(request,'Information Updated Successfully!')
         form.save()
         eid=request.POST['eid']
         mydata = EmpInfo.objects.filter(eid=eid)
         for object in mydata:
            object.dept=dept
            object.save()
         return redirect("/adminMEdashboard")
     messages.error(request,'Cannot Update.Kindly provide Valid Credentials!')
     return redirect("/adminMEdashboard")

def destroy(request,slug):
    employee=EmpInfo.objects.get(eid=slug)
    employee.delete()
    messages.success(request,'Deleted Successfully')
    return redirect("/adminMEdashboard")

def viewattendanceAdmin(request):
    loggedin=request.session['loggedin']
    if loggedin=='Yes':
        date = datetime.now()
        day = date.day
        month = date.month
        day=str(day)
        month=str(month)
        if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
            month= f"0{month}"

        if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
            day= f"0{day}"

        # type cast
        year = date.year
        
        dayno = date.weekday()
        print(dayno)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
        dayname = days[dayno]
        
        
        # current_date = f"{day}/{month}/{year}, {dayname}"
        current_date = f"{month}/{day}/{year}"
        eid=request.session['eid']
        profile = Admininfo.objects.filter(eid=eid)
        emailform=EmailAdmin()
        sform=Search()
        sform2=empSearch()
        return render(request,'adminATTdashboard.html',{'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'sform':sform,'sform2':sform2}) 
    else:
        return redirect('/admin')

def searchattStaff(request):
    date = datetime.now()
    day = date.day
    month = date.month
    day=str(day)
    month=str(month)
    if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
        month= f"0{month}"

    if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
        day= f"0{day}"

    # type cast
    year = date.year
    
    dayno = date.weekday()
    print(dayno)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    dayname = days[dayno]
    
    
    # current_date = f"{day}/{month}/{year}, {dayname}"
    current_date = f"{month}/{day}/{year}"
    eid=request.session['eid']
    profile = Admininfo.objects.filter(eid=eid)
    emailform=EmailAdmin()
    sform=Search()
    sform2=empSearch()


    if request.method == "POST":  
        form = empSearch(request.POST)  
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            
            
        if (month=='jan' or month=='Jan'):
            monthno='01'
        elif(month=='feb' or month=='Feb'):
            monthno='02'
        elif(month=='mar' or month=='Mar'):
            monthno='03'
        elif(month=='apr' or month=='Apr'):
            monthno='04'
        elif(month=='may' or month=='May'):
            monthno='05'
        elif(month=='jun' or month=='Jun' or month=='jun' or month=='Jun'):
            monthno='06'
        elif(month=='july' or month=='July' or month=='jul' or month=='Jul'):
            monthno='07'
        elif(month=='aug' or month=='Aug'):
            monthno='08'
        elif(month=='sep' or month=='Sep'):
            monthno='09'
        elif(month=='oct' or month=='Oct'):
            monthno='10'
        elif(month=='nov' or month=='Nov'):
            monthno='11'
        elif(month=='dec' or month=='Dec'):
            monthno='12'
        
        # mydata = Attendance.objects.filter(eid=eid)
        # record = EmpInfo.objects.filter(eid=eid)
        # for object in record:
        #     print(object.ename)
        #     ename=object.ename
        mydata = Attendance.objects.filter(date__startswith=monthno,date__endswith=year)
        # print(mydata.ename)
        form = Search() 

        if not (mydata.exists()):
            msg=f"No Record Found for the Month of {month}, {year} "
            messages.success(request,msg)
            return render(request,'adminATTdashboard.html',{'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'sform':sform,'sform2':sform2 })
        
        return render(request,'show2.html',{'att':mydata,'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'sform':sform,'sform2':sform2})  


def searchemp(request):
    date = datetime.now()
    day = date.day
    month = date.month
    day=str(day)
    month=str(month)
    if (month=='1' or month=='2' or month=='3'or month=='4' or month=='5' or month=='6' or month=='7'or month=='8' or month=='9'):
        month= f"0{month}"

    if (day=='1' or day=='2' or day=='3'or day=='4' or day=='5' or day=='6' or day=='7'or day=='8' or day=='9'):
        day= f"0{day}"

    # type cast
    year = date.year
    
    dayno = date.weekday()
    print(dayno)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday','Saturday','Sunday']
    dayname = days[dayno]
    
    
    # current_date = f"{day}/{month}/{year}, {dayname}"
    current_date = f"{month}/{day}/{year}"
    eid=request.session['eid']
    profile = Admininfo.objects.filter(eid=eid)
    emailform=EmailAdmin()
    EmpinfoForm=SearchEmpinfo()
    if request.method == "POST":  
        form = SearchEmpinfo(request.POST)  
        if form.is_valid():
            eid = form.cleaned_data['eid']            
        mydata = EmpInfo.objects.filter(eid=eid)

        if not (mydata.exists()):
            msg=f"No Record Found for {eid} "
            messages.success(request,msg)
            return render(request,'showEmp.html',{'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'EmpinfoForm':EmpinfoForm})
        show2='no'
        return render(request,'showEmp.html',{'employee':mydata,'profile':profile,'date':current_date,'dayname':dayname,'emailform':emailform,'EmpinfoForm':EmpinfoForm,'show2':show2})  

def viewall(req):
    return redirect('/adminMEdashboard')

def sendemail2(request):
    eid=request.session['eid']
    myrow=Admininfo.objects.filter(eid=eid)
    for obj in myrow:
        ename=obj.ename
    subject=f"Message from {ename}, Admin, SSGC"
    if request.method=='POST':
        rec=request.POST['rec']
        email=request.POST['email']

    msg=email
    send_mail(
    subject,
    msg,
    "ssgcmanager90@gmail.com",
    [rec],
    fail_silently=False,)
    messages.success(request,'Message sent Successfully!')
    return redirect('adminATTdashboard')

def sendemail22(request):
    eid=request.session['eid']
    myrow=Admininfo.objects.filter(eid=eid)
    for obj in myrow:
        ename=obj.ename
    subject=f"Message from {ename}, Admin, SSGC"
    if request.method=='POST':
        rec=request.POST['rec']
        email=request.POST['email']

    msg=email
    send_mail(
    subject,
    msg,
    "ssgcmanager90@gmail.com",
    [rec],
    fail_silently=False,)
    messages.success(request,'Message sent Successfully!')
    return redirect('adminMEdashboard')

def index(req):
    return render(req, 'index.html')