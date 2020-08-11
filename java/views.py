from django.shortcuts import render


def introduction(request):
	return render(request, "java/introduction.html")
