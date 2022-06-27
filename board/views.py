from django.shortcuts import render, redirect
from board.models import Board
from member.models import Member
from django.db.models import F


# Create your views here.


def list(request):
    # select 'id', 'title', 'userid', 'regdate', 'views'
    # from board order by id desc
    #
    # bdlist = Board.objects.values(
    #     'id', 'title', 'userid', 'regdate', 'views'
    # ).order_by('-id')

    # Board와 Member 테이블은 userid <-> id컬럼을 기준으로
    # inner join을 수행
    bdlist = Board.objects.select_related('member')

    # join 된 member 테이블의 userid 확인
    # bdlist.get(0).member.userid

    context = {'bds': bdlist}
    return render(request, 'board/list.html', context)


def view(request):
    if request.method == 'GET':
        form = request.GET.dict()

        b = Board.objects.get(id=form['bno'])
        b.views = b.views + 1
        b.save()
        # Board.objects.filter(id=form['bno']).update(views=F(view('views'))+1)

        # select * from board inner join member
        # using(id) where id = ???
        bd = Board.objects.select_related('member').get(id=form['bno'])
    elif request.method == 'POST':
        pass

    context = {'bd': bd}

    return render(request, 'board/view.html', context)


def write(request):
    form = None
    error = ''
    returnPage = 'board/write.html'
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        form = request.POST.dict()

        if not (form['title'] and form['contents']):
            error = '제목이나 본문을 입력'
        else:
            bd = Board(title=form['title'],
                       contents=form['contents'],
                       # 새 글 작성시 작성한 회원에 대한 정보는
                       # 회원테이블에 존재하는 회원번호(id)를 조회해서
                       # userid에 저장
                       member=Member.objects.get(pk=form['memberid'])
                       )
            bd.save()
            return redirect('/list')
    context = {'form': form, 'error': error}
    return render(request, returnPage, context)


def modify(request):
    if request.method == 'GET':
        form = request.GET.dict()

        # select board where bno = ???
        bd = Board.objects.get(id=form['bno'])
    elif request.method == 'POST':
        form = request.POST.dict()

        b = Board.objects.get(id=form['bno'])
        b.title = form['title']
        b.contents = form['contents']
        b.save()

        Board.objects.filter(id=form['bno']).update(title=form['title'], contents=form['contents'])

        return redirect('/view?bno=' + form['bno'])
    context = {'bd': bd}
    return render(request, 'board/modify.html', context)


def remove(request):
    if request.method == 'GET':
        form = request.GET.dict()

        Board.objects.filter(id=form['bno']).delete()

    return None
