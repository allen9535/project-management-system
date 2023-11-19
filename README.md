![logo](https://doc-images-s3.s3.ap-northeast-2.amazonaws.com/kanban.png)

# 📝 프로젝트 관리 시스템

**팀의 프로젝트 관리** 시스템입니다. 조직 내 사용자들이 팀을 생성하여 업무를 직관적이고 유연하게 분석·공유할 수 있도록 돕습니다. 회원가입한 사용자들은 팀을 생성할 수 있고, 팀을 생성하면 한 개의 보드를 사용할 수 있게 됩니다. 업무를 분류하고 관리해보세요. 저희는 이것을 컬럼이라 부릅니다. 각 분류에 맞게 업무를 생성하고 관리해보세요. 저희는 이것을 티켓이라 부릅니다. 각 기능들은 팀별 직급별로 권한이 명확하게 나누어져 있어 보안에 대해서도 크게 신경쓰지 않으셔도 됩니다.
여러분의 효율적인 프로젝트 관리를 도와드리겠습니다.

<br/>

## 목차

-   [개요](#개요)
-   [사용기술](#사용기술)
-   [디렉터리 구조](#디렉터리-구조)
-   [API 문서](#API-문서)
-   [ERD](#ERD)
-   [프로젝트 진행 및 이슈 관리](#프로젝트-진행-및-이슈-관리)
-   [구현 과정](#구현-과정)
-   [회고](#회고)

<br/>

## 개요

당 서비스는 프로젝트 관리를 돕는 시스템입니다. 조직 내 사용자들을 팀별, 직급별로 관리하고 프로젝트들과 작업들을 관리하는데 사용됩니다.

우선 회원 관리 시스템입니다. 회원가입 시점에서는 모두 일반 사용자입니다. 그러나 팀을 생성하게 되면 팀장이 되고, 다른 사용자들에게 팀 초대를 보내 팀을 구성할 권한을 갖게 됩니다.

다음은 보드 시스템입니다. 팀이 생성되면 한 개의 보드가 주어지는데, 이 보드에 진행할 업무를 분류할 수 있는 컬럼을 생성할 수 있습니다. 기본적으로는 Todo, In Progress, Done 같은 간단한 개념들을 추천드리지만, 편하신대로 구성해보실 수 있습니다.

또 컬럼을 생성하고 나면 실제 업무 단위에 해당하는 티켓을 생성할 수 있습니다. 업무 내용, 예상 소요 시간, 마감일, 담당자 등을 입력해 한 개의 티켓을 생성할 수 있는데, 이를 팀의 구성원들이 공유하게 됩니다.

당 서비스를 활용하여 유연하고 효율적인 작업 관리를 시작해보세요.

<br/>

## 사용기술

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white) &nbsp;
![Django](https://img.shields.io/badge/Django-092E20.svg?style=for-the-badge&logo=Django&logoColor=white) &nbsp;
![JWT](https://img.shields.io/badge/JWT-000000.svg?style=for-the-badge&logo=JSON-Web-Tokens&logoColor=white) &nbsp;
![Swagger](https://img.shields.io/badge/Swagger-85EA2D.svg?style=for-the-badge&logo=Swagger&logoColor=white) &nbsp;
![Celery](https://img.shields.io/badge/Celery-37814A.svg?style=for-the-badge&logo=Celery&logoColor=white) <br/>

![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white) <br/>

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white)

<br/>

## 디렉터리 구조

<details>
    <summary>디렉터리 구조</summary>

    📦Project-Management-System
    ┣ 📂.github
    ┃ ┣ 📂workflows
    ┃ ┃ ┣ 📜django_ci.yml
    ┃ ┃ ┗ 📜ec2_cd.yml
    ┃ ┗ 📜pull_request_template.md
    ┣ 📂boards
    ┃ ┣ 📜admin.py
    ┃ ┣ 📜apps.py
    ┃ ┣ 📜models.py
    ┃ ┣ 📜serializers.py
    ┃ ┣ 📜tests.py
    ┃ ┣ 📜urls.py
    ┃ ┣ 📜views.py
    ┃ ┗ 📜__init__.py
    ┣ 📂config
    ┃ ┣ 📜asgi.py
    ┃ ┣ 📜permissions.py
    ┃ ┣ 📜settings.py
    ┃ ┣ 📜urls.py
    ┃ ┣ 📜wsgi.py
    ┃ ┗ 📜__init__.py
    ┣ 📂teams
    ┃ ┣ 📜admin.py
    ┃ ┣ 📜apps.py
    ┃ ┣ 📜models.py
    ┃ ┣ 📜serializers.py
    ┃ ┣ 📜tests.py
    ┃ ┣ 📜urls.py
    ┃ ┣ 📜views.py
    ┃ ┗ 📜__init__.py
    ┣ 📂users
    ┃ ┣ 📜admin.py
    ┃ ┣ 📜apps.py
    ┃ ┣ 📜models.py
    ┃ ┣ 📜serializers.py
    ┃ ┣ 📜tests.py
    ┃ ┣ 📜urls.py
    ┃ ┣ 📜views.py
    ┃ ┗ 📜__init__.py
    ┣ 📜.env
    ┣ 📜.gitignore
    ┣ 📜db.json
    ┣ 📜db.sqlite3
    ┣ 📜manage.py
    ┣ 📜README.md
    ┣ 📜requirements.txt
    ┗ 📜swagger.py

기본 Django 프로젝트의 디렉터리 구조를 거의 그대로 사용하였습니다. DB 덤프 파일과 Swagger 파라미터를 저장한 파일은 개발 작업 시 편리하게 사용하기 위해 프로젝트 루트 폴더에 위치시켰습니다. 커스텀한 권한 파일은 Django와 연관되어 모든 앱에 사용되는 파일이기 때문에 config 폴더 아래에 위치시켰습니다.

</details>

<br/>

## API 문서

Swagger: `http://127.0.0.1:{port}`

<details>
    <summary>API 문서 확인</summary>
    
![Swagger](https://doc-images-s3.s3.ap-northeast-2.amazonaws.com/project_swagger.png)
</details>

<br/>

## ERD

![ERD](https://doc-images-s3.s3.ap-northeast-2.amazonaws.com/project-management-erd.png)

<br/>

## 프로젝트 진행 및 이슈 관리

GitHub 이슈 / GitHub 일정 관리

![GitHub이슈](https://doc-images-s3.s3.ap-northeast-2.amazonaws.com/project_issue.png)

![GitHub이슈상세](https://doc-images-s3.s3.ap-northeast-2.amazonaws.com/project_issue_detail.png)

![GitHub일정관리](https://doc-images-s3.s3.ap-northeast-2.amazonaws.com/project_manage.png)

<br/>

## 구현 과정

<details>
<summary>사용자 기능</summary>

-   [관련이슈 #2](https://github.com/allen9535/project-management-system/issues/2)
-   [관련이슈 #4](https://github.com/allen9535/project-management-system/issues/4)
-   [관련이슈 #5](https://github.com/allen9535/project-management-system/issues/5)
-   [관련이슈 #6](https://github.com/allen9535/project-management-system/issues/6)

1. 회원가입

    - 계정명, 비밀번호를 입력해야 합니다.
    - 계정명과 비밀번호는 사용자 인증에 사용됩니다.

2. 로그인

    - 계정명과 비밀번호를 입력하면 **JSON Web Token**을 발급합니다.
    - Access Token의 유효 기간은 1시간으로 사용자의 브라우저 등에 저장할 수 있도록 반환합니다.
    - Refresh Token의 경우 보안을 위해 서버에 캐시 데이터로 저장합니다.

3. 로그아웃

    - Access Token을 제출 받아 Rrefresh Token을 블랙리스트에 등록하는 것으로 토큰 재사용을 막습니다.

</details>

<details>
<summary>팀 기능</summary>

-   [관련이슈 #7](https://github.com/allen9535/project-management-system/issues/7)
-   [관련이슈 #8](https://github.com/allen9535/project-management-system/issues/8)
-   [관련이슈 #8](https://github.com/allen9535/project-management-system/issues/9)
-   [관련이슈 #11](https://github.com/allen9535/project-management-system/issues/11)

1.  팀 생성

    -   팀명을 입력해 새로운 팀을 생성합니다.
    -   모든 인증된 사용자에게 권한이 부여됩니다.
    -   팀을 생성한 사용자는 자동으로 팀장이 됩니다. 팀장은 팀 모델의 팀장 필드에 저장되기도 하지만, Django에서 기본적으로 제공하는 Group 기능을 활용해 팀장 그룹과 해당 팀 그룹에 포함되게 했습니다.
    -   기존에 다른 팀에 속해있던 사용자가 새 팀을 생성할 경우 기존 팀에서 탈퇴하고 새 팀의 팀장으로 옮겨가게 됩니다.
    -   만약 기존 팀의 팀장이 새 팀으로 옮겨가게 될 경우 남은 팀의 연장자(회원가입일이 가장 오래된 팀원)이 팀장이 됩니다.
    -   로직상 팀 생성·그룹 생성·팀 이동 등 여러 데이터의 저장이 함께 이루어져야 하기에 트랜잭션을 도입했습니다.

2.  팀 초대

    -   초대 대상의 계정명을 입력해 자신의 팀에 초대합니다.
    -   팀장에게만 권한이 부여됩니다.
    -   팀장이 자신의 팀에만 초대할 수 있습니다.
    -   자신 또는 다른 팀장이 특정 사용자를 이미 초대했을 경우, 더 이상 초대할 수 없는 상태임을 안내합니다.

3.  팀 초대 승락

    -   초대 받은 사용자는 그 초대를 수락할 수 있습니다.
    -   모든 인증된 사용자에게 권한이 부여됩니다.
    -   단, 초대 메시지가 없을 경우 초대 받은 팀이 없다는 것을 안내합니다.
    -   초대 메시지를 받은 사용자가 초대를 수락할 경우 해당하는 팀 그룹에 포함되며 초대 메시지는 비워집니다.
    -   기존에 다른 팀에 속해있던 사용자라면 기존 팀 그룹에서 제거하고 새 팀 그룹에 가입시킵니다.
    -   여러 데이터의 저장이 함께 이루어져야 하기에 트랜잭션을 도입했습니다.

</details>

<details>
<summary>보드 기능</summary>

-   [관련이슈 #10](https://github.com/allen9535/project-management-system/issues/10)
-   [관련이슈 #11](https://github.com/allen9535/project-management-system/issues/11)
-   [관련이슈 #12](https://github.com/allen9535/project-management-system/issues/12)
-   [관련이슈 #36](https://github.com/allen9535/project-management-system/issues/36)
-   [관련이슈 #37](https://github.com/allen9535/project-management-system/issues/37)
-   [관련이슈 #38](https://github.com/allen9535/project-management-system/issues/38)
-   [관련이슈 #39](https://github.com/allen9535/project-management-system/issues/39)
-   [관련이슈 #40](https://github.com/allen9535/project-management-system/issues/40)
-   [관련이슈 #41](https://github.com/allen9535/project-management-system/issues/41)
-   [관련이슈 #42](https://github.com/allen9535/project-management-system/issues/42)
-   [관련이슈 #43](https://github.com/allen9535/project-management-system/issues/43)
-   [관련이슈 #44](https://github.com/allen9535/project-management-system/issues/44)
-   [관련이슈 #45](https://github.com/allen9535/project-management-system/issues/45)
-   [관련이슈 #54](https://github.com/allen9535/project-management-system/issues/54)

1. 보드 생성

    - 사용자가 팀을 생성할 때 한 개의 보드도 함께 생성합니다. 이 보드는 프로젝트와 업무를 관리하는 단위이며 한 개의 팀이 한 개의 보드만 가질 수 있습니다.

2. 컬럼 추가

    - 컬럼은 업무를 구분하는 단위입니다. 보드 생성 초기에는 별도로 생성되어 있지 않으며, 팀장이 이름을 입력해 컬럼을 추가할 수 있습니다.
    - 팀장에게만 권한이 부여됩니다.
    - 컬럼이 추가될 때 순서값을 체크합니다. 사용자가 사용하는 화면 기준 왼쪽일수록 순서값이 작고, 오른쪽일수록 순서값이 큰 식입니다. 이에 새로 추가하는 컬럼은 현재 보드에 존재하는 컬럼들 중 가장 큰 순서값을 부여해 오른쪽에 위치시킵니다.

3. 컬럼 조회

    - 본인이 속한 팀이 소유하고 있는 보드의 컬럼 전체를 조회합니다.
    - 팀장과 팀원에게만 권한이 부여됩니다.
    - 컬럼의 순서값의 오름차순으로 반환됩니다. 이는 향후 프론트엔드에서 화면을 구성할 때 순서값이 작은 것부터 왼쪽에서 오른쪽으로 구성하는 것을 상정한 내용입니다.
    - 컬럼 내부에 속해있는 티켓의 내용도 함께 반환합니다.
    - 컬럼만 단독으로 조회되지는 않고, 팀에서 보드를 조회할 때 함께 조회되는 방식입니다.

4. 컬럼 수정

    - 컬럼 제목을 입력받아 수정합니다.
    - 팀장과 팀원에게만 권한이 부여됩니다.
    - 컬럼 순서의 경우 별도의 기능이므로 컬럼 수정 기능에서는 작동하지 않게 만들었습니다.

5. 컬럼 순서 수정

    - 컬럼 순서를 입력받아 수정합니다.
    - 팀장과 팀원에게만 권한이 부여됩니다.
    - 한 개 컬럼의 순서를 변경하게 되면 나머지 컬럼들도 순서를 변경해야 합니다.
    - 컬럼이 현재 순서값보다 큰 쪽으로 이동하게 되면, 현재 순서값 초과 이동할 순서값 이하의 순서값을 가진 컬럼들의 순서값을 모두 1씩 감산합니다.
    - 컬럼이 현재 순서값보다 작은 쪽으로 이동하게 되면 변경할 순서값 이상 현재 순서값 미만의 순서값을 가진 컬럼들의 순서값을 모두 1씩 가산합니다.
    - 해당 과정은 여러 값이 함께 수정되어야 하므로 트랜잭션으로 묶어 문제 발생시 롤백할 수 있도록 만들었습니다.

6. 컬럼 삭제

    - 컬럼 id를 입력받아 삭제합니다.
    - 팀장에게만 권한이 부여됩니다.

7. 티켓 추가

    - 티켓은 실제 업무 단위입니다. 보드나 컬럼 생성 초기에는 생성되어 있지 않으며, 팀장이나 팀원이 별도로 생성해야 합니다.
    - 팀장과 팀원에게만 권한이 부여됩니다.
    - 컬럼 id, 담당자, 티켓 제목, 태그, 작업량, 마감일을 입력받아 새 티켓을 생성하되, 담당자 필드는 필수값이 아닙니다. 이는 향후 별도로 담당자를 배정할 수 있도록 하려는 조치입니다.
    - 컬럼과 마찬가지로 순서값을 갖는데, 해당 티켓이 속한 컬럼 내에서의 순서를 말합니다. 별도로 입력받지 않아도 데이터를 조회하여 나중에 생성된 티켓일수록 큰 순서값을 갖도록 설정했습니다.

8. 티켓 수정

    - 담당자, 티켓 제목, 태그, 작업량, 마감일을 수정할 수 있습니다.
    - 팀장과 팀원에게만 권한이 부여됩니다.
    - 순서 수정의 경우 별도의 기능에서 담당하므로 티켓 수정 기능에서는 작동하지 않도록 만들었습니다.

9. 티켓 순서 수정

    - 티켓 id와 변경할 티켓 순서값, 컬럼 순서값을 입력받아 티켓의 순서를 수정합니다.
    - 팀장과 팀원에게만 권한이 있습니다.
    - 티켓은 소속된 컬럼 이외의 다른 컬럼으로도 이동할 수 있습니다.
    - 컬럼 단위의 변경이 없다면 컬럼 순서 수정과 비슷한 과정을 거칩니다.
    - 컬럼 단위의 변경이 있을 경우, 이동할 티켓이 도착할 컬럼의 티켓 순서값 이상의 값들을 모두 1씩 가산한 다음 빈 자리에 티켓을 이동시킵니다. 이동한 티켓이 원래 있던 컬럼의 티켓들은 다시 순서를 매깁니다.
    - 해당 과정은 여러 값이 함께 수정되어야 하므로 트랜잭션으로 묶어 문제 발생시 롤백할 수 있도록 만들었습니다.

10. 티켓 삭제

    - 티켓 id를 입력받아 해당하는 티켓을 삭제합니다.
    - 팀장과 팀원에게만 권한이 있습니다.
    - 티켓이 삭제된 다음에 빈 값이 발생할 수 있으므로 남은 티켓들의 순서값을 다시 매깁니다
    - 해당 과정은 여러 값이 함께 수정되어야 하므로 트랜잭션으로 묶어 문제 발생시 롤백할 수 있도록 만들었습니다.

</details>

<br/>

## 회고

<details>
<summary>배포 자동화(또는 지속적 배포) 구축</summary>

-   프로젝트를 Docker화 하여 EC2에 배포하는 경험은 있습니다. 그러나 배포 자동화에 대해 알게된 후, 한 번 배포 자동화를 구축해 놓으면 편리하겠다는 생각이 들었습니다.
-   Jenkins, Redhat 등 여러 배포 자동화 도구가 있었지만 저는 GitHub Actions를 사용하기로 했습니다. 배포 자동화에 대해 잘 모르는 제가 간단하게 배우고 시도해보기에는 GitHub Actions가 편리하다고 판단했기 때문입니다. 또 형상 관리를 위해 GitHub을 사용하고 있었기에 별도의 설정 없이 사용할 수 있다는 점도 제게는 장점이었습니다.
-   워크 플로우 파일을 작성했습니다. main 브랜치에 push가 발생하게 되면, 기존에 생성한 EC2 인스턴스에 접속해, GitHub main 브랜치에 push된 코드를 내려받도록 구성했습니다.
-   가장 어려웠던 부분은 GitHub Actions에서 제공하는 환경에서 AWS의 EC2에 접속하는 것이었습니다. SSH를 통해 접속해야 했는데 평소에 Tabby와 같은 도구를 사용해 접속하던 저로써는 다소 난해했습니다.
-   그러나 시행착오 끝에 성공적으로 배포 자동화를 구축할 수 있었습니다. 당 프로젝트 역시 main 브랜치에 push가 발생하게 되면 EC2 서버에서 자동으로 해당 코드를 다운로드합니다.

</details>

<details>
<summary>트랜잭션</summary>

-   당 프로젝트를 진행하며 다양한 데이터를 한꺼번에 저장·수정하는 경험을 하게 되었습니다. 동시에 오류가 발생하면 어떤 데이터는 변경되고 어떤 데이터는 그대로 남는 경험을 하게 되었습니다.
-   어떻게 하면 이 작업들을 하나로 묶어줄 수 있을까 고민하다 트랜잭션이라는 개념에 대해 알게 되었습니다. 트랜잭션은 DB 상태를 변화시키는 작업들을 하나로 묶은 단위이며, Django에도 이를 지원하기 위해 다양한 기능들이 제공된다는 것이었습니다.
-   이에 하나의 작업 단위가 되어야 하는 코드들을 transaction.atomic() 함수를 통해 묶었습니다. 이를 통해 묶여진 작업 단위가 모두 성공하지 않으면 DB의 데이터가 변화하지 않는다는 것을 보장할 수 있게 되었습니다.

</details>

<br/>

## 작성자

-   [전정헌](https://github.com/allen9535)
