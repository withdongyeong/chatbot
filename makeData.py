import os
# 롤 0
# 오버워치 1
# 배그 2
# 로스트아크 3
# 인사 4 (환영, 작별 묶고 반응은 중의적으로 해야할듯)
# 감사 5

datapath = "./train"
keyword = "배틀그라운드"
NthIter = 1
label = '5'
space = ' '
if not os.path.isdir("./train"):
    os.mkdir("./train")

templateGame = [
    keyword + space + '사양 알려줘', #1 keyword
    keyword + space + '하고 싶은데 똥컴임', #2
    keyword + space + '권장사항 좀 알려주세요', #3
    keyword + '은 고사양 게임은 아니지 않나', #4
    keyword + space + '할 때 안 끊기는 사양', #5
    keyword + space + '컴퓨터 추천', #6
    keyword + space + '할건데 컴퓨터 새로 사야겠다', #7
    keyword + space + '하는데 컴퓨터 바꾸고 싶다', #8
    keyword + '은 고사양 게임인가요?', #9
    keyword + '에 필요한 컴퓨터 권장 사양', #10
    keyword + space + '할 때 렉 걸림', #11
    keyword + space + '하는데 내가 할 때마다 로딩 너무 김', #12
    keyword + space + '할 때 컴퓨터 어떻게 사야 돼요?', #13
    keyword + space + '하는데 컴퓨터가 이상하다', #14
    keyword + space + '하려면 컴퓨터 새로 사야 되나요?', #15
    keyword + space + '권장사양 높은 편 인가요?', #16
    keyword + space + '하는데 나 때문에 로딩 긴 것 같다', #17
    keyword + space + '필요사양 좀 알려주세요', #18
    keyword + space + '할 때 자꾸 렉 걸려서 짜증난다', #19
    keyword + space + '하려면 컴퓨터 사양 뭐 필요한가요?', #20
    '새 컴퓨터로' + space + keyword + '하고 싶다', #21
    keyword + space + '할 때 쓸 컴퓨터', #22
    keyword + space + '할 때 게임이 자꾸 끊김', #23
    keyword + space + '컴퓨터 좀 추천해 주세요', #24
    '4년된 컴퓨터인데' + space + keyword + space + '하는데 문제 없나?', #25
    '친구가' + space + keyword + '하자는데 컴퓨터가 똥컴이라 못 하겠어요', #26
    '5년 전에 컴퓨터 샀는데' + space + keyword + space + '돌아갈까요?', #27
    '꾸진 컴퓨터도' + space + keyword + space + '돌아갈까요?', #28
    keyword + space + '하는데 내 컴퓨터 너무 안 좋다', #29
    keyword + space + '하는데 내 컴퓨터 느려서 미치겠음', #30
    keyword + space + '하고 싶습니다', #31
    keyword + space + '할 때 자꾸 튕김', #32
    '똥컴인데' + space + keyword + space + '되나요?' #33
]

templateHi = [
    "안녕", #1
    "반가워", #2
    "안녕 다알아", #3
    "다알아", #4
    "안녕하세요", #5
    "안녕하십니까", #6
    "반가워요", #7
    "반갑습니다", #8
    "안녕하세요 다알아", #9
    "안녕하십니까 다알아", #10
    "반가워 다알아", #11
    "반가워요 다알아", #12
    "반갑습니다 다알아", #13
    "잘 지냈어?", #14
    "잘 지내", #15
    "잘 있어", #16
    "또 올게", #17
    "또 봐", #18
    "다음에 봐", #19
    "다음에 봐요", #20
    "다음에 볼게", #21
    "이제 나가볼게", #22
    "이제 가볼게", #23
    "또 만나", #24
    "다음에 만나", #25
    "다시 만나", #26
    "내일 만나", #27
    "내일 봐", #28
    "좋은 아침", #29
    "환영해", #30
    "오랜만이야", #31
    "하이", #32
    "헬로" #33
]

templateThanks = [
    "고마워", #1
    "고마워요", #2
    "고맙습니다", #3
    "고마워 다알아", #4
    "고마워요 다알아", #5
    "고맙습니다 다알아", #6
    "땡큐", #7
    "감사해요", #8
    "감사합니다", #9
    "오 고마워", #10
    "오 고마워요", #11
    "오 고맙습니다", #12
    "오 고마워 다알아", #13
    "오 고마워요 다알아", #14
    "오 고맙습니다 다알아", #15
    "오 땡큐", #16
    "와 고마워", #17
    "와 고마워요", #18
    "와 고맙습니다", #19
    "대박", #20
    "오 대박", #21
    "와 대박", #22
    "역시", #23
    "역시 다알아", #24
]

labels = []
for i in range (0,33):
    labels.append(label)

# for label, text in zip(labels, templateGame):
#     print(label)
#     print(text)

# 텍스트 쓰기
# for i, (label, text) in enumerate(zip(labels, templateGame)):
#     fname = datapath + os.sep + label + "_" + str(i+1+(((NthIter-1)*33))) + ".txt"
#     if os.path.isfile(fname):
#         print(fname + " is exists")
#         exit()
#     f = open(fname, 'w', encoding='UTF-8')
#     # 첫번째 줄은 label
#     # strip() 함수는 문자열의 선행, 후행 개행 문자를 모두 제거
#     f.writelines(label + "\n")
#     f.writelines(text)
#     f.close()

for i, (label, text) in enumerate(zip(labels, templateThanks)):
    fname = datapath + os.sep + label + "_" + str(i+1+(((NthIter-1)*33))) + ".txt"
    if os.path.isfile(fname):
        print(fname + " is exists")
        exit()
    f = open(fname, 'w', encoding='UTF-8')
    # 첫번째 줄은 label
    # strip() 함수는 문자열의 선행, 후행 개행 문자를 모두 제거
    f.writelines(label + "\n")
    f.writelines(text)
    f.close()