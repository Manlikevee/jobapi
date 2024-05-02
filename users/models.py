import random

import shortuuid
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.timezone import now
from taggit.managers import TaggableManager

s = shortuuid.ShortUUID(alphabet="0123456789").random(length=10)


# Extending User Model Using a One-To-One Link

class Profile(models.Model):
    Workstatus = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    ProfileStatus = [
        ('pending', 'pending'),
        ('started', 'started'),
        ('underreview', 'underreview'),
        ('rejected', 'rejected')
    ]

    industry_choices = [
        ('Accounting ', 'Accounting '),
        ('Airlines/Aviation', 'Airlines/Aviation'),
        ('Alternative Dispute Resolution', 'Alternative Dispute Resolution'),
        ('Alternative Medicine', 'Alternative Medicine'),
        ('Animation', 'Animation'),
        ('Apparel/Fashion', 'Apparel/Fashion'),
        ('Architecture/Planning', 'Architecture/Planning'),
        ('Arts/Crafts', 'Arts/Crafts'),
        ('Automotive', 'Automotive'),
        ('Aviation/Aerospace', 'Aviation/Aerospace'),
        ('Banking/Mortgage', 'Banking/Mortgage'),
        ('Biotechnology/Greentech', 'Biotechnology/Greentech'),
        ('Broadcast Media', 'Broadcast Media'),
        ('Building Materials', 'Building Materials'),
        ('Business Supplies/Equipment', 'Business Supplies/Equipment'),
        ('Capital Markets/Hedge Fund/Private Equity', 'Capital Markets/Hedge Fund/Private Equity'),
        ('Chemicals', 'Chemicals'),
        ('Civic/Social Organization', 'Civic/Social Organization'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Commercial Real Estate', 'Commercial Real Estate'),
        ('Computer Games', 'Computer Games'),
        ('Computer Hardware', 'Computer Hardware'),
        ('Computer Networking', 'Computer Networking'),
        ('Computer Software/Engineering', 'Computer Software/Engineering'),
        ('Computer/Network Security', 'Computer/Network Security'),
        ('Construction', 'Construction'),
        ('Consumer Electronics', 'Consumer Electronics'),
        ('Consumer Goods', 'Consumer Goods'),
        ('Consumer Services', 'Consumer Services'),
        ('Cosmetics', 'Cosmetics'),
        ('Dairy', 'Dairy'),
        ('Defense/Space', 'Defense/Space'),
        ('Design', 'Design'),
        ('E-Learning', 'E-Learning'),
        ('Education Management', 'Education Management'),
        ('Electrical/Electronic Manufacturing', 'Electrical/Electronic Manufacturing'),
        ('Entertainment/Movie Production', 'Entertainment/Movie Production'),
        ('Environmental Services', 'Environmental Services'),
        ('Events Services', 'Events Services'),
        ('Executive Office', 'Executive Office'),
        ('Facilities Services', 'Facilities Services'),
        ('Farming', 'Farming'),
        ('Financial Services', 'Financial Services'),
        ('Fine Art', 'Fine Art'),
        ('Fishery', 'Fishery'),
        ('Food Production', 'Food Production'),
        ('Food/Beverages', 'Food/Beverages'),
        ('Fundraising', 'Fundraising'),
        ('Furniture', 'Furniture'),
        ('Gambling/Casinos', 'Gambling/Casinos'),
        ('Glass/Ceramics/Concrete', 'Glass/Ceramics/Concrete'),
        ('Government Administration', 'Government Administration'),
        ('Government Relations', 'Government Relations'),
        ('Graphic Design/Web Design', 'Graphic Design/Web Design'),
        ('Health/Fitness', 'Health/Fitness'),
        ('Higher Education/Acadamia', 'Higher Education/Acadamia'),
        ('Hospital/Health Care', 'Hospital/Health Care'),
        ('Hospitality', 'Hospitality'),
        ('Human Resources/HR', 'Human Resources/HR'),
        ('Import/Export', 'Import/Export'),
        ('Individual/Family Services', 'Individual/Family Services'),
        ('Industrial Automation', 'Industrial Automation'),
        ('Information Services', 'Information Services'),
        ('Information Technology/IT', 'Information Technology/IT'),
        ('Insurance', 'Insurance'),
        ('International Affairs', 'International Affairs'),
        ('International Trade/Development', 'International Trade/Development'),
        ('Internet', 'Internet'),
        ('Investment Banking/Venture', 'Investment Banking/Venture'),
        ('Investment Management/Hedge Fund/Private Equity', 'Investment Management/Hedge Fund/Private Equity'),
        ('Judiciary', 'Judiciary'),
        ('Law Enforcement', 'Law Enforcement'),
        ('Law Practice/Law Firms', 'Law Practice/Law Firms'),
        ('Legal Services', 'Legal Services'),
        ('Legislative Office', 'Legislative Office'),
        ('Leisure/Travel', 'Leisure/Travel'),
        ('Library', 'Library'),
        ('Logistics/Procurement', 'Logistics/Procurement'),
        ('Luxury Goods/Jewelry', 'Luxury Goods/Jewelry'),
        ('Machinery', 'Machinery'),
        ('Management Consulting', 'Management Consulting'),
        ('Maritime', 'Maritime'),
        ('Market Research', 'Market Research'),
        ('Marketing/Advertising/Sales', 'Marketing/Advertising/Sales'),
        ('Mechanical or Industrial Engineering', 'Mechanical or Industrial Engineering'),
        ('Media Production', 'Media Production'),
        ('Medical Equipment', 'Medical Equipment'),
        ('Medical Practice', 'Medical Practice'),
        ('Mental Health Care', 'Mental Health Care'),
        ('Military Industry', 'Military Industry'),
        ('Mining/Metals', 'Mining/Metals'),
        ('Motion Pictures/Film', 'Motion Pictures/Film'),
        ('Museums/Institutions', 'Museums/Institutions'),
        ('Music', 'Music'),
        ('Nanotechnology', 'Nanotechnology'),
        ('Newspapers/Journalism', 'Newspapers/Journalism'),
        ('Non-Profit/Volunteering', 'Non-Profit/Volunteering'),
        ('Oil/Energy/Solar/Greentech', 'Oil/Energy/Solar/Greentech'),
        ('Online Publishing', 'Online Publishing'),
        ('Other Industry', 'Other Industry'),
        ('Outsourcing/Offshoring', 'Outsourcing/Offshoring'),
        ('Package/Freight Delivery', 'Package/Freight Delivery'),
        ('Packaging/Containers', 'Packaging/Containers'),
        ('Paper/Forest Products', 'Paper/Forest Products'),
        ('Performing Arts', 'Performing Arts'),
        ('Pharmaceuticals', 'Pharmaceuticals'),
        ('Philanthropy', 'Philanthropy'),
        ('Photography', 'Photography'),
        ('Plastics', 'Plastics'),
        ('Political Organization', 'Political Organization'),
        ('Primary/Secondary Education', 'Primary/Secondary Education'),
        ('Printing', 'Printing'),
        ('Professional Training', 'Professional Training'),
        ('Program Development', 'Program Development'),
        ('Public Relations/PR', 'Public Relations/PR'),
        ('Public Safety', 'Public Safety'),
        ('Publishing Industry', 'Publishing Industry'),
        ('Railroad Manufacture', 'Railroad Manufacture'),
        ('Ranching', 'Ranching'),
        ('Real Estate/Mortgage', 'Real Estate/Mortgage'),
        ('Recreational Facilities/Services', 'Recreational Facilities/Services'),
        ('Religious Institutions', 'Religious Institutions'),
        ('Renewables/Environment', 'Renewables/Environment'),
        ('Research Industry', 'Research Industry'),
        ('Restaurants', 'Restaurants'),
        ('Retail Industry', 'Retail Industry'),
        ('Security/Investigations', 'Security/Investigations'),
        ('Semiconductors', 'Semiconductors'),
        ('Shipbuilding', 'Shipbuilding'),
        ('Sporting Goods', 'Sporting Goods'),
        ('Sports', 'Sports'),
        ('Staffing/Recruiting', 'Staffing/Recruiting'),
        ('Supermarkets', 'Supermarkets'),
        ('Telecommunications', 'Telecommunications'),
        ('Textiles', 'Textiles'),
        ('Think Tanks', 'Think Tanks'),
        ('Tobacco', 'Tobacco'),
        ('Translation/Localization', 'Translation/Localization'),
        ('Transportation', 'Transportation'),
        ('Utilities', 'Utilities'),
        ('Venture Capital/VC', 'Venture Capital/VC'),
        ('Veterinary', 'Veterinary'),
        ('Warehousing', 'Warehousing'),
        ('Wholesale', 'Wholesale'),
        ('Wine/Spirits', 'Wine/Spirits'),
        ('Wireless', 'Wireless'),
        ('Writing/Editing', 'Writing/Editing')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(default=0000, blank=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    phonenumber = models.BigIntegerField(default=234, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, blank=True, choices=Workstatus)
    bvn = models.BigIntegerField(default=0000, blank=True)
    residential_address = models.CharField(blank=True, max_length=600)
    rep_address_1 = models.CharField(blank=True, max_length=600)
    rep_city = models.CharField(blank=True, max_length=600)
    rep_state = models.CharField(blank=True, max_length=600)
    rep_zip = models.CharField(blank=True, max_length=600)
    work_sector = models.CharField(blank=True, max_length=600, choices=industry_choices)
    form_of_id = models.CharField(blank=True, max_length=600)
    id_number = models.BigIntegerField(default=0000, blank=True)
    job_title = models.CharField(blank=True, max_length=600)
    country = models.CharField(blank=True, max_length=600)
    city = models.CharField(blank=True, max_length=600)
    region = models.CharField(blank=True, max_length=600)
    profile_verified = models.BooleanField(default=False)
    rc_number = models.CharField(blank=True, max_length=600)
    company_name = models.CharField(blank=True, max_length=600)
    keyman_email = models.EmailField(blank=True, max_length=600)
    keyman_phonenumber = models.BigIntegerField(blank=True, default='234')
    tin = models.CharField(blank=True, max_length=600)
    accountnumber = models.CharField(max_length=100, blank=True)
    profuuid = models.UUIDField(blank=True, max_length=600, null=True)
    profile_status = models.CharField(blank=True, max_length=600, default='pending', choices=ProfileStatus)
    security_lock = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=now, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.accountnumber:
            self.accountnumber = s
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Testmodel(models.Model):
    keyword = models.CharField(blank=True, max_length=600)
    keyword2 = models.CharField(blank=True, max_length=600)

    def __str__(self):
        return self.keyword


class Identification(models.Model):
    Workstatus = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    industry_choices = [
        ('Accounting ', 'Accounting '),
        ('Airlines/Aviation', 'Airlines/Aviation'),
        ('Alternative Dispute Resolution', 'Alternative Dispute Resolution'),
        ('Alternative Medicine', 'Alternative Medicine'),
        ('Animation', 'Animation'),
        ('Apparel/Fashion', 'Apparel/Fashion'),
        ('Architecture/Planning', 'Architecture/Planning'),
        ('Arts/Crafts', 'Arts/Crafts'),
        ('Automotive', 'Automotive'),
        ('Aviation/Aerospace', 'Aviation/Aerospace'),
        ('Banking/Mortgage', 'Banking/Mortgage'),
        ('Biotechnology/Greentech', 'Biotechnology/Greentech'),
        ('Broadcast Media', 'Broadcast Media'),
        ('Building Materials', 'Building Materials'),
        ('Business Supplies/Equipment', 'Business Supplies/Equipment'),
        ('Capital Markets/Hedge Fund/Private Equity', 'Capital Markets/Hedge Fund/Private Equity'),
        ('Chemicals', 'Chemicals'),
        ('Civic/Social Organization', 'Civic/Social Organization'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Commercial Real Estate', 'Commercial Real Estate'),
        ('Computer Games', 'Computer Games'),
        ('Computer Hardware', 'Computer Hardware'),
        ('Computer Networking', 'Computer Networking'),
        ('Computer Software/Engineering', 'Computer Software/Engineering'),
        ('Computer/Network Security', 'Computer/Network Security'),
        ('Construction', 'Construction'),
        ('Consumer Electronics', 'Consumer Electronics'),
        ('Consumer Goods', 'Consumer Goods'),
        ('Consumer Services', 'Consumer Services'),
        ('Cosmetics', 'Cosmetics'),
        ('Dairy', 'Dairy'),
        ('Defense/Space', 'Defense/Space'),
        ('Design', 'Design'),
        ('E-Learning', 'E-Learning'),
        ('Education Management', 'Education Management'),
        ('Electrical/Electronic Manufacturing', 'Electrical/Electronic Manufacturing'),
        ('Entertainment/Movie Production', 'Entertainment/Movie Production'),
        ('Environmental Services', 'Environmental Services'),
        ('Events Services', 'Events Services'),
        ('Executive Office', 'Executive Office'),
        ('Facilities Services', 'Facilities Services'),
        ('Farming', 'Farming'),
        ('Financial Services', 'Financial Services'),
        ('Fine Art', 'Fine Art'),
        ('Fishery', 'Fishery'),
        ('Food Production', 'Food Production'),
        ('Food/Beverages', 'Food/Beverages'),
        ('Fundraising', 'Fundraising'),
        ('Furniture', 'Furniture'),
        ('Gambling/Casinos', 'Gambling/Casinos'),
        ('Glass/Ceramics/Concrete', 'Glass/Ceramics/Concrete'),
        ('Government Administration', 'Government Administration'),
        ('Government Relations', 'Government Relations'),
        ('Graphic Design/Web Design', 'Graphic Design/Web Design'),
        ('Health/Fitness', 'Health/Fitness'),
        ('Higher Education/Acadamia', 'Higher Education/Acadamia'),
        ('Hospital/Health Care', 'Hospital/Health Care'),
        ('Hospitality', 'Hospitality'),
        ('Human Resources/HR', 'Human Resources/HR'),
        ('Import/Export', 'Import/Export'),
        ('Individual/Family Services', 'Individual/Family Services'),
        ('Industrial Automation', 'Industrial Automation'),
        ('Information Services', 'Information Services'),
        ('Information Technology/IT', 'Information Technology/IT'),
        ('Insurance', 'Insurance'),
        ('International Affairs', 'International Affairs'),
        ('International Trade/Development', 'International Trade/Development'),
        ('Internet', 'Internet'),
        ('Investment Banking/Venture', 'Investment Banking/Venture'),
        ('Investment Management/Hedge Fund/Private Equity', 'Investment Management/Hedge Fund/Private Equity'),
        ('Judiciary', 'Judiciary'),
        ('Law Enforcement', 'Law Enforcement'),
        ('Law Practice/Law Firms', 'Law Practice/Law Firms'),
        ('Legal Services', 'Legal Services'),
        ('Legislative Office', 'Legislative Office'),
        ('Leisure/Travel', 'Leisure/Travel'),
        ('Library', 'Library'),
        ('Logistics/Procurement', 'Logistics/Procurement'),
        ('Luxury Goods/Jewelry', 'Luxury Goods/Jewelry'),
        ('Machinery', 'Machinery'),
        ('Management Consulting', 'Management Consulting'),
        ('Maritime', 'Maritime'),
        ('Market Research', 'Market Research'),
        ('Marketing/Advertising/Sales', 'Marketing/Advertising/Sales'),
        ('Mechanical or Industrial Engineering', 'Mechanical or Industrial Engineering'),
        ('Media Production', 'Media Production'),
        ('Medical Equipment', 'Medical Equipment'),
        ('Medical Practice', 'Medical Practice'),
        ('Mental Health Care', 'Mental Health Care'),
        ('Military Industry', 'Military Industry'),
        ('Mining/Metals', 'Mining/Metals'),
        ('Motion Pictures/Film', 'Motion Pictures/Film'),
        ('Museums/Institutions', 'Museums/Institutions'),
        ('Music', 'Music'),
        ('Nanotechnology', 'Nanotechnology'),
        ('Newspapers/Journalism', 'Newspapers/Journalism'),
        ('Non-Profit/Volunteering', 'Non-Profit/Volunteering'),
        ('Oil/Energy/Solar/Greentech', 'Oil/Energy/Solar/Greentech'),
        ('Online Publishing', 'Online Publishing'),
        ('Other Industry', 'Other Industry'),
        ('Outsourcing/Offshoring', 'Outsourcing/Offshoring'),
        ('Package/Freight Delivery', 'Package/Freight Delivery'),
        ('Packaging/Containers', 'Packaging/Containers'),
        ('Paper/Forest Products', 'Paper/Forest Products'),
        ('Performing Arts', 'Performing Arts'),
        ('Pharmaceuticals', 'Pharmaceuticals'),
        ('Philanthropy', 'Philanthropy'),
        ('Photography', 'Photography'),
        ('Plastics', 'Plastics'),
        ('Political Organization', 'Political Organization'),
        ('Primary/Secondary Education', 'Primary/Secondary Education'),
        ('Printing', 'Printing'),
        ('Professional Training', 'Professional Training'),
        ('Program Development', 'Program Development'),
        ('Public Relations/PR', 'Public Relations/PR'),
        ('Public Safety', 'Public Safety'),
        ('Publishing Industry', 'Publishing Industry'),
        ('Railroad Manufacture', 'Railroad Manufacture'),
        ('Ranching', 'Ranching'),
        ('Real Estate/Mortgage', 'Real Estate/Mortgage'),
        ('Recreational Facilities/Services', 'Recreational Facilities/Services'),
        ('Religious Institutions', 'Religious Institutions'),
        ('Renewables/Environment', 'Renewables/Environment'),
        ('Research Industry', 'Research Industry'),
        ('Restaurants', 'Restaurants'),
        ('Retail Industry', 'Retail Industry'),
        ('Security/Investigations', 'Security/Investigations'),
        ('Semiconductors', 'Semiconductors'),
        ('Shipbuilding', 'Shipbuilding'),
        ('Sporting Goods', 'Sporting Goods'),
        ('Sports', 'Sports'),
        ('Staffing/Recruiting', 'Staffing/Recruiting'),
        ('Supermarkets', 'Supermarkets'),
        ('Telecommunications', 'Telecommunications'),
        ('Textiles', 'Textiles'),
        ('Think Tanks', 'Think Tanks'),
        ('Tobacco', 'Tobacco'),
        ('Translation/Localization', 'Translation/Localization'),
        ('Transportation', 'Transportation'),
        ('Utilities', 'Utilities'),
        ('Venture Capital/VC', 'Venture Capital/VC'),
        ('Veterinary', 'Veterinary'),
        ('Warehousing', 'Warehousing'),
        ('Wholesale', 'Wholesale'),
        ('Wine/Spirits', 'Wine/Spirits'),
        ('Wireless', 'Wireless'),
        ('Writing/Editing', 'Writing/Editing')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100, blank=True, choices=Workstatus)
    bvn = models.BigIntegerField(default=0000, blank=True)
    residential_address = models.CharField(blank=True, max_length=600)
    country = models.CharField(blank=False, max_length=600)
    rep_city = models.CharField(blank=False, max_length=600)
    rep_state = models.CharField(blank=False, max_length=600)
    work_sector = models.CharField(blank=False, max_length=600, choices=industry_choices)
    form_of_id = models.CharField(blank=False, max_length=600)
    id_number = models.BigIntegerField(default=0000, blank=True)


class workexperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobtitle = models.CharField(blank=True, max_length=600)
    jobservice = models.CharField(blank=True, max_length=600)
    jobsector = models.CharField(blank=True, max_length=600)
    jobstart = models.DateField(default=now)
    jobend = models.DateField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    jobdescription = models.TextField(blank=True, max_length=6000)

    def __str__(self):
        return self.user.username


class Jobs(models.Model):
    industry_choices = [
        ('Accounting ', 'Accounting '),
        ('Airlines/Aviation', 'Airlines/Aviation'),
        ('Alternative Dispute Resolution', 'Alternative Dispute Resolution'),
        ('Alternative Medicine', 'Alternative Medicine'),
        ('Animation', 'Animation'),
        ('Apparel/Fashion', 'Apparel/Fashion'),
        ('Architecture/Planning', 'Architecture/Planning'),
        ('Arts/Crafts', 'Arts/Crafts'),
        ('Automotive', 'Automotive'),
        ('Aviation/Aerospace', 'Aviation/Aerospace'),
        ('Banking/Mortgage', 'Banking/Mortgage'),
        ('Biotechnology/Greentech', 'Biotechnology/Greentech'),
        ('Broadcast Media', 'Broadcast Media'),
        ('Building Materials', 'Building Materials'),
        ('Business Supplies/Equipment', 'Business Supplies/Equipment'),
        ('Capital Markets/Hedge Fund/Private Equity', 'Capital Markets/Hedge Fund/Private Equity'),
        ('Chemicals', 'Chemicals'),
        ('Civic/Social Organization', 'Civic/Social Organization'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Commercial Real Estate', 'Commercial Real Estate'),
        ('Computer Games', 'Computer Games'),
        ('Computer Hardware', 'Computer Hardware'),
        ('Web Development', 'Web Development'),
        ('FrontEnd Development', 'FrontEnd Development'),
        ('BackEnd Development', 'BackEnd Development'),
        ('Computer Networking', 'Computer Networking'),
        ('Computer Software/Engineering', 'Computer Software/Engineering'),
        ('Computer/Network Security', 'Computer/Network Security'),
        ('Construction', 'Construction'),
        ('Consumer Electronics', 'Consumer Electronics'),
        ('Consumer Goods', 'Consumer Goods'),
        ('Consumer Services', 'Consumer Services'),
        ('Cosmetics', 'Cosmetics'),
        ('Dairy', 'Dairy'),
        ('Defense/Space', 'Defense/Space'),
        ('Design', 'Design'),
        ('E-Learning', 'E-Learning'),
        ('Education Management', 'Education Management'),
        ('Electrical/Electronic Manufacturing', 'Electrical/Electronic Manufacturing'),
        ('Entertainment/Movie Production', 'Entertainment/Movie Production'),
        ('Environmental Services', 'Environmental Services'),
        ('Events Services', 'Events Services'),
        ('Executive Office', 'Executive Office'),
        ('Facilities Services', 'Facilities Services'),
        ('Farming', 'Farming'),
        ('Financial Services', 'Financial Services'),
        ('Fine Art', 'Fine Art'),
        ('Fishery', 'Fishery'),
        ('Food Production', 'Food Production'),
        ('Food/Beverages', 'Food/Beverages'),
        ('Fundraising', 'Fundraising'),
        ('Furniture', 'Furniture'),
        ('Gambling/Casinos', 'Gambling/Casinos'),
        ('Glass/Ceramics/Concrete', 'Glass/Ceramics/Concrete'),
        ('Government Administration', 'Government Administration'),
        ('Government Relations', 'Government Relations'),
        ('Graphic Design/Web Design', 'Graphic Design/Web Design'),
        ('Health/Fitness', 'Health/Fitness'),
        ('Higher Education/Acadamia', 'Higher Education/Acadamia'),
        ('Hospital/Health Care', 'Hospital/Health Care'),
        ('Hospitality', 'Hospitality'),
        ('Human Resources/HR', 'Human Resources/HR'),
        ('Import/Export', 'Import/Export'),
        ('Individual/Family Services', 'Individual/Family Services'),
        ('Industrial Automation', 'Industrial Automation'),
        ('Information Services', 'Information Services'),
        ('Information Technology/IT', 'Information Technology/IT'),
        ('Insurance', 'Insurance'),
        ('International Affairs', 'International Affairs'),
        ('International Trade/Development', 'International Trade/Development'),
        ('Internet', 'Internet'),
        ('Investment Banking/Venture', 'Investment Banking/Venture'),
        ('Investment Management/Hedge Fund/Private Equity', 'Investment Management/Hedge Fund/Private Equity'),
        ('Judiciary', 'Judiciary'),
        ('Law Enforcement', 'Law Enforcement'),
        ('Law Practice/Law Firms', 'Law Practice/Law Firms'),
        ('Legal Services', 'Legal Services'),
        ('Legislative Office', 'Legislative Office'),
        ('Leisure/Travel', 'Leisure/Travel'),
        ('Library', 'Library'),
        ('Logistics/Procurement', 'Logistics/Procurement'),
        ('Luxury Goods/Jewelry', 'Luxury Goods/Jewelry'),
        ('Machinery', 'Machinery'),
        ('Management Consulting', 'Management Consulting'),
        ('Maritime', 'Maritime'),
        ('Market Research', 'Market Research'),
        ('Marketing/Advertising/Sales', 'Marketing/Advertising/Sales'),
        ('Mechanical or Industrial Engineering', 'Mechanical or Industrial Engineering'),
        ('Media Production', 'Media Production'),
        ('Medical Equipment', 'Medical Equipment'),
        ('Medical Practice', 'Medical Practice'),
        ('Mental Health Care', 'Mental Health Care'),
        ('Military Industry', 'Military Industry'),
        ('Mining/Metals', 'Mining/Metals'),
        ('Motion Pictures/Film', 'Motion Pictures/Film'),
        ('Museums/Institutions', 'Museums/Institutions'),
        ('Music', 'Music'),
        ('Nanotechnology', 'Nanotechnology'),
        ('Newspapers/Journalism', 'Newspapers/Journalism'),
        ('Non-Profit/Volunteering', 'Non-Profit/Volunteering'),
        ('Oil/Energy/Solar/Greentech', 'Oil/Energy/Solar/Greentech'),
        ('Online Publishing', 'Online Publishing'),
        ('Other Industry', 'Other Industry'),
        ('Outsourcing/Offshoring', 'Outsourcing/Offshoring'),
        ('Package/Freight Delivery', 'Package/Freight Delivery'),
        ('Packaging/Containers', 'Packaging/Containers'),
        ('Paper/Forest Products', 'Paper/Forest Products'),
        ('Performing Arts', 'Performing Arts'),
        ('Pharmaceuticals', 'Pharmaceuticals'),
        ('Philanthropy', 'Philanthropy'),
        ('Photography', 'Photography'),
        ('Plastics', 'Plastics'),
        ('Political Organization', 'Political Organization'),
        ('Primary/Secondary Education', 'Primary/Secondary Education'),
        ('Printing', 'Printing'),
        ('Professional Training', 'Professional Training'),
        ('Program Development', 'Program Development'),
        ('Public Relations/PR', 'Public Relations/PR'),
        ('Public Safety', 'Public Safety'),
        ('Publishing Industry', 'Publishing Industry'),
        ('Railroad Manufacture', 'Railroad Manufacture'),
        ('Ranching', 'Ranching'),
        ('Real Estate/Mortgage', 'Real Estate/Mortgage'),
        ('Recreational Facilities/Services', 'Recreational Facilities/Services'),
        ('Religious Institutions', 'Religious Institutions'),
        ('Renewables/Environment', 'Renewables/Environment'),
        ('Research Industry', 'Research Industry'),
        ('Restaurants', 'Restaurants'),
        ('Retail Industry', 'Retail Industry'),
        ('Security/Investigations', 'Security/Investigations'),
        ('Semiconductors', 'Semiconductors'),
        ('Shipbuilding', 'Shipbuilding'),
        ('Sporting Goods', 'Sporting Goods'),
        ('Sports', 'Sports'),
        ('Staffing/Recruiting', 'Staffing/Recruiting'),
        ('Supermarkets', 'Supermarkets'),
        ('Telecommunications', 'Telecommunications'),
        ('Textiles', 'Textiles'),
        ('Think Tanks', 'Think Tanks'),
        ('Tobacco', 'Tobacco'),
        ('Translation/Localization', 'Translation/Localization'),
        ('Transportation', 'Transportation'),
        ('Utilities', 'Utilities'),
        ('Venture Capital/VC', 'Venture Capital/VC'),
        ('Veterinary', 'Veterinary'),
        ('Warehousing', 'Warehousing'),
        ('Wholesale', 'Wholesale'),
        ('Wine/Spirits', 'Wine/Spirits'),
        ('Wireless', 'Wireless'),
        ('Writing/Editing', 'Writing/Editing')
    ]

    SALARY_RANGE = [
        ('< 100', '< 100'),
        ('100-200', '100-200'),
        ('200-300', '200-300'),
        ('300-400', '300-400'),
        ('500-600', '500-600'),
        ('500 >', '500 >'),
    ]
    Work_Level = [
        ('Junior Level', 'Junior Level'),
        ('Intermediate Level', 'Intermediate Level'),
        ('Senior Level', 'Senior Level'),
        ('Expert Level', 'Expert Level'),
    ]
    employmenttype = [
        ('Intern', 'Intern'),
        ('Part-Time', 'Part-Time'),
        ('Full-Time', 'Full-Time'),
    ]
    Workstatus = [
        ('pending confirmation', 'pending confirmation'),
        ('submitted for review', 'submitted for review'),
        ('Awaiting Payment', 'Awaiting Payment'),
        ('confirmed', 'confirmed'),
        ('cancelled', 'cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jobtitle = models.CharField(blank=True, null=True, max_length=600)
    jobidcode = models.PositiveBigIntegerField(blank=True, null=True, default=1)
    jobservice = models.CharField(blank=True, null=True, max_length=600)
    joblocation = models.CharField(blank=True, null=True, max_length=600)
    jobcategory = models.CharField(blank=True, null=True, max_length=600, choices=industry_choices)
    jobemploymenttype = models.CharField(blank=True, null=True, max_length=600, choices=employmenttype)
    jobsalaryrange = models.CharField(blank=True, null=True, max_length=600, choices=SALARY_RANGE)
    jobmaximumapplication = models.CharField(blank=True, null=True, max_length=600)
    applicationenddate = models.DateTimeField(default=now)
    applicationpublish = models.DateTimeField(default=now)
    jobpostdate = models.DateTimeField(auto_now_add=True)
    jobminimumexperience = models.BigIntegerField(blank=True, null=True, default=2)
    workinglevel = models.CharField(blank=True, null=True, max_length=600, choices=Work_Level)
    jobdescription = models.TextField(blank=True, max_length=600000)
    is_paidfor = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    stage1 = models.BooleanField(default=False)
    stage2 = models.BooleanField(default=False)
    stage3 = models.BooleanField(default=False)
    stage4 = models.BooleanField(default=False)
    status = models.CharField(blank=True, max_length=500, choices=Workstatus, default='pending confirmation')
    payment_data = models.JSONField(blank=True, null=True, default=list)
    likes = models.ManyToManyField(User, related_name='blogpost_like')
    applied = models.ManyToManyField(User, related_name='job_applied')
    last_seen = models.DateTimeField(default=now, null=True, blank=True)
    tags = TaggableManager()

    def number_of_likes(self):
        return self.likes.count()

    def number_of_applied(self):
        return self.applied.count()

    def __str__(self):
        return self.user.username


class Jobsalert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(blank=True, max_length=600)

    def __str__(self):
        return self.user.username


class jsonfolder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    testj = models.JSONField(null=True)

    def __str__(self):
        return self.user.username


class messagestarter(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recievers')
    messageid = models.BigIntegerField(null=True)
    messagetime = models.DateTimeField(default=now)
    message = models.TextField(blank=True, null=True)
    mymessages = models.JSONField(blank=True, null=True, default=list)

    def __str__(self):
        return self.sender.username


class messagefolder(models.Model):
    messageid = models.OneToOneField(messagestarter, on_delete=models.CASCADE)
    lastupdated = models.DateTimeField(auto_now=True)
    testj = models.JSONField(blank=True, null=True, default=list)

    def __str__(self):
        return self.messageid.sender.username


class postings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='blog_posts', max_length=500)
    messageid = models.BigIntegerField(null=True)
    messagetime = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_like')
    testj = models.JSONField(blank=True, null=True, default=list)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.user.username


class PaymentDetails(models.Model):
    requestuser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorization_code = models.CharField(max_length=100, blank=True)
    authorization_data = models.JSONField()
    authorization_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.requestuser.username


class jobfeatures(models.Model):
    user = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    feature = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.jobtitle


class Status(models.Model):
    Accounttype = [
        ('individual', 'individual'),
        ('Recruiter', 'Recruiter'),
        ('none', 'none')
    ]

    requestuser = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=100, default='individual', choices=Accounttype)
    application_status = models.CharField(max_length=100, default='pending')
    stage_1 = models.BooleanField(default=False)
    stage_2 = models.BooleanField(default=False)
    stage_3 = models.BooleanField(default=False)
    stage_4 = models.BooleanField(default=False)
    stage_5 = models.BooleanField(default=False)
    stage_6 = models.BooleanField(default=False)
    stage_7 = models.BooleanField(default=False)
    stage_9 = models.BooleanField(default=False)
    stage_8 = models.BooleanField(default=False)

    def __str__(self):
        return self.requestuser.username


class Userplan(models.Model):
    planname = models.CharField(max_length=100, default='BASIC PLAN', null=True)
    Planprice = models.BigIntegerField(default=0, null=True)
    plandescription = models.CharField(max_length=100, default='BASIC PLAN', null=True)

    def __str__(self):
        return self.planname


class UserMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Userplan, related_name='user_membership', on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=False)
    start_at = models.DateField(default=now)
    end_at = models.DateField(default=now)

    def __str__(self):
        return self.user.username


class exceltest(models.Model):
    institution = models.CharField(max_length=350, blank=True, null=True)
    Type = models.CharField(max_length=750, blank=True, null=True)
    Acronym = models.CharField(max_length=750, blank=True, null=True)
    Ownership = models.CharField(max_length=750, blank=True, null=True)
    Url = models.CharField(max_length=750, blank=True, null=True)
    logourl = models.CharField(max_length=750, blank=True, null=True)
    Year = models.CharField(max_length=750, blank=True, null=True)

    def __str__(self):
        return self.institution


class University(models.Model):
    DegreeType = [
        ('Associate degree', 'Associate degree'),
        ('Bachelor degree', 'Bachelor degree'),
        ('Master degree', 'Master degree'),
        ('Doctoral degree', 'Doctoral degree'),
        ('Master degree', 'Master degree'),
        ('Diploma degree', 'Diploma degree'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.ForeignKey(exceltest, on_delete=models.CASCADE)
    course = models.CharField(blank=True, max_length=600)
    degree = models.CharField(blank=True, max_length=600, choices=DegreeType)
    start_date = models.DateField(default=now)
    finish_date = models.DateField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Areaofexp(models.Model):
    areaofexperties = models.CharField(max_length=750, blank=True, null=True)

    def __str__(self):
        return self.areaofexperties


class Personaldetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv = models.FileField(blank=True, null=True, upload_to='usercv')
    profilephoto = models.FileField(blank=True, null=True, upload_to='profile_images')
    utilitybill = models.FileField(blank=True, null=True, upload_to='utilitybill')
    biography = models.TextField(blank=True, null=True, max_length=6000)
    aoexp = models.ManyToManyField(Areaofexp, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class Question(models.Model):
    choice = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=250)
    answer = models.CharField(max_length=100)
    option_one = models.CharField(max_length=100)
    option_two = models.CharField(max_length=100)
    option_three = models.CharField(max_length=100, blank=True)
    option_four = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Applications(models.Model):
    ProfileStatus = [
        ('pending', 'pending'),
        ('started', 'started'),
        ('underreview', 'underreview'),
        ('rejected', 'rejected')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_user')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_author')
    application_id = models.BigIntegerField(default=0, null=True)
    application_status = models.CharField(max_length=100, choices=ProfileStatus, default='pending')
    jobapplied = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.application_status


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    image = CloudinaryField(resource_type='auto')
    extradetails = models.JSONField(blank=True, null=True, default=list)


class employees(models.Model):
    Workstatus = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    created_at = models.DateField(default=now)
    phone_number = models.BigIntegerField(default=234, blank=True)
    gender = models.CharField(max_length=100, blank=True, choices=Workstatus)
    staff_id = models.CharField(max_length=100, blank=True)
    availability = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = s
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name


class visitorslog(models.Model):
    Workstatus = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    ref = models.BigIntegerField(blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    phonenumber = models.BigIntegerField(default=234, blank=True)
    created_at = models.DateTimeField(default=now)
    clock_in = models.DateTimeField(default=now)
    clock_out = models.DateTimeField(default=now)
    staff_id = models.ForeignKey(employees, on_delete=models.CASCADE)
    tag_id = models.CharField(max_length=100, blank=True)

    reason = models.CharField(max_length=100, blank=True)
    visitation_type = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True, default='awaiting_confirmation')
    availability = models.CharField(max_length=100, blank=True)
    is_resheduled = models.BooleanField(default=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.ref:
            # Generate a positive random number within the range of a BigIntegerField
            self.ref = random.randint(1, 9223372036854775807)  # Maximum positive value for a BigIntegerField
            # Ensure uniqueness
            while visitorslog.objects.filter(ref=self.ref).exists():
                self.ref = random.randint(1, 9223372036854775807)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name


class qrcodes(models.Model):
    code_tag = models.CharField(max_length=100, blank=True)
    created_at = models.DateField(default=now)
    availability = models.BooleanField(default=True)
    used_by = models.ForeignKey(visitorslog, null=True, blank=True, on_delete=models.SET_NULL)
    usage_history = models.JSONField(blank=True, null=True, default=list)

    def __str__(self):
        return self.code_tag
