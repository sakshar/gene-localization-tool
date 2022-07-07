from django.shortcuts import redirect


def goto_gene_tool(request):
    response = redirect('/gene_tool/')
    return response
