import csv

from django.http import HttpResponse


def queryset_to_csv(queryset):
    """Возвращает объект HttpResponse, содержащий csv файл
    с данными из queryset"""
    response = HttpResponse(
        content_type="text/csv",
        headers={'Content-Disposition':
                 'attachment; filename="shopping_list.csv"'},
    )
    writer = csv.DictWriter(response, fieldnames=queryset.first().keys())
    writer.writeheader()
    writer.writerows(queryset)
    return response
