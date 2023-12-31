from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from web.forms.projectForm import ProjectModelForm
from web import models


def project_list(request):
    """项目列表"""
    # print(request.tracer.user.username)
    # print(request.tracer.price_policy.title)
    if request.method == 'GET':
        project_dict = {'star': [], 'my': [], 'join': []}
        my_project_list = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_project_list:
            if row.star:
                project_dict['star'].append({'value':row,'type': 'my'})
            else:
                project_dict['my'].append(row)
        join_project_list = models.ProjiectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value':item.project,'type': 'join'})
            else:
                project_dict['join'].append(item.project)

        form = ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})
    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 验证通过，models必填项：name,color,desc, creator
        form.instance.creator = request.tracer.user
        form.save()
        # return render(request, 'project_list.html', {'form': form})
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """
     设置星标项目:
        我的星标项目：/project/star/my/1
        参与星标项目：/project/star/join/3
     """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('web:project_list')
    if project_type == 'join':
        models.ProjiectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('web:project_list')
    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    """
         取消星标项目:
            我的星标项目：/project/unstar/my/1
            参与星标项目：/project/unstar/join/3
         """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('web:project_list')
    if project_type == 'join':
        models.ProjiectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('web:project_list')
    return HttpResponse('请求错误')
