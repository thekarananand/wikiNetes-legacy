from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import markdown
import os
from . import util

containerID = os.environ['HOSTNAME']

def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries(),
        "containerID": containerID
    })

def RenderPage(request, Page):
    if Page in util.list_entries() :
        return render(request, "encyclopedia/article.html", {
            "Name" : Page ,
            "Content": markdown(util.get_entry(Page)),
            "containerID": containerID
        })

    else :
        return render(request, "encyclopedia/Page404.html", {
            "Name" : Page,
            "Error_Msg" : "Hey, This Piece of Link doesn't fit !",
            "containerID": containerID
        })


def search(request):
    if request.method == "POST":
        q = request.POST['q']

        RelatedEntries = []

        for entry in util.list_entries():
            if q.lower() == entry.lower():
                return RenderPage(request, entry)

            elif q.lower() in entry.lower():
                RelatedEntries.append(entry)

        return render(request, "encyclopedia/index.html", {
            "title": "Pages Related to \"" + q + "\"" ,
            "entries": RelatedEntries,
            "containerID": containerID
        })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/NewPage.html", {
            "title" : "",
            "content" : "",
            "endpoint" : "new",
            "error" : "",
            "containerID": containerID
        })

    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['md-content']

        for entry in util.list_entries():
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/NewPage.html", {
                    "title" : title,
                    "content" : content,
                    "endpoint" : "new",
                    "Url" : "/wiki/"+title+"/edit/",
                    "error" : """
                        <div id='error_box'>
                            ❌ An Article with the same name already exists...
                        </div>
                    """,
                    "containerID": containerID
                })

        util.save_entry(title, content)
        return RenderPage(request, title)

def editPage(request, Page):
    return render(request, "encyclopedia/NewPage.html", {
        "title" : Page,
        "content" : util.get_entry(Page),
        "endpoint" : "edit",
        "error" : "",
        "containerID": containerID
    })

def edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['md-content']
        util.save_entry(title, content)
        return RenderPage(request, title)
