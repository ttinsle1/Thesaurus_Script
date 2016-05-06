#!/usr/bin/env python
import re
import csv
dict_index_column = {}
dps = {}

"""
Opens the deconcatenated dict, and reads each field into a dictionary.
dps is a dictionary of dictionary, where the key's are the ADID and the
values are a dictionary of each barcode.
"""
with open ('Thesaurus 3376+TT.txt', 'U') as infile:
    master = csv.reader(infile,delimiter= '\t')
    for row in master:
        for i in range(len(row)):
            dict_index_column[i] = row[i]
        break

    for row in master:
        if row[0] == 'ADID' or None:
            next
        else:
            dp = {}
            for i in range(len(row)):
                dp[dict_index_column[i]] = row[i]
            dps[row[0]] = dp

output = open('Thesaurus 3376+TT_Output.txt', 'w')
writer =  csv.writer(output, delimiter = '\t')


dict_column_index = {v:k for k,v in dict_index_column.iteritems()}
writer.writerow(sorted(dict_column_index, key=dict_column_index.get))


"""
Iterates through dps and assign a thesaurus code and Description.
"""
#DIV TYPES>>>>> FUQQQQQ
for dp in dps.values():
    #Assigns to C Bucket
    if re.search(r'(C[123]i+|Cdiv|C[123]div)', dp['EL IO']) or 'C' in dp['EL Obj']:
        #Tier 2
        if dp['EL Product'] == 'RP':
            #Tier 3
            if re.search(r'C2i+', dp['EL Obj']):
                dp['GLT_tag'] = '3A1'
                dp['GLT_Desc'] = 'Information Products meant to inform'
            elif re.search(r'C3i+', dp['EL Obj']):
                dp['GLT_tag'] = '3A2'
                dp['GLT_Desc'] = 'Information Products meant to influence'
            elif re.search(r'C4i+', dp['EL Obj']):
                dp['GLT_tag'] = '3A3'
                dp['GLT_Desc'] = 'Information Products meant to command'
            else:
                dp['GLT_tag'] = '3A'
                dp['GLT_Desc'] = 'Information Resource Products'
        #Tier 2
        elif dp['EL Product'] == "AP":
            if re.search(r'1\.1\.\d', dp['EL Act']):
                dp['GLT_tag'] = '3B1'
                dp['GLT_Desc'] = 'Procurement related services'
            elif re.search(r'1\.2\.\d', dp['EL Act']):
                dp['GLT_tag'] = '3B2'
                dp['GLT_Desc'] = 'Information Transportation related services'
            elif dp['EL Act'] == '1.3.1':
                dp['GLT_tag'] = '3B3'
                dp['GLT_Desc'] = 'Security Services'
            elif dp['EL Act'] == '1.3.3' and dp['EL Obj'] == 'F':
                dp['GLT_tag'] = '3B4'
                dp['GLT_Desc'] = 'Outsourced HR'
            elif dp['EL Act'] == '2.1.2':
                dp['GLT_tag'] = '3B5'
                dp['GLT_Desc'] = 'Design Related Services'
            elif dp['EL Act'] == '2.2.2':
                dp['GLT_tag'] = '3B6'   #I think there is a loophole here. A code with IO but not C object will end up here, but not be contract printing?
                dp['GLT_Desc'] = 'Contract Printing'
            elif re.search(r'2\.3\.\d', dp['EL Act']):
                dp['GLT_tag'] = '3B7'
                dp['GLT_Desc'] = 'Quality control related services'
            elif dp['EL Act'] == '3.1.1':
                dp['GLT_tag'] = '3B8'
                dp['GLT_Desc'] = 'Advertising or Market Research'
            elif re.search(r'4\.\d\.\d', dp['EL Act']):
                dp['GLT_tag'] = '3B9'
                dp['GLT_Desc'] = 'Consulting related services'
            elif dp['EL Act'] == '1.3.2':
                dp['GLT_tag'] = '3B10'
                dp['GLT_Desc'] = 'Information Storage Services'
            elif dp['EL Act'] == '2.1.1':
                dp['GLT_tag'] = '3B11'
                dp['GLT_Desc'] = 'Research services'
            elif dp['EL Act'] == '3.3.3':
                dp['GLT_tag'] = '3B12'
                dp['GLT_Desc'] = 'Custodian Banking'
            else:
                dp['GLT_tag'] = '3B'
                dp['GLT_Desc'] = 'Information Activity Products'
        else:
            dp['GLT_tag'] = '3'
            dp['GLT_Desc'] = 'Information'
    #Assigns to A Bucket
    elif re.search(r'A\w+', dp['EL Obj']):
            #TIER 2
            if dp['EL Product'] == 'RP':
                #TIER 3
                if dp['EL Act'] == '2.2.2':
                    #TIER 4
                    if '(A4ii) 1.3.2' in dp['WG1'] or dp['WG2']:
                        dp['GLT_tag'] = '1A1.A'
                        dp['GLT_Desc'] = 'Storage Space Developers'
                    elif ('2.1.1 E' in dp['WG1'] or dp['WG2']) and re.search(r'E4\w{1-3}\s2\.3\.2', dp['CofC FR1']):
                        dp['GLT_tag'] = '1A1.B'
                        dp['GLT_Desc'] = 'Medical Research Facilities Developers'
                    elif re.search(r'\(\W\di+\)\s2\.2\.2\sF', dp['WG1']) or re.search(r'\(\W\di+\)\s2\.2\.2\sF', dp['WG2']):
                        dp['GLT_tag'] = '1A1.C'
                        dp['GLT_Desc'] = 'Event Space Developers'
                    elif re.search(r'3\.1\.2', dp['WG1']) or re.search(r'3\.1\.2', dp['WG2']):
                        dp['GLT_tag'] = '1A1.D'
                        dp['GLT_Desc'] = 'Developers of Retail Space'
                    elif re.search(r'2\.3\.2\sF', dp['WG1']) or re.search(r'2\.3\.2\sF', dp['WG1']):
                        dp['GLT_tag'] = '1A1.E'
                        dp['GLT_Desc'] = 'Developers of Medical Treatment Space'
                    elif re.search(r'2\.2\.2\s[ABCDE]', dp['WG1']) or re.search(r'2\.2\.2\s[ABCDE]', dp['WG2']):
                        dp['GLT_tag'] = '1A1.F'
                        dp['GLT_Desc'] = 'Developers of Production Space'
                    elif re.search(r'\(A4ii\)\s1\.2\.3', dp['WG1']) or re.search(r'\(A4ii\)\s1\.2\.3', dp['WG2']):
                        dp['GLT_tag'] = '1A1.H'
                        dp['GLT_Desc'] = 'Distribution Center Developer'
                    elif 'Div' in dp['WG1'] or dp['WG2']:
                        dp['GLT_tag'] = '1A1.G'
                        dp['GLT_Desc'] = 'Developers of real estate used for Diverse Activities'
                    else:
                        dp['GLT_tag'] = '1A1'
                        dp['GLT_Desc'] = 'Real Estate Developers'
                elif dp['EL Act'] == '1.3.2' or '3.3.2' or '3.1.2':
                    if dp['EL Act'] == '1.3.2':
                        dp['GLT_tag'] = '1A2.A'
                        dp['GLT_Desc'] = 'Real Estate Operators'
                    elif dp['EL Act'] == '3.3.2':
                        dp['GLT_tag'] = '1A2.B'
                        dp['GLT_Desc'] = 'Real Estate Lessors'
                    elif dp['EL Act'] == '3.1.2':
                        dp['GLT_tag'] = '1A2.C'
                        dp['GLT_Desc'] = 'Real Estate Seller'
                    else:
                        dp['GLT_tag'] = '1A2'
                        dp['GLT_Desc'] = 'Real Estate Distributors'
                else:
                    dp['GLT_tag'] = '1A'
                    dp['GLT_Desc'] = 'Real Estate Resource Products'
            elif dp['EL Product'] == 'AP':
                if dp['EL Act'] == '2.2.2':
                    if '1.3.2 F' in dp['Cust EL']:
                        dp['GLT_tag'] = '1B1.A'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors strictly for Consumers'
                    elif '3.3.2 A4ii' in dp['Cust EL']:
                        dp['GLT_tag'] = '1B1.B'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for Real Estate Lessors'
                    elif '2.2.2 A' in dp['Cust EL'] and dp['Cust Product'] == 'RP':
                        dp['GLT_tag'] = '1B1.C'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for Real Estate developers'
                    elif '2.2.2 B' in dp['Cust EL'] and dp['Cust Product'] == 'RP':
                        dp['GLT_tag'] = '1B1.D'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for Equipment manufacturers'
                    elif '2.2.2 E' in dp['Cust EL'] and dp['Cust Product'] == 'RP' and re.search(r'E4\w+\s2\.3\.2', dp['CofC FR1']):
                        dp['GLT_tag'] = '1B1.E'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for medicine Producers'
                    elif ('2.2.2 E' in dp['Cust EL'] and dp['Cust Product'] == 'RP') and re.search(r'(E4\w+\s2\.2\.2\sB|E4\w+\s2\.2\.2\sDiv)', dp['CofC FR1']):
                        dp['GLT_tag'] = '1B1.F'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for producers of Energy for equipment or diversified resources'
                    elif '2.3.2 F' in dp['Cust EL']:
                        dp['GLT_tag'] = '1B1.G'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for Medical Treatment Providers'
                    elif '4.2.2 F' == dp['Cust EL'] and dp['Cust Product'] == 'AP':
                        dp['GLT_tag'] = '1B1.H'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for Government'
                    elif '2.2.2 Div' in dp['Cust EL'] and dp['Cust Product'] == 'RP':
                        dp['GLT_tag'] = '1B1.I'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for diversified Producers'
                    elif dp['Cust EL'] == 'Div' or 'DivA' or 'DivS':
                        dp['GLT_tag'] = '1B1.J'
                        dp['GLT_Desc'] = 'Building Real Estate Contractors for Diversified Customers'
                    else:
                        dp['GLT_tag'] = '1B1'
                        dp['GLT_Desc'] = 'Real Estate Contract Builders'
                elif dp['EL Act'] == '1.1.2' or '3.1.2':
                    if 'consumer' in dp['Cust Type'].lower():
                        dp['GLT_tag'] = '1B2.A'
                        dp['GLT_Desc'] = 'Real Estate Broker services for Consumers'
                    elif 'business' and not 'consumer' in dp['Cust Type'].lower():
                        dp['GLT_tag'] = '1B2.B'
                        dp['GLT_Desc'] = 'Real Estate Broker services for Businesses'
                    else:
                        dp['GLT_tag'] = '1B2'
                        dp['GLT_Desc'] = 'Real Estate Brokers'
                elif dp['EL Act'] == '2.2.3' or '2.3.2':
                    if 'business' and not 'consumer' in dp['Cust Type'].lower():
                        dp['GLT_tag'] = '1B3.A'
                        dp['GLT_Desc'] = 'Real Estate maintenance or repair services for Businesses'
                    elif 'consumer' in dp['Cust Type'].lower():
                        dp['GLT_tag'] = '1B3.B'
                        dp['GLT_Desc'] = 'Real Estate Maintenance or repair services for Consumers'
                    elif 'government' and not 'consumer' and not 'business' in dp['Cust Type'].lower():
                        dp['GLT_tag'] = '1B3.C'
                        dp['GLT_Desc'] = 'Real Estate maintenance or repair Services for Government'
                    else:
                        dp['GLT_tag'] = '1B3'
                        dp['GLT_Desc'] = 'Real Estate maintenance or repair services'
                elif dp['EL'] == '4.2.2':
                    if 'business' and not 'consumer' in dp['Cust Type'].lower():
                        dp['GLT_tag'] = '1B4.A'
                        dp['GLT_Desc'] = 'Real Estate Management for Businesses'
                    elif 'government' and not 'consumer' and not 'business' in dp['Cust Type'].lower():
                        dp['GLT_tag'] = '1B4.B'
                        dp['GLT_Desc'] = 'Real Estate Management for the Government'
                    else:
                        dp['GLT_tag'] = '1B4'
                        dp['GLT_Desc'] = 'Real Estate Management Services'
                else:
                    dp['GLT_tag'] = '1B'
                    dp['GLT_Desc'] = 'Real Estate Activity Products'
            else:
                dp['GLT_tag'] = '1'
                dp['GLT_Desc'] = 'Real Estate'

        #Assigns to B Bucket
    #Assigns to B Bucket
    elif re.search(r'B\w+', dp['EL Obj']) or dp['EL Obj'] == 'Div':
            #Assigns to Tier 2
            if dp['EL Product'] == 'RP':
                #Tier 3
                if dp['EL Act'] == '2.2.2':
                    #TIER 4
                    if (re.search (r'C', dp['CR1 Obj']) and re.search(r'(B[1-3]\w+|Bdiv)', dp['EL Obj'])) or (re.search(r'B4', dp['EL Obj']) and not re.search(r'C', dp['FR1 Obj'])):
                    elif
                    else:
                        dp['GLT_tag'] = '2A1'
                        dp['GLT_Desc'] = 'Equipment manufacturers'
                elif dp['EL Act'] == '1.3.2' or '3.1.2' or '3.3.2':
                    dp['GLT_tag'] = '2A2'
                    dp['GLT_Desc'] = 'Equipment Distributer'
                else:
                    dp['GLT_tag'] = '2A'
                    dp['GLT_Desc'] = 'Equipment Resource Products'
            elif dp['EL Product'] == 'AP':
                if re.search(r'1\.2\.\d', dp['EL Act']):
                    dp['GLT_tag'] = '2B1'
                    dp['GLT_Desc'] = 'Transportation related services of Equipment or diversified resources'
                elif dp['EL Act'] == '1.3.2':
                    dp['GLT_tag'] = '2B2'
                    dp['GLT_Desc'] = 'Equipment Storage'
                elif dp['EL Act'] == '2.2.2':
                    dp['GLT_tag'] = '2B3'
                    dp['GLT_Desc'] = 'Contract Equipment Manufacturing'
                elif dp['EL Act'] == '2.2.3' or '2.3.2':
                    dp['GLT_tag'] = '2B4'
                    dp['GLT_Desc'] = 'Equipment Maintenance or Repair'
                elif dp['EL Act'] == '1.1.2' or '3.1.2':
                    dp['GLT_tag'] = '2B5'
                    dp['GLT_Desc'] = 'Equipment brokers'
                else:
                    dp['GLT_tag'] = '2B'
                    dp['GLT_Desc'] = 'Equipment activity products'
            else:
                dp['GLT_tag'] = '2'
                dp['GLT_Desc'] == 'Equipment'

        #Assigns to D Bucket
    #Assigns to D Bucket
    elif re.search(r'D\w+', dp['EL Obj']):
        #Assigns to Tier 2
        if dp['EL Product'] == 'RP':
            #TIER 3
            if dp['EL Act'] == '1.3.2' or '3.3.2' or '3.1.2':
                dp['GLT_tag'] = '4A1'
                dp['GLT_Desc'] = 'Financial Distributor'
            elif dp['EL Act'] =='2.2.2':
                dp['GLT_tag'] = '4A2'
                dp['GLT_Desc'] = 'Financial Producer'
            else:
                dp['GLT_tag'] = '4A'
                dp['GLT_Desc'] = 'Financial Resource Products'
        elif dp['EL Product'] =='AP':
            if dp['EL Act'] == '1.1.2' or '3.1.2':
                dp['GLT_tag'] = '4B1'
                dp['GLT_Desc'] = 'Financial Brokers'
            elif re.search(r'3\.2\.\d', dp['EL']) or dp['EL Act'] == '3.3.2':
                dp['GLT_tag'] = '4B2'
                dp['GLT_Desc'] = 'Money deposits and transport related services'
            elif dp['EL Act'] == '4.2.2':
                dp['GLT_tag'] = '4B3'
                dp['GLT_Desc'] = 'Asset managers or Funds'
            else:
                dp['GLT_tag'] = '4B'
                dp['GLT_Desc'] = 'Financial Activity Products'
        else:
            dp['GLT_tag'] = '4'
            dp['GLT_Desc'] = 'Finance'
        #Assigns to E Bucket
    #Assigns to E Bucket
    elif re.search(r'E\w+', dp['EL Obj']):
        #Assigns to Tier 2
        if re.search(r'(E4\w+\s2\.2\.2\sB\w+|E4\w+\s2\.2\.2\sDiv)', dp['FR2']) \
        or re.search(r'(E4\w+\s2\.2\.2\sB\w+|E4\w+\s2\.2\.2\sDiv)', dp['CofC FR1'])\
        or re.search(r'(E4\w+\s2\.2\.2\sB\w+|E4\w+\s2\.2\.2\sDiv)', dp['FR1']):
            #TIER 3
            if dp['EL Product'] == 'RP':
                dp['GLT_tag'] = '5A1'
                dp['GLT_Desc'] = 'Energy for Equipment or diversified resources Resource Products'
            elif dp['EL Product'] == 'AP':
                dp['GLT_tag'] = '5A2'
                dp['GLT_Desc'] = 'Energy for Equipment or diversified resources Activity Products'
            else:
                dp['GLT_tag'] = '5A'
                dp['GLT_Desc'] = 'Energy for Equipment or Diversified Resources'
        elif re.search(r'E4i+\s2\.2\.\d\sF', dp['FR2']) \
        or re.search(r'E4i+\s2\.2\.\d\sF', dp['CofC FR1']) \
        or re.search(r'E4i+\s2\.2\.\d\sF', dp['FR1']):
            if dp['EL Product'] == 'RP':
                dp['GLT_tag'] = '5B1'
                dp['GLT_Desc'] = 'Food Resource Products'
            elif dp['EL Product'] == 'AP':
                dp['GLT_tag'] = '5B2'
                dp['GLT_Desc'] = 'Food Activity Products'
            else:
                dp['GLT_tag'] = '5B'
                dp['GLT_Desc'] = 'Food'
        elif re.search(r'E4i+\s2\.3\.2', dp['FR1']) or re.search(r'E4i+\s2\.3\.2', dp['FR2']) or re.search(r'E4i+\s2\.3\.2', dp['CofC FR1']):
            if dp['EL Product'] == 'RP':
                dp['GLT_tag'] = '5C1'
                dp['GLT_Desc'] = 'Medicinal Resource Products'
            elif dp['EL Product'] == 'AP':
                dp['GLT_tag'] = '5C2'
                dp['GLT_Desc'] = 'Medicinal activity products'
            else:
                dp['GLT_tag'] = '5C'
                dp['GLT_Desc'] = 'Medicine'
        else:
            dp['GLT_tag'] = '5'
            dp['GLT_Desc'] = 'Energy'

        #Assigns to F Bucket
    #Assigns to F Bucket
    elif dp['EL Obj'] == 'F':
        #TIER 2
        if dp['EL Product'] == 'AP':
            #TIER 3
            if dp['EL Act'] == '2.2.3':
                dp['GLT_tag'] = '6A1'
                dp['GLT_Desc'] = 'Personal Maintenance Services'
            elif dp['EL Act'] == '2.3.2':
                if '3.3.2 D3ii' in dp['Int 1 EL'] or dp['Int 2 EL']:
                    dp['GLT_tag'] = '6A2.A'
                    dp['GLT_Desc'] = 'Medical Service Providers that are paid for through private insurance'
                elif '4.2.2 F' in dp['Int 1 EL'] or dp['Int 2 EL']:
                    dp['GLT_tag'] = '6A2.B'
                    dp['GLT_Desc'] = 'Medical Service Providers that are paid for through government insurance'
                elif '3.3.2 D3ii' or '4.2.2 F' not in dp['Int 1 EL'] or dp['Int 2 EL']:
                    dp['GLT_tag'] = '6A2.C'
                    dp['GLT_Desc'] = 'Medical Service Providers that are paid for without health insurance'
                else:
                    dp['GLT_tag'] = '6A2'
                    dp['GLT_Desc'] = 'Medical Service Providers'
            elif dp['EL Act'] == '2.2.2':
                dp['GLT_tag'] = '6A3'
                dp['GLT_Desc'] = 'Entertainment services'
            elif dp['EL Act'] == '1.2.1':
                dp['GLT_tag'] = '6A4'
                dp['GLT_Desc'] = 'Employee relocation services'
            elif dp['EL Act'] == '1.2.2':
                dp['GLT_tag'] = '6A5'
                dp['GLT_Desc'] = 'Transportation of People'
            elif dp['EL Act'] == '1.3.2':
                dp['GLT_tag'] = '6A6'
                dp['GLT_Desc'] = 'Prison Operators'
            elif dp['EL Act'] == '1.1.2':
                dp['GLT_tag'] = '6A7'
                dp['GLT_Desc'] = 'Employee Recruitment Services'
            else:
                dp['GLT_tag'] = '6A'
                dp['GLT_Desc'] = 'Activity Products that act on people'
        elif dp['EL Product'] =='RP':
            if dp['EL Act'] == '1.3.2':
                dp['GLT_tag'] = '6B1'
                dp['GLT_Desc'] = 'Temporary Staffing'
            else:
                dp['GLT_tag'] = '6B'
                dp['GLT_Desc'] = 'Resource Products that act on people'
        else:
            dp['GLT_tag'] = '6'
            dp['GLT_Desc'] = 'People'
    else:
        dp['GLT_tag'] = 'Error'
        dp['GLT_Desc'] = 'Error'

    #WRITES TO CSV
    outrow = [item[1] for item in sorted(dp.items(), key = lambda x: dict_column_index[x[0]])]
    if not dp['GLT_tag'] == 'Error':
        writer.writerow(outrow)
