import sqlite3

with sqlite3.connect("sql/special_posts.db") as DB:
    DB.execute("""
        DELETE FROM special_posts WHERE title=='about'
    """)
    DB.execute("""
        INSERT INTO special_posts (
            title, content, author, published
        )
        VALUES (
            "about",
            "# 연세문학회는
문학과 관련하여 다양한 정기, 비정기 활동을 하는 동아리입니다. 「연세문학회」란 이름은 정현종 시인이 지었습니다.
# 활동
## 정기 활동
### 주간 활동
- [시반](/classes/poetry): 시를 짓습니다.
- [소설반](/classes/novel): 소설을 씁니다.
- [합평반](/classes/critique): 회원이 쓴 작품을 합평합니다. 작가는 회원들이 평하는 동안 단 한 마디도 할 수 없습니다.
- [독서반](/classes/reading): 기성 작가가 쓴 작품을 읽고 감상을 나눕니다.
### 반기 활동
- 상반기: 시 설치미술전
- 하반기: 영상 문학제
## 비정기 활동
- 릴레이 시 창작회
- 별 헤는 밤
# 문집
연 2회, 회원들의 작품을 모아 문집을 발간합니다. 봄·여름호와 가을·겨울호가 있습니다.
# 거쳐간 대표 문인
- [윤동주](http://encykorea.aks.ac.kr/Contents/Item/E0042294)
- [송몽규](http://encykorea.aks.ac.kr/Contents/Item/E0073811)
- [정현종](http://moonji.com/bookauth/627/)
- [기형도](http://www.kihyungdo.co.kr/sub03/sub01.php)
- [마광수](http://www.yes24.com/24/AuthorFile/Author/42)
- [나희덕](https://www.changbi.com/authors/2999?board_id=25)
- [성석제](https://www.changbi.com/authors/3722?board_id=31)
- [공지영](https://www.changbi.com/authors/2328?board_id=24)",
        1,
        "2022-01-16"
    )
    """)