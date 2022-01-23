# Proejct YoonDong-ju: the official website of Yonsei Literature Club
> 하늘을 우러러 한 점 버그가 없기를!
## Requirements
* npm
* Typescript compiiler
* pip
* python >=3.8
## Run in local
1. `npx tsc`
1. `pip install -r requirements.txt`
1. `python main.py`
## Features
* 공지 열람 및 작성.
## Frameworks & Solutions
* Python
  * [Flask](https://flask.palletsprojects.com) deployed by [Gunicorn](https://gunicorn.org/): for being the easiest python web framework.
  * [Jinja2](https://jinja.palletsprojects.com/): for being too easy to not use.
  * [Markdown](https://python-markdown.github.io/): for its intuitiveness. Check out the syntax at: https://markdownlivepreview.com.
* JavaScript
  * Neither [React](https://reactjs.org/) nor [Vue](https://v3.vuejs.org/) but [VanillaJS](http://vanilla-js.com) with the help of [Typescript](https://www.typescriptlang.org/): since this webiste does not implement any complex UIs, which the former two are for.
* SQL
  * [SQLite](https://www.sqlite.org): for its minimality and [ability to handle up to 100K hits/day without any performance issue.](https://www.sqlite.org/whentouse.html#:~:text=SQLite%20works%20great%20as%20the,should%20work%20fine%20with%20SQLite.)
## Code Conventions
* Python: [Google's](https://google.github.io/styleguide/pyguide.html)
* HTML/CSS: [Google's](https://google.github.io/styleguide/htmlcssguide.html)
* JavaScript: [Google's](https://google.github.io/styleguide/jsguide.html)
* Shell: [Google's](https://google.github.io/styleguide/shellguide.html)
* Nginx conf: [Just like this](https://www.nginx.com/resources/wiki/start/topics/examples/full/)
## Notes
### Copyright
* 연세문학회 문집 더미에 파묻힌 강아지가 바깥으로 몸을 반쯤 내밀고 숨을 돌리는 대문 그림은 원저작자의 허락을 받아 사용함.
* 서체
  * 국문/영문 서체: 고운 바탕
  * 한문 서체: Noto Serif Korean
## Contributors
* [TrulyBright](https://github.com/TrulyBright)