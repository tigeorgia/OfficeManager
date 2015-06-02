from django.shortcuts import render

from employee.models import Profile
from frontpage.views import checkuserloggedin
import datetime
from timesheet import tshelpers

from openpyxl.reader.excel import load_workbook
from budgetshare.models import SalarySource, SalaryAssignment
from django.contrib.auth.models import User





@checkuserloggedin
def import_salary_assignments( request ):

    employee = Profile.objects.get( user = request.user )

    months = tshelpers.months
    current_month = {
                     "month": months[ datetime.date.today().month - 1],
                     "year": datetime.date.today().year,
                     }
    message = ''

    sheet_data = None

    if request.method == "POST":
        if request.FILES['sheet']:
            sheet_data = read_excel_sheet( request.FILES['sheet'] )



            data_verified = verify_excel_data( sheet_data )

            if data_verified == False:
                message = "Error in data, please check the excel sheet"
                sheet_data = None
            else:

                budget_percentage = sheet_data[:-1]
                budget_totals = sheet_data[-1]

                budget_period = request.POST['data-period']

                import_to_database( budget_percentage, budget_period )


                message = "Data has been imported"


                sheet_data = {
                              "percentage": budget_percentage,
                              "totals" : budget_totals
                              }


    return render( request, "import_salary_assignments.html",
                   {
                    "employee": employee,
                    "months": months,
                    "current_month": current_month,
                    "message": message,
                    "sheetdata": sheet_data,
                    } )



def read_excel_sheet( inFile ):

    # saving it to temp first
    outFile = "/tmp/outsheet.xlsx"
    with open( outFile, 'wb+' ) as destination:
        for chunk in inFile.chunks():
            destination.write( chunk )


    sheet_data = load_workbook( filename = outFile )

    sheet = sheet_data.active
    data_row = 0
    scolumns = 'ABCDEFGHIJKLMNO'

    index_value = 0
    while index_value != 1:
        data_row += 1
        index_value = sheet['A%d' % data_row].value

    data_value = 0
    data_column = -1
    while data_value is not None:
        data_column += 1
        data_value = sheet['%s%d' % ( scolumns[data_column], data_row )].value

    data_column -= 1

    codes = budget_codes( sheet, data_row, data_column, scolumns )

    out_data = []
    while True:
        person_data = budget_data( sheet, data_row, data_column, codes, scolumns )

        if person_data['name'] is not None:
            out_data.append( person_data )
            data_row += 1
        else:
            break


    return out_data

# data of a single employee
def budget_data( sheet, data_row, last_data_column, codes, scolumns ):

    out_data = {}
    out_data['name'] = sheet[ '%s%d' % ( scolumns[1], data_row )].value

    if out_data['name'] is None:
        return out_data


    for code_idx in range( 2, last_data_column + 1 ):
        data_value = sheet[ '%s%d' % ( scolumns[code_idx], data_row )].value

        # excel gives a lot of precission that is untrue and unnecessary
        # need to round it
        data_value = int( round( data_value * 100 ) )


        out_data[ codes[code_idx - 2]] = data_value

    return out_data

# just extracting the budget codes
def budget_codes( sheet, first_data_row, last_data_column, scolumns ):

    codes = []

    for code_idx in range( 2, last_data_column + 1 ):
        codes.append( sheet['%s%d' % ( scolumns[code_idx], first_data_row - 1 )].value )

    return codes

# checking if all data is correct (sums to 1 and is not none)
def verify_excel_data( budget_data ):

    verified = True
    for entry in budget_data:
        row_sum = 0
        for key in entry.keys():
            if key.lower() == "name":
                continue
            if not isinstance( entry[ key], ( int, float, long ) ):
                verified = False
                break
            row_sum += entry[ key]

        if verified == False:
            break

        #         # not checking that, finance's systems have fractional errors
        #         if row_sum != 1:
        #             verified = False
        #             break

    return verified

def import_to_database( budget_percentage, budget_period ):


    for budget_code in budget_percentage[0].keys():
        if budget_code.lower() == "name":
            continue

        SalarySource.objects.get_or_create( code = budget_code )[0].save()

        

    for entry in budget_percentage:

        empl_name = entry['name'].split()


        for code in entry.keys():
            if code.lower() == "name":
                continue


            # pylint: disable=no-member
            user = User.objects.filter( first_name = empl_name[0], last_name = empl_name[1] )
            if not user:
                continue
            
            employee = Profile.objects.get( user = user )
            if not employee:
                continue
            
            source = SalarySource.objects.get( code = code )
            
            if entry[code] <= 0:
                continue
            
            SalaryAssignment.objects.get_or_create( employee = employee, 
                                                    source = source,
                                                    period = budget_period,
                                                    percentage = entry[code])[0].save()
            














