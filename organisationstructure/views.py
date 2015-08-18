from django.shortcuts import render
from employee.models import Profile
from django.db.models import F
from employee.views import checkuserloggedin

@checkuserloggedin
def organisationstructure( request, employee ):

    structure = []

    profiles = Profile.objects.filter( supervisor = F( 'user' ) )

    for profile in profiles:
        structure.append( underlings( profile ) )


    htmlstruct = generatehtml( structure )



    return render( request,
                   'org_structure.html',
                   { 
                    'employee': employee,
                    'structure':structure,
                    'htmlstruct': htmlstruct
                    } )


def generatehtml( structure, arrow = False, level = 0 ):

    html = '<ul class="empl-list">'
    
    for element in structure:
        profile = element['profile']
        if level == 0:
            imagestr = ''
        else:
            imagestr = '<img alt="arrow" src="officemanager/static/images/arrow.png" ></img>'
            
        html += '<li class="empl-item">%s %s %s - %s</li>' % ( imagestr, profile.user.first_name, profile.user.last_name, profile.position)
        
        
        
        #         if arrow:
        #             html += '%s<img alt="arrow" src="officemanager/static/images/arrow.png" ></img>' % ( '<span class="spaces"></span>' * (2 * level))
        #         html +=  '<span class="employee-item">&nbsp; %s %s - %s</span><br>' % ( profile.user.first_name, profile.user.last_name, profile.position)
        
        if element.has_key('underlings'):
            html += generatehtml( element['underlings'], True, level + 1)


    html += "</ul>"
    return html


def underlings( profile ):

    subprofiles = Profile.objects.filter( supervisor = profile.user )

    if subprofiles.count() == 1 and subprofiles[0].supervisor == subprofiles[0].user:
        return {'profile': profile}

    subordinates = []

    for underling in subprofiles:
        if underling == profile:
            continue
        subordinates.append( underlings( underling ) )

    if len( subordinates ) == 0:
        return {'profile' : profile}
    else:
        return {'profile' : profile, 'underlings': subordinates}
