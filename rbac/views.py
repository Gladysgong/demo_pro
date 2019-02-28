# -*- coding: utf-8 -*- 
from django.shortcuts import render, redirect, reverse
from .models import UserInfo, Role, Permission, Menu
from .forms import UserInfoModelForm, RoleModelForm, PermissionModelForm, MenuModelForm
from rbac import models
from utils import pagination


def index(request):
    return render(request, 'index.html')


def users(request):
    """查询所有用户信息"""
    # user_list = UserInfo.objects.all()
    # return render(request, 'rbac/users.html', {'user_list': user_list})
    page = request.GET.get('page')
    current_page = 1
    if page:
        current_page = int(page)
    search_fl = request.GET.get('fl')
    search_fn = request.GET.get('fn')
    if search_fl:
        search_fl = search_fl
    else:
        search_fl = ''
    if search_fn:
        search_fn = search_fn
    else:
        search_fn = ''
    try:
        if search_fl!='':
            user_info = models.UserInfo.objects.filter(username__startswith=search_fl.lower()).order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(user_info), 10, 9)
            data = user_info[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/rbac/users/?fl=%s&page=" % search_fl.lower())
        elif search_fn!='':
            user_info = models.UserInfo.objects.filter(username__contains=search_fn).all()
            page_obj = pagination.Page(current_page, len(user_info), 10, 9)
            data = user_info[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/rbac/users/?fn=%s&page=" % search_fn)
        else:
            user_info = models.UserInfo.objects.all().order_by('id')[::-1]
            page_obj = pagination.Page(current_page, len(user_info), 10, 9)
            data = user_info[page_obj.start:page_obj.end]
            page_str = page_obj.page_str("/rbac/users/?page=")
        first_letter=list()
        user_name_info = models.UserInfo.objects.all().order_by('id')[::-1]
        for item in user_name_info:
            if item.username[0].upper() not in first_letter:
                first_letter.append(item.username[0].upper())
        first_letter=sorted(first_letter)

        none_limit=list()
        for user_role in user_name_info:
            if user_role.roles.all().count()==0:
                none_limit.append(user_role.username)

    except Exception as e:
        print(e)
        pass
    return render(request, 'rbac/user_control.html', {'li': data, 'page_str': page_str,'first_letter':first_letter,'none_limit_num':len(none_limit),'none_limit':none_limit})


def users_new(request):
    if request.method =="GET":
        # 传入ModelForm对象
        model_form = UserInfoModelForm()
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '新增用户'})
    else:
        model_form = UserInfoModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(users))
        else:
            return render(request, 'rbac/common_edit.html',{'model_form': model_form, 'title': '新增用户'})


def users_edit(request,id):
    user_obj = UserInfo.objects.filter(id=id).first()
    if request.method == 'GET':
        model_form = UserInfoModelForm(instance=user_obj)
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑用户'})
    else:
        model_form = UserInfoModelForm(request.POST, instance=user_obj)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(users))
        else:
            return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑用户'})


def users_delete(request, id):
    user_obj = UserInfo.objects.filter(id=id).first()
    user_obj.delete()
    return redirect(reverse(users))


def roles(request):
    role_list = Role.objects.all()
    return render(request, 'rbac/roles.html', {'role_list': role_list})


def roles_new(request):
    if request.method == "GET":
        # 传入ModelForm对象
        model_form = RoleModelForm()
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '新增角色'})
    else:
        model_form = RoleModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(roles))
        else:
            return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '新增角色'})


def roles_edit(request, id):
    role_obj = Role.objects.filter(id=id).first()
    if request.method == 'GET':
        model_form = RoleModelForm(instance=role_obj)
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑角色'})
    else:
        model_form = RoleModelForm(request.POST, instance=role_obj)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(roles))
        else:
            return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑角色'})


def roles_delete(request, id):
    role_obj = Role.objects.filter(id=id).first()
    role_obj.delete()
    return redirect(reverse(roles))


def permissions(request):
    permission_list = Permission.objects.all()
    return render(request, 'rbac/permissions.html', {'permission_list': permission_list})


def permissions_new(request):
    if request.method == "GET":
        # 传入ModelForm对象
        model_form = PermissionModelForm()
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '新增权限'})
    else:
        model_form = PermissionModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(permissions))
        else:
            return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '新增权限'})


def permissions_edit(request, id):
    permission_obj = Permission.objects.filter(id=id).first()
    if request.method == 'GET':
        model_form = PermissionModelForm(instance=permission_obj)
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑权限'})
    else:
        model_form = PermissionModelForm(request.POST, instance=permission_obj)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(permissions))
        else:
            return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑权限'})


def permissions_delete(request, id):
    print(id)
    permission_obj = Permission.objects.filter(id=id).first()
    permission_obj.delete()
    return redirect(reverse(permissions))


def menus(request):
    menu_list = Menu.objects.all()
    return render(request, 'rbac/menus.html', {'menu_list': menu_list})


def menus_new(request):
    if request.method == "GET":
        # 传入ModelForm对象
        model_form = MenuModelForm()
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '新增菜单'})
    else:
        model_form = MenuModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(menus))
        else:
            return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '新增菜单'})


def menus_edit(request, id):
    menu_obj = Menu.objects.filter(id=id).first()
    if request.method == 'GET':
        model_form = MenuModelForm(instance=menu_obj)
        return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑菜单'})
    else:
        model_form = MenuModelForm(request.POST, instance=menu_obj)
        if model_form.is_valid():
            model_form.save()
            return redirect(reverse(menus))
        else:
            return render(request, 'rbac/common_edit.html', {'model_form': model_form, 'title': '编辑菜单'})


def menus_delete(request, id):
    print(id)
    menu_obj = Menu.objects.filter(id=id).first()
    menu_obj.delete()
    return redirect(reverse(menus))

