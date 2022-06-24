from django.shortcuts import render, redirect
from board.models import Board
from member.models import Member


# Create your views here.


def list(request):
    bdlist = Board.objects.values(
        'id', 'title', 'userid', 'regdate', 'views'
    ).order_by('id')

    context = {'bds': bdlist}

    return render(request, 'board/list.html', context)


def view(request):
    return render(request, 'board/view.html')


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
                       userid=Member.objects.get(pk=form['memberid'])
                       )
            bd.save()
            return redirect('/list')
    context = {'form': form, 'error': error}
    return render(request, returnPage, context)
