# AIA6_BackEnd
AIA6_BackEnd

장르와 평점을 기준으로 영화를 추천해주는 사이트입니다.


![photo-1485846234645-a62644f84728](https://github.com/nueeng/AIA6_BackEnd/assets/127704498/3122696a-1247-442b-9f4b-4bf357419313)
웹페이지 이미지 들어갈 예정  

[Frontend Repository](https://github.com/nueeng/AIA6_FrontEnd)  

## 📚 Stacks

<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"><img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"><img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"><img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">

<img src="https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white"><img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">

<img src="https://img.shields.io/badge/TMDB-pink?style=for-the-badge&logo=themoviedatabase&logoColor=black">


## 📽 Dependency

의존성 PIP



## 🎬 Features

- 로그인 / 회원가입
    - 회원가입(이메일 or 소셜은 추후 논의)
    - 로그인
    - 로그아웃
    - 마이페이지  
  
- 영화
    - TMDB API를 사용하여 간략한 영화정보에 후기를 달 수 있는 게시판 기능
    - 후기 CRUD (TextField 짧게 한줄평 느낌으로!)
    - 좋아요 기능

- 영화 추천 과정
    - 관심있는 장르 or 영화 수집 페이지
    1. TMDB API 중 Trending 랜덤 10개 띄워주기 (영화 제목 / 포스터)
    2. 하나를 선택 = input, 근데 없으면?(다시 검색하기 - 또 스무개/위에서 띄운 10개는 제외)
    3. 해당 영화 줄거리 / 포스터 / 후기 + AI가 input과 장르가 유사하고 평점이 높은 영화 추천 3개 (영화 상세 페이지)

## 👤 Implement AI
<br/>

AI가 구현되는 과정 상세히 적어보기

 ## Team
 
<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://github.com/JooHan10"><img src="https://avatars.githubusercontent.com/u/116674496?v=4" width="100px;" alt=""/><br /><sub><b>팀장 : 이주한</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/Songjimyung"><img src="https://avatars.githubusercontent.com/u/116045723?v=4" width="100px;" alt=""/><br /><sub><b>팀원 : 송지명</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/Jihunz123 "><img src="https://avatars.githubusercontent.com/u/126747911?v=4" width="100px;" alt=""/><br /><sub><b>팀원 : 이지훈</b></sub></a><br /></td>
      <td align="center"><a href="https://github.com/nueeng"><img src="https://avatars.githubusercontent.com/u/127704498?v=4" width="100px;" alt=""/><br /><sub><b>팀원 : 최준영</b></sub></a><br /></td>
    <tr/>
  </tbody>
</table>

## ✅ Checklist

0. **※ Machine Learning**
1. 좌측 메뉴 바 슬라이드 인 / 슬라이드 아웃 기능
2. 영화 추천 페이지 모달 기능
3. 디자인 조금 더 다듬기
4. 구글 소셜 로그인 기능
5. tmdb api 이용한 프로젝트라고 소개글 추가
6. 개발 끝난 후, print문이나 쓸데없는 주석, 사용되지 않는 코드 등의 legacy code 삭제시간 갖기
7. review모델 평점 필드(rating)가 없다✅
8. likes 테스트코드✅
9. movie admin 등록✅
10. review에서 movie_id 활용 로직 구체화✅
11. 계정 아이디 validation 먹통현상