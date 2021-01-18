import meraki
import json
from flask import Flask,render_template,request,jsonify,Markup,redirect,url_for
from pathlib import Path
from yattag import indent
from airium import Airium

'''
    For access to the Meraki API you will need to export the key as environment variable at the command line.
    See here:
    -   https://github.com/meraki/dashboard-api-python/
    -   https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html

    export MERAKI_DASHBOARD_API_KEY=#################################
'''

app = Flask(__name__)

dashboard = meraki.DashboardAPI(log_path='./logs/')

templateLocation = "static/json/template.json"

def buildOrgTab():
    orgs = dashboard.organizations.getOrganizations()

    html = Airium()

    with html.table(klass='orgTable'):
        with html.tr():
            html.th(klass='id',_t='ID')
            html.th(klass='org',_t='Organisation')
            html.th(klass='orgbutton',_t='Update')

            for org in orgs:
                with html.tr():
                    html.td(id=org['id'], _t=org['id'])
                    html.td(_t=org['name'])
                    with html.td():
                        updateOrg = 'updateOrg('+ org['id'] + ')'
                        html.button(type='button', _t='Update', onclick=updateOrg)

    return str(html)        

def readTemplate():
    currentTemplate = Path(templateLocation)
    if(currentTemplate.exists()):
        with open(templateLocation, "r") as templateFile:
            return json.load(templateFile) 

def buildTemplateTab():
    html = Airium()
    data = readTemplate()

    html.h3(_t='Organisation settings')
    html.table(_t=buildTable(data['org']))
    html.h3(_t='Network settings')
    html.table(_t=buildTable(data['net']))

    return str(html)

def buildTable(data):
    html = Airium()
    with html.table(klass='templateTable'):
        for i in data:
            with html.tr():
                html.td(_t=i['name'])
                if(isinstance(i['value'],bool)):
                    with html.td():
                        if('enable'):
                            html.input(type='checkbox', checked='')
                        else:
                            html.input(type='checkbox')
                elif(isinstance(i['value'],dict)):
                    html.td()
    return str(html)


@app.route('/updateOrg')
def updateOrg():

    currentTemplate = Path(templateLocation)

    id = request.args.get('orgID')
    org = dashboard.organizations.getOrganization(id)
    networks = dashboard.organizations.getOrganization(id)
    print(org)
    print(networks)
    
    return 'success'

@app.route('/updateSuccess')
def updateSuccess():
    return render_template('success.html')

@app.route('/')
def home():
    return render_template('index.html',
        orgTable = Markup(buildOrgTab()),
        configTemplate = Markup(buildTemplateTab()),
        orgStatus = Markup("Coming soon"),
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')