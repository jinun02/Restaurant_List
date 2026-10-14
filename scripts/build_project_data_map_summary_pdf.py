from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, PageBreak, Paragraph, Preformatted, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "pdf" / "프로젝트_데이터와_지도_구현_간소화본.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

font_path = Path(r"C:\Windows\Fonts\NotoSansKR-VF.ttf")
if not font_path.exists():
    font_path = Path(r"C:\Windows\Fonts\malgun.ttf")
pdfmetrics.registerFont(TTFont("KR", str(font_path)))
pdfmetrics.registerFont(TTFont("KRB", str(font_path)))

BLACK = colors.HexColor("#000000")
LINE = colors.HexColor("#CCCCCC")
LIGHT = colors.HexColor("#F2F2F2")
LIGHTER = colors.HexColor("#FAFAFA")
base = getSampleStyleSheet()
TITLE = ParagraphStyle("Title", parent=base["Title"], fontName="KRB", fontSize=26, leading=36, alignment=TA_CENTER, textColor=BLACK)
SUBTITLE = ParagraphStyle("Subtitle", parent=base["Normal"], fontName="KR", fontSize=10, leading=17, alignment=TA_CENTER, textColor=BLACK)
H1 = ParagraphStyle("H1", parent=base["Heading1"], fontName="KRB", fontSize=18, leading=25, textColor=BLACK, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=base["Heading2"], fontName="KRB", fontSize=12.5, leading=18, textColor=BLACK, spaceBefore=8, spaceAfter=5)
BODY = ParagraphStyle("Body", parent=base["BodyText"], fontName="KR", fontSize=9.6, leading=15.5, textColor=BLACK, spaceAfter=7, wordWrap="CJK")
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8, leading=12.5)
CODE = ParagraphStyle("Code", fontName="KR", fontSize=7.7, leading=11, textColor=BLACK, leftIndent=7, rightIndent=7, borderColor=LINE, borderWidth=0.6, borderPadding=8, backColor=LIGHTER, spaceBefore=3, spaceAfter=8)


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.setFont("KR", 7.5)
    canvas.setFillColor(BLACK)
    canvas.drawString(18 * mm, 8.5 * mm, "프로젝트 데이터·지도 구현 간소화본")
    canvas.drawRightString(width - 18 * mm, 8.5 * mm, str(doc.page))
    canvas.restoreState()


doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, title="프로젝트 데이터와 지도 구현 간소화본",
                      leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm, bottomMargin=18 * mm)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
doc.addPageTemplates(PageTemplate(id="all", frames=[frame], onPage=footer))
story = []


def p(text, style=BODY): story.append(Paragraph(text, style))
def h1(text): story.append(Paragraph(text, H1))
def h2(text): story.append(Paragraph(text, H2))
def code(text): story.append(Preformatted(text.strip("\n"), CODE))


def box(title, text):
    item = Table([[Paragraph(f"<b>{title}</b><br/>{text}", BODY)]], colWidths=[166 * mm])
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), LIGHTER), ("BOX", (0, 0), (-1, -1), 0.8, BLACK),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([item, Spacer(1, 7)])


def qna(question, answer):
    box("★ 핵심 질문과 답변", f"<b>질문</b>  {question}<br/><br/><b>답변</b>  {answer}")


def table(rows, widths):
    item = Table([[Paragraph(str(c), SMALL) for c in row] for row in rows], colWidths=widths, repeatRows=1)
    item.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("FONTNAME", (0, 0), (-1, 0), "KRB"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHTER]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(item)


# 표지
story.append(Spacer(1, 45 * mm))
p("QUICK PROJECT GUIDE", ParagraphStyle("Label", parent=SMALL, fontName="KRB", alignment=TA_CENTER, fontSize=9))
story.extend([Spacer(1, 7 * mm), Paragraph("CSV부터 지도 표시까지<br/>핵심 구현 요약", TITLE)])
p("Kakao Maps · Google Maps · 마커 · GPS · 길찾기", SUBTITLE)
story.append(Spacer(1, 18 * mm))
box("이 PDF의 목적", "21페이지 상세 설명서에서 꼭 알아야 할 코드와 작동 원리만 골라 빠르게 복습할 수 있도록 정리했습니다.")
story.append(PageBreak())


