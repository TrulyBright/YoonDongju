# Proejct YoonDong-ju: the official website of Yonsei Literature Club
> 하늘을 우러러 한 점 버그가 없기를
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
## Contributors
* [TrulyBright](https://github.com/TrulyBright)