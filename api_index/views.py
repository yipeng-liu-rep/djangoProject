from django.core import serializers
from django.shortcuts import render
from django.forms import model_to_dict


# Create your views here.
from django.http import HttpResponse, JsonResponse
from api_index.models import Article, UserInfo, Collection
from django.core.cache import cache
import json


def token_validate(token):
    # 验证接口
    back_dic = {'code': 10000, 'msg': ''}
    cache_list = cache.keys("*")
    if token not in cache_list:
        back_dic['code'] = 400
        back_dic['msg'] = '登录已过期，请推出后重新登录'
    else:
        back_dic['code'] = 200
        back_dic['msg'] = '完成'
    return back_dic


def index(request):
    # users = UserInfo.objects.values()
    # retStr = ''
    # for user in users:
    #     for name,value in user.items():
    #         retStr += f'{name} : {value} | '
    #
    #     retStr += '<br>'
    retStr = 'Hello World'

    return HttpResponse(retStr)


def show_index(request):
    # 展示接口
    if request.method == 'GET':
        msg = serializers.serialize('json', Article.objects.all())
    return HttpResponse(msg, content_type="application/json")


def add_article(request):
    # 添加文章
    if request.method == 'POST':
        token = request.headers['token']
        back_dic = token_validate(token)
        if back_dic['code'] == 200:
            user = UserInfo.objects.get(username=request.POST['name'])
            new_article = Article.objects.create(article_title=request.POST['title'],
                                                      article_content=request.POST['content'],
                                                      article_photo_path=request.FILES.get('img'),
                                                      article_owner=user)
            new_article.save()
        return JsonResponse(back_dic)
    else:
        return HttpResponse('post only')


def show_personal_article(request):
    # 个人文章展示界面
    user = UserInfo.objects.get(username=request.GET['name'])
    msg = serializers.serialize('json', user.article_set.all())

    return HttpResponse(msg, content_type="application/json")


def article_detail(request):
    article = Article.objects.filter(pk=request.GET['id'])
    username = article[0].article_owner.username
    dict = model_to_dict(article[0])
    dict['username'] = username
    dict['article_photo_path'] = str(dict['article_photo_path'])
    msg = json.dumps(dict)
    return HttpResponse(msg, content_type="application/json")
    # 详情页面


def listarticle(request):
    # 查询操作
    Query = Article.objects.values()
    retlist = list(Query)
    return JsonResponse({'ret': 0, 'retStr': retlist})


def add_collection(request):
    # 添加收藏操作
    info = request.GET
    # 从请求消息中 获取要添加客户的信息
    # 并且插入到数据库中
    # 返回值 就是对应插入记录的对象
    user = UserInfo.objects.filter(id=info['user_id'])
    article = Article.objects.filter(id=info['article_id'])
    print(user)
    record = Collection.objects.create(collection_username=user[0],
        collection_article_name = article[0])

    return JsonResponse({'ret': 0, 'id': record.id})


def delete_collection(request):
    # 删除收藏操作
    info = request.GET
    Collection.objects.get(id=info['id']).delete()

    return JsonResponse({'ret': 0, 'result': True})


class Vividict(dict):
    # 嵌套字典
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


def user_collected_article(request):
    # 用户所收藏的文章
    info = request.GET
    queryset = Collection.objects.filter(collection_username=info['user_id'])
    dict = Vividict()
    for i, query in enumerate(queryset):
        dict[i]['title'] = query.collection_article_name.article_title
        dict[i]['photo_path'] = str(query.collection_article_name.article_photo_path)
        dict[i]['article_id'] = query.collection_article_name.id
    print(dict[1]['article_id'])
    return JsonResponse(dict)


def is_collected(request):
    # 判断文章是否被收藏
    info = request.GET
    collect_set = Collection.objects.filter(collection_username=info['user_id'], collection_article_name=info['article_id'])
    if len(collect_set)==0:
        return JsonResponse({'ret': 0, 'result': False})
    else:
        return JsonResponse({'ret': 1, 'result': True, 'collect_id': collect_set[0].id})