h1("목차")
table([
    ["장", "내용", "페이지"],
    ["1", "프로젝트 전체 흐름", "3"],
    ["2", "CSV 파일 읽기와 변환", "4"],
    ["3", "카카오 지도와 마커", "5"],
    ["4", "GeoJSON·GPS·카카오 길찾기", "6"],
    ["5", "메인 화면의 구글 지도", "7"],
    ["6", "구글 마커·GPS 정확도 원·상세 지도", "8"],
    ["7", "카카오·구글 비교와 오류 확인", "9"],
], [15 * mm, 136 * mm, 15 * mm])
box("추천 사용법", "코드 흐름은 1~2장, 카카오는 3~4장, 구글은 5~6장, 두 지도의 차이와 오류 해결은 7장에서 확인합니다.")
story.append(PageBreak())


h1("1. 프로젝트 전체 흐름")
p("CSV 파일을 지도에 바로 넣는 것이 아니라, 텍스트를 JavaScript 객체로 변환한 다음 위도·경도로 지도 마커를 만든다.")
code("""CSV 파일
  ↓ fetch() + response.text()
CSV 문자열
  ↓ parseCsv() + toRestaurant()
식당 객체 배열
  ↓ 지도 SDK와 Marker 생성자
카카오 또는 구글 지도 마커""")
table([
    ["화면", "지도 SDK", "담당 파일"],
    ["맛집 탐색·길찾기", "Kakao Maps", "restaurantMap.js"],
    ["메인 미니맵", "Google Maps", "restaurant_homepageMap.js"],
    ["음식점 상세", "Google Maps", "restaurantDetailMap.js"],
], [52 * mm, 48 * mm, 66 * mm])
h2("HTML과 스크립트 순서")
code("""<!-- 지도가 표시될 빈 영역 -->
<div id="map-api"></div>

<!-- 키와 데이터 서비스를 먼저 준비 -->
<script src="map-config-KakaoJS.js"></script>
<script src="restaurantService.js"></script>
<script src="restaurantMap.js"></script>""")
p("지도 div에는 CSS width와 height가 있어야 한다. 필요한 전역 객체가 먼저 생성되도록 API 키·데이터 서비스·지도 파일 순서로 실행한다.")
qna("카카오 지도와 구글 지도를 동시에 사용하는가요?", "그렇다. 맛집 탐색은 카카오 지도이고 메인·상세 화면은 구글 지도다. 두 SDK의 지도와 마커 객체는 서로 다르다.")
story.append(PageBreak())


h1("2. CSV 파일 읽기와 변환")
h2("CSV 요청")
code("""async function loadRestaurants() {
    // CSV 파일의 HTTP 응답을 기다린다.
    const response = await fetch(RESTAURANT_CSV_URL, {
        cache: 'no-store'
    });

    if (!response.ok) throw new Error('CSV 요청 실패');

    // CSV는 JSON이 아니라 텍스트로 읽는다.
    const csvText = await response.text();

    return parseCsv(csvText)
        .map(toRestaurant)
        .filter(Boolean);
}""")
h2("텍스트를 객체로 변환")
code("""const lines = csvText
    .replace(/^\\uFEFF/, '') // BOM 제거
    .split(/\\r?\\n/)      // 줄 단위 분리
    .filter(line => line.trim() !== '');

const latitude = Number(row['위도']);
const longitude = Number(row['경도']);

return {
    name: row['음식점명'],
    latitude,
    longitude
};""")
p("CSV 값은 처음에는 문자열이다. 좌표는 Number()로 변환하며, 따옴표 안 쉼표를 올바르게 처리하기 위해 실제 프로젝트는 parseCsvLine()을 별도로 사용한다.")
qna("왜 response.json()이 아니라 response.text()를 사용하나요?", "CSV는 JSON 문법이 아닌 일반 텍스트다. 문자열로 받은 뒤 CSV 규칙에 맞춰 행과 열을 직접 나눠야 한다.")
story.append(PageBreak())


