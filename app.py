from flask import Flask, request, jsonify, redirect, abort, make_response
from datetime import datetime,date,timedelta
from collections import OrderedDict
from random import randint

import json


app = Flask(__name__)

@app.route("/")
def homepage():
    return "This is just the start of the world"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    return res

def processRequest(req):

    chatParameters = req.get("result").get("parameters")
    print(chatParameters)
    valid_params = {}
    for paramKey, paramValues in chatParameters.items():
        if paramValues != "":
            if "geo" not in paramKey:
                valid_params[paramKey] = paramValues
            else:
                valid_params["geo-region"] = paramValues

    print("Filtered params")
    print(valid_params)

    chatContexts = req.get("result").get("contexts")
    valid_context = {}
    for context in chatContexts:
        contextName = context.get("name")
        if contextName == "data-category":
            if context.get("parameters").get("data-category.original") != "":
                valid_context["data-category"] = context.get("parameters").get("data-category.original")
            elif context.get("parameters").get("data-category")!= "":
                valid_context["data-category"] = context.get("parameters").get("data-category")

        if contextName == "time-period":
            if context.get("parameters").get("date-period") != "":
                valid_context["date-period"] = context.get("parameters").get("date-period")

        if contextName == "geo-region":
            if context.get("parameters").get("geo-country.original") != "":
                valid_context["geo-region"] = context.get("parameters").get("geo-country.original")
            elif context.get("parameters").get("geo-state-us.original")!= "":
                valid_context["geo-region"] = context.get("parameters").get("geo-state-us.original")
            elif context.get("parameters").get("geo-city.original")!= "":
                valid_context["geo-region"] = context.get("parameters").get("geo-city.original")

    print("Filtered context")
    print(valid_context)

    union_params = dict(valid_context, **valid_params)
    print("union result")
    print(union_params)

    graph_data = {}
    if "date-period" in union_params:
        dates = union_params["date-period"].split("/")
        months = getMonthList(dates)
        for month in months:
            graph_data[month] = randint(50, 100)

        print("graph_data")
        print(graph_data)

    data_report = {}
    if "data-category" in union_params:
        data_report["y-axis-tag"] = union_params["data-category"]

    if "date-period" in union_params:
        data_report["x-axis-tag"] = "Time (in months)"

    if len(graph_data) > 5:
        data_report["graph-type"] = "Pie chart"
    else:
        data_report["graph-type"] = "Bar chart"

    data_report["xy-plots"] = graph_data

    #Get the speech from response
    chatSpeech = req.get("result").get("fulfillment").get("speech")
    print(chatSpeech)

    return buildResponse(speech=chatSpeech, displayText=chatSpeech, data_metrics=data_report, source="priyanka's webhook",
                         responseCode=200)

def getMonthList(dates):
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    mlist = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        mlist.append(datetime(y, m+1, 1).strftime("%b-%y"))
    return mlist

def buildResponse(speech, displayText, data_metrics, source, responseCode):
    print("BUILD RESPONSE")
    print({'speech': speech, 'displayText': displayText, 'data': data_metrics, 'source': source})
    return jsonify(
        {'speech': speech, 'displayText': displayText, 'data': data_metrics, 'source': source}), responseCode

if __name__ == '__main__':
    app.run()
