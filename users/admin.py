from django.contrib import admin
from .models import Profile, workexperience, Personaldetails, Jobsalert, messagestarter, messagefolder, Jobs, \
    PaymentDetails, jobfeatures, Userplan, exceltest, Areaofexp, Category, Question, UserMembership, exceltest, UploadedImage, postings
# Register your models here.


admin.site.register(Profile)
admin.site.register(workexperience)
admin.site.register(Personaldetails)
admin.site.register(Jobsalert)
admin.site.register(messagestarter)
admin.site.register(messagefolder)
admin.site.register(Jobs)
admin.site.register(PaymentDetails)
admin.site.register(jobfeatures)
admin.site.register(Userplan)
admin.site.register(UserMembership)
admin.site.register(exceltest)
admin.site.register(UploadedImage)
admin.site.register(postings)