h1("3. 카카오 지도와 마커")
h2("SDK와 지도 본체")
code("""// 카카오 JavaScript 키로 SDK 주소를 만든다.
script.src =
    `https://dapi.kakao.com/v2/maps/sdk.js` +
    `?appkey=${encodeURIComponent(apiKey)}&autoload=false`;
script.onload = () => kakao.maps.load(initFoodMap);
document.head.appendChild(script);

// 맛집 탐색 지도 본체를 생성한다.
map = new kakao.maps.Map(mapElement, {
    center: new kakao.maps.LatLng(37.8813, 127.7298),
    level: 7
});""")
h2("CSV 좌표로 카카오 마커 생성")
code("""restaurants.forEach(restaurant => {
    const marker = new kakao.maps.Marker({
        map,
        position: new kakao.maps.LatLng(
            restaurant.latitude,
            restaurant.longitude
        ),
        title: restaurant.name
    });

    kakao.maps.event.addListener(marker, 'click', () => {
        openRestaurantGroup(marker, [restaurant]);
    });
});""")
p("필터를 다시 적용할 때는 기존 마커에 marker.setMap(null)을 호출한 뒤 새 마커를 만든다. 카카오 마커는 kakao.maps.Marker 객체다.")
qna("marker.setMap(null)은 구글 지도 코드인가요?", "카카오와 구글 모두 같은 이름의 메서드를 제공한다. 이 코드의 객체가 kakao.maps.Marker라면 카카오 마커를 제거하는 동작이다.")
story.append(PageBreak())


h1("4. GeoJSON·GPS·카카오 길찾기")
h2("행정동 경계")
code("""const responses = await Promise.all([
    fetch(DISTRICT_URL),
    fetch(CITY_URL)
]);

const [district, city] = await Promise.all(
    responses.map(response => response.json())
);

// GeoJSON [경도, 위도] → Kakao (위도, 경도)
const latLng = coordinate =>
    new kakao.maps.LatLng(coordinate[1], coordinate[0]);""")
h2("GPS 실시간 위치")
code("""const DEFAULT_OPTIONS = {
    enableHighAccuracy: true, // 정확도 높은 측정 요청
    timeout: 10000,           // 최대 10초 대기
    maximumAge: 0             // 과거 캐시 위치 사용 안 함
};

watchId = navigator.geolocation.watchPosition(
    onPosition,
    onError,
    DEFAULT_OPTIONS
);""")
h2("카카오 자동차 길찾기")
code("""const response = await fetch(`${DIRECTIONS_ENDPOINT}?${query}`, {
    headers: {
        Authorization: `KakaoAK ${getApiKey()}`
    }
});

// 받은 좌표를 선으로 연결한다.
routePolyline = new kakao.maps.Polyline({ map, path });""")
qna("GPS accuracy는 보정된 좌표인가요?", "아니다. 브라우저가 알려주는 예상 오차 반경(m)이다. 현재 프로젝트에는 여러 좌표를 평균 내는 별도 보정 알고리즘은 없다.")
story.append(PageBreak())


h1("5. 메인 화면의 구글 지도")
h2("Google Maps SDK")
code("""window.initHomepageMap = initHomepageMap;

const script = document.createElement('script');
script.src =
    'https://maps.googleapis.com/maps/api/js' +
    `?key=${encodeURIComponent(apiKey)}` +
    '&callback=initHomepageMap&v=weekly' +
    '&language=ko&region=KR';
script.async = true;
script.defer = true;
document.head.appendChild(script);""")
h2("지도 본체")
code("""map = new google.maps.Map(
    document.getElementById('homepage-map'),
    {
        center: { lat: 37.8813, lng: 127.7298 },
        zoom: 13,
        mapTypeControl: false,
        streetViewControl: false
    }
);""")
p("SDK 주소의 callback=initHomepageMap은 스크립트 로딩 완료 후 실행할 전역 함수를 지정한다. 구글 지도는 { lat, lng } 객체를 좌표로 사용하며 zoom 값이 클수록 확대된다.")
qna("SDK를 불러오는 것과 지도 객체를 만드는 것은 다른가요?", "그렇다. SDK 로딩은 google.maps 기능을 브라우저에 준비하고, new google.maps.Map()은 그 기능으로 실제 지도 인스턴스를 생성한다.")
story.append(PageBreak())


h1("6. 구글 마커·GPS 정확도 원·상세 지도")
h2("순위 음식점 마커")
code("""const bounds = new google.maps.LatLngBounds();

const marker = new google.maps.Marker({
    map,
    position: { lat: latitude, lng: longitude },
    label: { text: String(index + 1), color: '#ffffff' },
    title: restaurant.name
});

bounds.extend(marker.getPosition());
map.fitBounds(bounds, 64);""")
h2("현재 위치와 예상 오차 범위")
code("""currentLocationMarker = new google.maps.Marker({
    map,
    position: location,
    icon: { path: google.maps.SymbolPath.CIRCLE }
});

currentLocationAccuracyCircle = new google.maps.Circle({
    map,
    center: location,
    radius: position.accuracy // 미터 단위 예상 오차 반경
});""")
h2("상세 페이지")
code("""map = new google.maps.Map(mapElement, {
    center: position,
    zoom: 17
});

marker = new google.maps.Marker({ map, position });""")
p("메인 화면은 여러 순위 마커와 GPS 정확도 원을 표시한다. 상세 페이지는 선택한 음식점 한 곳을 중심으로 지도와 마커 하나를 표시한다.")
qna("정확도 원이 클수록 GPS가 정확한가요?", "반대다. 원의 반지름이 클수록 예상 오차 범위가 넓어 정확도가 낮다는 뜻이다.")
story.append(PageBreak())


h1("7. 카카오·구글 비교와 오류 확인")
table([
    ["구분", "카카오", "구글"],
    ["사용 화면", "맛집 탐색·길찾기", "메인·상세"],
    ["지도", "kakao.maps.Map", "google.maps.Map"],
    ["마커", "kakao.maps.Marker", "google.maps.Marker"],
    ["좌표", "LatLng(위도, 경도)", "{ lat, lng }"],
    ["확대", "level 작을수록 확대", "zoom 클수록 확대"],
    ["범위", "setBounds()", "fitBounds()"],
    ["특징", "경계·자동차 경로", "순위·GPS 정확도 원"],
], [32 * mm, 67 * mm, 67 * mm])
h2("오류 확인 순서")
code("""1. Console에서 JavaScript 오류 확인
2. Network에서 CSV·GeoJSON·SDK 상태 코드 확인
3. 지도 div의 width와 height 확인
4. API 키 종류와 허용 도메인 확인
5. CSV 좌표가 유효한 숫자인지 확인""")
table([
    ["문제", "핵심 확인"],
    ["CSV가 안 읽힘", "로컬 서버 실행·경로·response.ok"],
    ["지도가 안 보임", "API 키·SDK·지도 div 높이"],
    ["마커가 안 보임", "위도·경도 순서와 Number 변환"],
    ["마커가 중복됨", "setMap(null) 후 배열 초기화"],
    ["길찾기 401", "KakaoAK REST API 인증 헤더"],
], [55 * mm, 111 * mm])
box("마지막 정리", "CSV는 text()로 읽고 객체 배열로 변환한다. 맛집 탐색은 카카오 지도, 메인·상세는 구글 지도다. 각 지도에서 해당 SDK의 Map과 Marker 객체를 사용한다.")
p("상세판: pdf/프로젝트_데이터와_지도_구현_설명서.pdf", SMALL)
p("기준 소스: restaurantService.js, restaurantMap.js, restaurant_homepageMap.js, restaurantDetailMap.js, geolocationService.js, directionsService.js", SMALL)


doc.build(story)
print(OUTPUT)
