from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

FONT = Path(r"C:\Windows\Fonts\NotoSansKR-VF.ttf")
if not FONT.exists():
    FONT = Path(r"C:\Windows\Fonts\malgun.ttf")

pdfmetrics.registerFont(TTFont("KR", str(FONT)))
pdfmetrics.registerFont(TTFont("KR-Bold", str(FONT)))

NAVY = colors.HexColor("#16324F")
BLUE = colors.HexColor("#2563EB")
SKY = colors.HexColor("#EAF2FF")
GREEN = colors.HexColor("#16845B")
PALE_GREEN = colors.HexColor("#EAF7F1")
GOLD = colors.HexColor("#F4B400")
PALE_GOLD = colors.HexColor("#FFF7D6")
TEXT = colors.HexColor("#25313C")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#D8E0E8")
CODE_BG = colors.HexColor("#F4F6F8")


styles = getSampleStyleSheet()
TITLE = ParagraphStyle(
    "TitleKR", parent=styles["Title"], fontName="KR-Bold", fontSize=27,
    leading=36, textColor=NAVY, alignment=TA_CENTER, spaceAfter=12,
)
SUBTITLE = ParagraphStyle(
    "SubtitleKR", parent=styles["Normal"], fontName="KR", fontSize=11,
    leading=18, textColor=MUTED, alignment=TA_CENTER,
)
H1 = ParagraphStyle(
    "H1KR", parent=styles["Heading1"], fontName="KR-Bold", fontSize=18,
    leading=25, textColor=NAVY, spaceBefore=6, spaceAfter=12,
)
H2 = ParagraphStyle(
    "H2KR", parent=styles["Heading2"], fontName="KR-Bold", fontSize=13,
    leading=19, textColor=GREEN, spaceBefore=10, spaceAfter=7,
)
BODY = ParagraphStyle(
    "BodyKR", parent=styles["BodyText"], fontName="KR", fontSize=9.5,
    leading=16, textColor=TEXT, spaceAfter=7, wordWrap="CJK",
)
SMALL = ParagraphStyle(
    "SmallKR", parent=BODY, fontSize=8, leading=13, textColor=MUTED,
)
QUESTION = ParagraphStyle(
    "QuestionKR", parent=BODY, fontName="KR-Bold", fontSize=10.2,
    leading=16, textColor=NAVY, spaceAfter=4,
)
ANSWER = ParagraphStyle(
    "AnswerKR", parent=BODY, leftIndent=9, borderColor=LINE,
    borderWidth=0, borderPadding=0, spaceAfter=10,
)
CODE = ParagraphStyle(
    "CodeKR", fontName="KR", fontSize=7.3, leading=11,
    textColor=colors.HexColor("#1F2937"), leftIndent=7, rightIndent=7,
    borderColor=LINE, borderWidth=0.5, borderPadding=8,
    backColor=CODE_BG, spaceBefore=4, spaceAfter=9,
)


def footer(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.setFont("KR", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 8.5 * mm, "Restaurant List - 지도/API 정리")
    canvas.drawRightString(width - 18 * mm, 8.5 * mm, str(doc.page))
    canvas.restoreState()


def document(path, title):
    doc = BaseDocTemplate(
        str(path), pagesize=A4, title=title,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=17 * mm, bottomMargin=18 * mm,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="all", frames=[frame], onPage=footer))
    return doc


def cover(story, title, subtitle, label):
    story += [Spacer(1, 48 * mm)]
    story.append(Paragraph(label, ParagraphStyle(
        "CoverLabel", parent=SMALL, alignment=TA_CENTER,
        fontName="KR-Bold", textColor=GREEN, fontSize=10,
    )))
    story += [Spacer(1, 8 * mm), Paragraph(title, TITLE), Paragraph(subtitle, SUBTITLE)]
    story += [Spacer(1, 22 * mm)]
    box = Table([[Paragraph(
        "춘천 음식점 지도 프로젝트<br/>카카오 지도 · Google 지도 · GeoJSON · GPS · 길찾기",
        ParagraphStyle("CoverBox", parent=BODY, alignment=TA_CENTER, fontSize=10, leading=18),
    )]], colWidths=[142 * mm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_GREEN),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#B9DFC9")),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(box)
    story.append(PageBreak())


def h1(story, text):
    story.append(Paragraph(text, H1))


def h2(story, text):
    story.append(Paragraph(text, H2))


def p(story, text, style=BODY):
    story.append(Paragraph(text, style))


def code(story, text):
    story.append(Preformatted(text.strip("\n"), CODE))


def source(story, path, lines):
    p(story, f"원본 위치: <b>{path}</b> {lines}", SMALL)


def callout(story, title, text, color=SKY, edge=BLUE):
    table = Table([[Paragraph(f"<b>{title}</b><br/>{text}", BODY)]], colWidths=[166 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.8, edge),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    story += [table, Spacer(1, 7)]


def flow(story, items):
    cells = [[Paragraph(f"<b>{i + 1}</b><br/>{item}", SMALL) for i, item in enumerate(items)]]
    widths = [166 * mm / len(items)] * len(items)
    table = Table(cells, colWidths=widths)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKY),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#BFD3F8")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFD3F8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story += [table, Spacer(1, 8)]


def build_guide():
    path = OUT / "지도_API_코드_설명서.pdf"
    story = []
    cover(story, "지도 · API 코드 설명서", "TXT 설명을 반영한 상세판 - 구조, 문법, 실행 흐름", "DETAILED TECHNICAL GUIDE")

    h1(story, "1. 한눈에 보는 파일 역할")
    data = [
        ["파일", "담당 기능"],
        ["restaurantMap.js", "카카오 지도, 행정동 경계, 음식점 마커, 현재 위치"],
        ["restaurantExplorer.js", "지역·카테고리·즐겨찾기 필터와 목록 연동"],
        ["directionsService.js", "카카오모빌리티 REST API로 자동차 경로 요청"],
        ["directionsController.js", "출발지·도착지와 경로선 UI 제어"],
        ["geolocationService.js", "브라우저 GPS 현재 위치 조회·추적"],
        ["nearbyRestaurantService.js", "직선거리 계산과 주변 맛집 검색"],
        ["restaurant_homepageMap.js", "메인 홈페이지 Google 미니 지도"],
    ]
    table = Table([[Paragraph(str(c), SMALL) for c in row] for row in data], colWidths=[54 * mm, 112 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "KR-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    callout(story, "핵심 구분", "맛집 탐색 화면은 카카오 지도, 메인·상세 미니 지도는 Google 지도를 사용한다.")

    story.append(PageBreak())
    h1(story, "2. 카카오 지도와 GeoJSON")
    p(story, "춘천시 외곽선과 행정동 면 영역은 GeoJSON 파일에서 읽는다. 지도 화면은 카카오 JavaScript SDK가 담당한다.")
    flow(story, ["GeoJSON 요청", "JSON 객체 변환", "좌표 순서 변환", "Polygon·Polyline 생성"])
    source(story, "js/restaurantMap.js", "164~171줄")
    code(story, """const responses = await Promise.all([
    fetch(DISTRICT_URL),
    fetch(CITY_URL)
]);

if (responses.some(response => !response.ok)) {
    throw new Error('경계 파일을 불러오지 못했습니다.');
}

[districtGeoJson, cityGeoJson] = await Promise.all(
    responses.map(response => response.json())
);""")
    h2(story, "왜 response.ok를 확인하나?")
    p(story, "fetch는 404나 500 응답에서도 Promise 자체가 완료될 수 있다. 따라서 HTTP 요청이 성공 범위(200~299)인지 직접 확인한다.")
    h2(story, "response => !response.ok를 풀어 쓰면")
    code(story, """// 화살표 함수
response => !response.ok

// 같은 뜻의 일반 함수
function (response) {
    return !response.ok;
}""")
    p(story, "responses.some(...)은 배열의 응답을 하나씩 검사한다. response.ok가 false인 응답을 찾으면 !false가 true가 되고, some()은 즉시 true를 반환한다. 즉 ‘두 파일 중 하나라도 실패했는가?’를 검사하는 코드다.")
    h2(story, "좌표 순서를 왜 바꾸나?")
    code(story, """// GeoJSON: [경도, 위도]
// Kakao LatLng: (위도, 경도)
const latLng = coordinate =>
    new kakao.maps.LatLng(coordinate[1], coordinate[0]);""")
    callout(story, "★ 예상 질문", "GeoJSON을 사용한 이유는? 행정동 이름뿐 아니라 실제 면 경계 좌표가 필요했기 때문이다.", PALE_GOLD, GOLD)

    h2(story, "Polygon과 MultiPolygon 처리")
    source(story, "js/restaurantMap.js", "46줄")
    code(story, """const polygonsOf = geometry =>
    geometry.type === 'Polygon'
        ? [geometry.coordinates]
        : geometry.coordinates;""")
    p(story, "Polygon과 MultiPolygon은 좌표 배열의 중첩 깊이가 다르다. Polygon도 배열로 한 번 감싸면 이후 반복문이 두 형식을 같은 방식으로 처리할 수 있다.")
    h2(story, "경계 도형을 다시 그리는 이유")
    p(story, "사용자가 행정동 선택을 바꾸면 과거 Polygon과 Polyline을 먼저 setMap(null)로 제거한다. 제거하지 않으면 이전 경계와 새 경계가 겹치고, 선택 상태와 화면이 달라진다.")
    code(story, """const clearOverlays = overlays => {
    overlays.forEach(overlay => overlay.setMap(null));
    overlays.length = 0;
};""")
    callout(story, "실행 결과", "‘전체’ 선택 시 춘천시 외곽선을, 특정 동 선택 시 행정동 면을 강조하고 LatLngBounds로 선택 영역 전체가 보이게 한다.", PALE_GREEN, GREEN)

    story.append(PageBreak())
    h1(story, "3. 음식점 마커와 필터")
    source(story, "js/restaurantMap.js", "203~228줄")
    p(story, "새 데이터를 그리기 전에 기존 마커를 지도에서 제거하고 배열도 비운다. 그렇지 않으면 실행할 때마다 같은 마커와 클릭 이벤트가 겹친다.")
    code(story, """restaurantMarkers.forEach(({ marker }) =>
    marker.setMap(null)
);
restaurantMarkers = [];""")
    callout(story, "정확한 의미", "카카오 지도 전체를 초기화하는 것이 아니라 음식점 마커만 정리한 뒤 최신 데이터로 다시 만든다.", PALE_GREEN, GREEN)
    h2(story, "같은 좌표의 음식점 묶기")
    p(story, "동일 건물에 음식점이 여러 개 있으면 마커가 완전히 겹친다. 위도와 경도를 소수점 8자리 문자열로 만든 뒤 Map의 key로 사용해 같은 위치를 한 그룹으로 묶는다.")
    code(story, """const groups = new Map();

restaurants.forEach(restaurant => {
    const key =
        `${restaurant.latitude.toFixed(8)},` +
        `${restaurant.longitude.toFixed(8)}`;
    const group = groups.get(key) || [];
    group.push(restaurant);
    groups.set(key, group);
});""")
    p(story, "마커는 그룹마다 하나만 생성하고, 클릭 시 같은 위치의 음식점 목록을 정보창에서 보여준다. toFixed(8)은 작은 부동소수점 차이 때문에 같은 위치가 다른 그룹이 되는 문제를 줄인다.")
    h2(story, "필터 조건")
    code(story, """const matchesFilter = restaurant =>
    (selectedDistricts.has(ALL) ||
        selectedDistricts.has(restaurant.district)) &&
    (selectedCategory === ALL ||
        restaurant.category === selectedCategory) &&
    (favoriteRestaurantKeys === null ||
        favoriteRestaurantKeys.has(getRestaurantKey(restaurant)));""")
    p(story, "지역·카테고리·즐겨찾기 조건을 모두 통과한 음식점만 표시한다. `marker.setMap(map)`은 표시, `marker.setMap(null)`은 숨김이다.")
    h2(story, "즐겨찾기 데이터 연결")
    source(story, "js/restaurantExplorer.js", "16~38줄")
    p(story, "즐겨찾기 저장 ID는 ‘행정동_카테고리_순번’이지만 지도 CSV는 그 순번을 직접 알지 못한다. 따라서 즐겨찾기 항목을 ‘행정동|음식점명’ 형태로 변환해 지도 데이터와 비교한다.")
    code(story, """function syncFavoriteMarkers() {
    window.RestaurantMap?.selectFavorites(
        favoritesOnly
            ? getFavoriteRestaurantKeys()
            : null
    );
}""")
    p(story, "favoritesOnly가 true면 즐겨찾기 키 배열을 전달하고, false면 null을 전달해 필터를 해제한다. ?.는 RestaurantMap이 아직 준비되지 않은 경우 호출 오류를 막는다.")
    callout(story, "★ 예상 질문", "같은 좌표의 음식점은 왜 묶나? 같은 건물의 마커가 겹치는 문제를 막고 하나의 정보창에서 여러 음식점을 보여주기 위해서다.", PALE_GOLD, GOLD)

    h1(story, "4. GPS와 주변 맛집")
    flow(story, ["위치 권한 요청", "현재 좌표 획득", "직선거리 계산", "반경 필터", "거리 표시"])
    source(story, "js/geolocationService.js", "24~40줄")
    code(story, """navigator.geolocation.getCurrentPosition(
    position => resolve({
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy
    }),
    error => reject(new Error(getErrorMessage(error)))
);""")
    h2(story, "GPS 옵션과 오류 처리")
    data = [
        ["옵션", "의미", "고려할 점"],
        ["enableHighAccuracy", "가능하면 높은 정확도 요청", "응답·배터리 비용 증가 가능"],
        ["timeout: 10000", "최대 10초 대기", "초과 시 오류 코드 3"],
        ["maximumAge: 0", "캐시 위치 사용 안 함", "새 위치를 요청"],
    ]
    gps_table = Table([[Paragraph(str(c), SMALL) for c in row] for row in data], colWidths=[43 * mm, 61 * mm, 62 * mm])
    gps_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [gps_table, Spacer(1, 8)]
    p(story, "오류 코드 1은 권한 거부, 2는 위치 확인 불가, 3은 시간 초과다. 숫자 코드를 사용자에게 이해되는 문장으로 변환한다. 페이지를 나갈 때 clearWatch로 위치 추적을 중지해 불필요한 조회를 막는다.")
    h2(story, "하버사인 공식이 필요한 이유")
    p(story, "위도·경도는 평면 좌표가 아니므로 단순 차이만으로 km 거리를 구할 수 없다. 하버사인은 지구 곡면을 고려하고, 음식점마다 길찾기 API를 호출하지 않아 주변 후보를 빠르게 찾는다.")
    source(story, "js/nearbyRestaurantService.js", "30~50줄")
    code(story, """const haversine =
    Math.sin(latitudeDifference / 2) ** 2 +
    Math.cos(startLatitude) *
    Math.cos(endLatitude) *
    Math.sin(longitudeDifference / 2) ** 2;

return EARTH_RADIUS_KM * 2 * Math.atan2(
    Math.sqrt(haversine),
    Math.sqrt(1 - haversine)
);""")
    h2(story, "반경 필터와 정렬")
    p(story, "각 음식점까지 distanceKm를 계산한 뒤 radiusKm보다 먼 항목은 제외한다. sortBy가 distance이면 가까운 순, rating이면 평점·리뷰 수를 우선하고 동률일 때 거리순으로 정렬한다. 좌표가 잘못된 음식점은 개별 try/catch로 제외해 전체 검색이 중단되지 않게 한다.")
    callout(story, "실제 화면", "메인 홈페이지의 ‘내 주변 맛집’ 탭에서 250m·500m·1km·직접 설정 반경과 음식점 거리를 표시한다.", PALE_GREEN, GREEN)
    callout(story, "주의", "하버사인 결과는 직선거리다. 실제 자동차 도로 거리는 카카오 길찾기 API 결과를 사용한다.")

    h1(story, "5. 카카오 자동차 길찾기")
    flow(story, ["출발지·도착지", "REST API 요청", "JSON 응답", "vertexes 추출", "Polyline 표시"])
    source(story, "js/directionsService.js", "15~64줄")
    code(story, """const response = await fetch(
    `${DIRECTIONS_ENDPOINT}?${query}`,
    {
        headers: {
            Authorization: `KakaoAK ${getApiKey()}`
        }
    }
);

if (!response.ok) {
    throw new Error(`길찾기 요청 실패 (${response.status})`);
}

const data = await response.json();""")
    h2(story, "요청 query의 의미")
    data = [
        ["항목", "값", "설명"],
        ["origin", "경도,위도", "자동차 출발 위치"],
        ["destination", "경도,위도", "자동차 도착 위치"],
        ["priority", "RECOMMEND", "추천 경로 요청"],
        ["alternatives", "false", "대안 경로 생략"],
        ["road_details", "false", "상세 도로 정보 생략"],
    ]
    query_table = Table([[Paragraph(str(c), SMALL) for c in row] for row in data], colWidths=[39 * mm, 45 * mm, 82 * mm])
    query_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [query_table, Spacer(1, 8)]
    p(story, "지도 LatLng는 위도,경도 순서지만 REST API query는 경도,위도 순서다. 두 규격을 혼동하면 다른 위치의 경로가 검색되므로 요청 단계와 표시 단계를 구분해야 한다.")
    h2(story, "두 단계의 오류 검사")
    p(story, "첫째 response.ok로 HTTP 통신 성공을 확인한다. 401·403은 인증 또는 권한 문제로 따로 안내한다. 둘째 route.result_code로 실제 자동차 경로 계산 성공을 확인한다. HTTP가 200이어도 경로가 없을 수 있기 때문이다.")
    h2(story, "경로 좌표 구조")
    p(story, "응답 구조는 routes → sections → roads → vertexes다. vertexes는 [경도, 위도, 경도, 위도, ...] 형태라 두 칸씩 읽는다.")
    source(story, "js/directionsController.js", "146~164줄")
    code(story, """const path = route.points.map(point =>
    new kakao.maps.LatLng(
        point.latitude,
        point.longitude
    )
);

routePolyline = new kakao.maps.Polyline({
    map, path,
    strokeWeight: 7,
    strokeColor: '#eb1111'
});""")
    callout(story, "★ 예상 질문", "JavaScript SDK와 REST API의 차이는? SDK는 지도 요소를 브라우저에 그리며, REST API는 서버가 계산한 자동차 경로 JSON을 반환한다.", PALE_GOLD, GOLD)
    h2(story, "화면 제어와 중복 요청 방지")
    p(story, "길찾기 버튼을 누르면 출발지·도착지 존재 여부를 먼저 검사한다. 요청 중에는 버튼을 disabled 상태로 만들고, try에서 요청·표시, catch에서 오류 안내, finally에서 버튼 복구를 수행한다.")
    code(story, """try {
    const route = await DirectionsService.findDrivingRoute(
        routeLocations.origin,
        routeLocations.destination
    );
    drawRoute(route);
} catch (error) {
    clearRoute();
    showRouteResult(error.message, true);
} finally {
    routeSubmitButton.disabled = false;
}""")

    h1(story, "6. 지도 API를 불러오는 순서")
    h2(story, "카카오 지도 SDK")
    flow(story, ["설정 파일에서 키 읽기", "script 요소 생성", "SDK 주소 지정", "head에 추가", "onload 후 지도 생성"])
    source(story, "js/restaurantMap.js", "257줄부터")
    code(story, """const script = document.createElement('script');
script.src =
    'https://dapi.kakao.com/v2/maps/sdk.js' +
    `?appkey=${encodeURIComponent(apiKey)}` +
    '&autoload=false';
script.async = true;
script.onload = () => kakao.maps.load(initFoodMap);
document.head.appendChild(script);""")
    p(story, "createElement만으로는 다운로드가 시작되지 않는다. appendChild로 실제 HTML head에 넣는 순간 브라우저가 SDK를 요청한다.")
    h2(story, "onload, onerror, autoload=false")
    p(story, "script.onload는 SDK 파일 다운로드 성공 후 실행되고, script.onerror는 네트워크 문제 등으로 파일 자체를 받지 못했을 때 실행된다. autoload=false를 사용했으므로 onload 이후 kakao.maps.load(initFoodMap)을 직접 호출해 SDK 내부 준비가 끝난 뒤 지도를 생성한다.")
    h2(story, "설정 파일이 먼저 실행되어야 하는 이유")
    code(story, """<!-- 키를 먼저 window에 등록 -->
<script src="../js/map-config-KakaoJS.js"></script>

<!-- 그 다음 키를 읽는 지도 코드 실행 -->
<script src="../js/restaurantMap.js"></script>""")
    p(story, "HTML의 일반 script 태그는 위에서 아래로 실행된다. 순서를 바꾸면 restaurantMap.js가 실행될 때 window.KAKAO_JS_MAPS_API_KEY가 없어 지도가 비활성화될 수 있다.")
    h2(story, "Google 미니 지도 SDK")
    p(story, "Google 지도는 URL의 callback 이름을 SDK 로딩 완료 후 호출한다. 따라서 초기화 함수를 window에 등록해야 한다.")
    code(story, """window.initHomepageMap = initHomepageMap;
script.src =
    'https://maps.googleapis.com/maps/api/js' +
    `?key=${encodeURIComponent(apiKey)}` +
    '&callback=initHomepageMap' +
    '&language=ko&region=KR';""")

    story.append(PageBreak())
    h1(story, "7. API 키 보안과 구조 개선")
    callout(story, "중요", "브라우저 JavaScript에 들어간 키는 완전히 숨길 수 없다. 지도 JavaScript 키에는 허용 도메인과 API 제한을 반드시 설정한다.", PALE_GOLD, GOLD)
    p(story, "카카오 REST 키는 프런트엔드 코드와 네트워크 요청에서 노출될 수 있다. 실제 배포에서는 백엔드가 키를 환경 변수로 보관하고 카카오 API를 대신 호출하는 구조가 더 안전하다.")
    p(story, "이미 공개 저장소에 올라간 키는 파일에서 지우는 것만으로 부족하다. 키를 폐기·재발급하고 Git 기록 노출 여부도 확인한다.")
    h2(story, "권장 구조")
    flow(story, ["브라우저", "자체 백엔드", "카카오 API", "필요 결과만 반환"])
    p(story, "브라우저는 자체 백엔드에 출발지·도착지만 보낸다. 백엔드는 환경 변수에 저장한 REST 키로 카카오 API를 호출한다. 이렇게 하면 REST 키가 브라우저 코드와 개발자 도구에 직접 노출되지 않는다.")
    h2(story, "추가 개선 항목")
    p(story, "음식점 이름 대신 고유 ID 사용, 지도 제공자 통일, 마커 클러스터링, 화면 범위 기반 로딩, 요청 취소(AbortController), 오류 재시도 UI와 자동화 테스트를 적용할 수 있다.")

    story.append(PageBreak())
    h1(story, "8. 전체 작동 흐름")
    flow(story, ["페이지 실행", "지도 SDK 로딩", "GeoJSON·CSV 로딩", "경계·마커 표시"])
    flow(story, ["사용자 필터", "마커 표시 갱신", "GPS 선택", "주변 맛집 계산"])
    flow(story, ["출발지·도착지", "REST API", "경로 좌표", "지도 경로선"])
    h2(story, "발표 전 빠른 체크")
    checks = [
        ["질문", "한 문장 답변"],
        ["메인 지도 파일", "restaurant_homepageMap.js - Google 미니 지도"],
        ["카카오 지도 파일", "restaurantMap.js - 탐색 지도와 마커·경계"],
        ["주변 맛집 거리", "하버사인 직선거리 - API 요청 없이 후보 검색"],
        ["자동차 경로", "카카오모빌리티 REST API - 실제 도로 거리"],
        ["가장 중요한 보안 개선", "REST 키와 API 호출을 백엔드로 이동"],
    ]
    check_table = Table(
        [[Paragraph(str(c), SMALL) for c in row] for row in checks],
        colWidths=[54 * mm, 112 * mm],
    )
    check_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "KR-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [check_table, Spacer(1, 8)]
    p(story, "설명 원본은 txt/map_code, 예상 질문 원본은 txt/Q&Atxt에 보관되어 있다.", SMALL)

    document(path, "지도 API 코드 설명서").build(story)
    return path


def qa(story, number, question, answer, star=False):
    mark = "★ " if star else ""
    block = [
        Paragraph(f"{mark}Q{number}. {question}", QUESTION),
        Paragraph(f"A. {answer}", ANSWER),
    ]
    story.append(KeepTogether(block))


def build_qna():
    path = OUT / "지도_API_핵심_QnA.pdf"
    story = []
    cover(story, "지도 · API 상세 Q&A", "핵심 질문 40개와 이어지는 꼬리 질문", "DETAILED PRESENTATION Q&A")

    sections = [
        ("1. 지도와 GeoJSON", [
            ("맛집 탐색 페이지는 어떤 지도 API를 사용했나요?", "카카오 지도 JavaScript SDK를 사용했습니다. restaurantMap.js가 지도, 마커, 행정동 경계와 현재 위치를 관리합니다.", True),
            ("메인 홈페이지 지도도 카카오 지도인가요?", "아닙니다. 메인·상세 미니 지도는 Google 지도이고, 맛집 탐색 화면은 카카오 지도입니다.", True),
            ("GeoJSON을 사용한 이유는 무엇인가요?", "행정동 이름뿐 아니라 실제 면 경계 좌표가 필요했기 때문입니다. 춘천시 외곽선과 행정동 영역을 지도에 그립니다.", True),
            ("GeoJSON 좌표 순서를 왜 바꾸나요?", "GeoJSON은 [경도, 위도], 카카오 LatLng는 (위도, 경도) 순서이기 때문입니다.", True),
            ("두 경계 파일을 Promise.all로 읽은 이유는?", "서로 독립적인 요청을 동시에 실행해 순차 요청보다 로딩 시간을 줄이기 위해서입니다.", False),
        ]),
        ("2. 마커와 필터", [
            ("기존 마커를 먼저 제거하는 이유는 무엇인가요?", "마커 생성 함수가 다시 실행될 때 같은 마커와 클릭 이벤트가 중복되는 것을 막기 위해서입니다.", True),
            ("setMap(null)은 지도 전체 초기화인가요?", "아닙니다. 해당 음식점 마커만 지도에서 분리합니다. 지도와 행정동 경계는 유지됩니다.", True),
            ("같은 좌표의 음식점을 왜 묶었나요?", "같은 건물의 마커 겹침을 막고 하나의 정보창에서 여러 음식점을 보여주기 위해서입니다.", True),
            ("필터는 어떤 조건으로 동작하나요?", "지역·카테고리·즐겨찾기 조건을 모두 만족한 음식점만 마커로 표시합니다.", False),
            ("즐겨찾기 키를 왜 변환하나요?", "즐겨찾기 저장 형식과 지도 CSV의 식별 형식이 달라 행정동|음식점명 형태의 공통 키가 필요합니다.", True),
        ]),
        ("3. GPS와 주변 맛집", [
            ("현재 위치는 어떤 API로 가져오나요?", "지도 회사 API가 아니라 브라우저의 navigator.geolocation을 사용합니다.", True),
            ("Geolocation API를 Promise로 감싼 이유는?", "콜백 API를 await 방식으로 읽기 쉽게 사용하고 오류 처리를 통일하기 위해서입니다.", False),
            ("하버사인 공식이 왜 필요한가요?", "위도·경도와 지구 곡면을 고려해 직선거리를 계산하고, 음식점마다 길찾기 API를 호출하지 않고 주변 후보를 빠르게 찾기 위해서입니다.", True),
            ("하버사인 거리는 실제 자동차 거리인가요?", "아닙니다. 직선거리입니다. 실제 도로 거리는 카카오 길찾기 API 결과를 사용합니다.", True),
            ("이 기능은 실제 화면 어디에 있나요?", "메인 홈페이지의 내 주변 맛집 탭입니다. 250m·500m·1km·직접 설정 반경과 음식점 거리를 표시합니다.", True),
        ]),
        ("4. 자동차 길찾기", [
            ("길찾기는 어떤 API를 사용하나요?", "카카오모빌리티 자동차 길찾기 REST API를 사용합니다.", True),
            ("출발지 좌표를 왜 경도,위도로 보내나요?", "카카오모빌리티 REST API 요청 규격이 x,y 즉 경도,위도 순서이기 때문입니다.", True),
            ("await fetch의 의미는 무엇인가요?", "서버 응답이 도착해 실제 Response 객체를 받을 때까지 해당 async 함수의 다음 실행을 기다린다는 뜻입니다.", True),
            ("response.ok는 무엇인가요?", "HTTP 상태 코드가 200~299 범위인지 나타내는 Boolean 속성입니다.", True),
            ("경로 좌표는 응답 어디에 있나요?", "routes → sections → roads → vertexes에 있으며, 경도와 위도가 번갈아 저장됩니다.", False),
            ("index를 2씩 증가시키는 이유는?", "vertexes에서 한 좌표가 경도와 위도 두 숫자로 구성되기 때문입니다.", False),
            ("경로를 지도에 어떻게 그리나요?", "좌표를 kakao.maps.LatLng로 바꾼 뒤 kakao.maps.Polyline의 path에 전달합니다.", True),
            ("이전 경로선을 왜 제거하나요?", "새 검색 결과와 과거 경로가 겹치지 않게 하기 위해서입니다.", False),
        ]),
        ("5. API 로딩과 보안", [
            ("카카오 지도 SDK는 어떻게 불러오나요?", "script 요소를 동적으로 만들고 SDK URL을 설정한 뒤 document.head.appendChild로 HTML에 추가합니다.", True),
            ("appendChild가 왜 필요한가요?", "createElement는 메모리에 요소만 만들며, 실제 HTML에 추가해야 브라우저가 SDK 다운로드를 시작합니다.", True),
            ("autoload=false를 사용한 이유는?", "다운로드 직후 자동 실행하지 않고 kakao.maps.load로 SDK 준비 완료 시점을 제어하기 위해서입니다.", False),
            ("script.onload와 onerror의 차이는?", "onload는 SDK 다운로드 성공, onerror는 파일 자체를 받지 못했을 때 실행됩니다.", True),
            ("Google callback을 왜 window에 등록하나요?", "SDK URL에는 함수 이름 문자열이 전달되므로 Google이 전역 객체에서 그 함수를 찾을 수 있어야 합니다.", True),
            ("JavaScript SDK와 REST API 차이는?", "SDK는 지도 클래스와 화면 요소를 제공하고, REST API는 서버가 계산한 JSON 데이터를 반환합니다.", True),
            ("브라우저의 API 키를 완전히 숨길 수 있나요?", "없습니다. JavaScript 지도 키는 도메인·API 제한으로 보호하고, REST 키는 백엔드로 옮기는 것이 안전합니다.", True),
        ]),
        ("6. JavaScript 문법", [
            ("response => !response.ok는 무슨 뜻인가요?", "각 응답의 ok 값을 반대로 바꿔 실패 응답인지 검사하는 화살표 함수입니다.", True),
            ("some은 어떻게 작동하나요?", "배열 요소 중 하나라도 조건이 true면 즉시 true를 반환합니다.", False),
            ("window.restaurantData || {}는 왜 쓰나요?", "전역 데이터가 없을 때 빈 객체를 기본값으로 사용해 Object.entries 등의 오류를 막기 위해서입니다.", True),
            ("?.는 무엇인가요?", "왼쪽 값이 null 또는 undefined가 아닐 때만 다음 속성이나 함수를 사용하는 선택적 연결 연산자입니다.", False),
            ("visible ? map : null은 무엇인가요?", "조건이 참이면 마커를 지도에 표시하고 거짓이면 숨기는 삼항 연산자입니다.", False),
        ]),
        ("7. 오류와 개선", [
            ("지도가 안 보이면 무엇부터 확인하나요?", "API 키·허용 도메인·SDK 네트워크 요청·콘솔 오류·지도 div 높이 순서로 확인합니다.", True),
            ("401과 403 오류는 어떻게 다른가요?", "401은 주로 인증 실패, 403은 사용 권한이나 애플리케이션 설정 문제일 수 있습니다.", True),
            ("현재 구조의 가장 중요한 보안 개선점은?", "카카오 REST API 호출을 백엔드로 이동하고 키를 서버 환경 변수로 보관하는 것입니다.", True),
            ("데이터가 많아지면 무엇을 개선할 수 있나요?", "마커 클러스터링, 화면 범위 기반 로딩, 기존 마커 재사용, API 요청 취소를 적용할 수 있습니다.", False),
            ("프로젝트를 한 문장으로 설명한다면?", "춘천 음식점 CSV와 행정구역 GeoJSON을 지도에 결합하고 필터·GPS 주변 검색·자동차 길찾기를 연동한 맛집 탐색 웹입니다.", True),
        ]),
    ]

    number = 1
    for idx, (section, questions) in enumerate(sections):
        h1(story, section)
        if idx == 0:
            callout(story, "읽는 법", "★ 표시는 발표·코드 리뷰에서 특히 나올 가능성이 높은 질문이다.", PALE_GOLD, GOLD)
        for question, answer, star in questions:
            qa(story, number, question, answer, star)
            number += 1
        if idx in (1, 3, 5):
            story.append(PageBreak())

    story.append(PageBreak())
    h1(story, "8. 꼬리 질문 - 조금 더 자세한 답변")
    callout(story, "답변 방법", "기능 설명 → 선택 이유 → 실제 화면 활용 순서로 답하면 짧지만 설득력 있게 설명할 수 있다.", PALE_GREEN, GREEN)
    detailed = [
        ("왜 카카오 지도와 Google 지도를 함께 사용했나요?",
         "현재 프로젝트 구조에서는 맛집 탐색 화면이 카카오 지도 기능을 중심으로 구현됐고, 메인·상세 미니 지도는 기존 Google 지도 모듈을 유지했습니다. 기능상 동작하지만 키 관리와 유지보수가 두 갈래가 되므로 장기적으로 한 제공자로 통일하는 것이 개선점입니다."),
        ("왜 음식점 마커를 필터마다 새로 만들지 않고 숨기나요?",
         "지역·카테고리 변경은 표시 조건만 달라지는 작업입니다. 기존 Marker 객체를 유지한 채 setMap(map/null)로 연결 상태만 바꾸면 마커 생성과 이벤트 재등록 비용을 줄일 수 있습니다. 데이터 자체를 다시 불러올 때만 전체 마커를 초기화하고 재생성합니다."),
        ("하버사인 대신 모든 음식점에 길찾기 API를 호출하면 안 되나요?",
         "가능하지만 음식점 수만큼 네트워크 요청이 필요해 느리고 API 할당량도 많이 사용합니다. 하버사인으로 직선거리 후보를 브라우저에서 빠르게 거른 뒤, 사용자가 선택한 한 경로에만 길찾기 API를 사용하는 것이 효율적입니다."),
        ("GPS 정확도 값은 어디에 활용하나요?",
         "position.coords.accuracy를 미터 단위로 받아 현재 위치 상태 문구에 표시합니다. 사용자는 위치 결과가 어느 정도 정확한지 판단할 수 있습니다. 정확도가 낮더라도 주변 검색은 가능하지만 반경이 작을수록 결과 오차가 커질 수 있습니다."),
        ("HTTP 성공과 경로 계산 성공을 왜 따로 검사하나요?",
         "response.ok는 서버 통신이 HTTP 수준에서 성공했는지 확인합니다. 하지만 HTTP 200이어도 자동차로 갈 수 없는 좌표처럼 경로 계산 결과가 실패할 수 있으므로 route.result_code도 별도로 검사해야 합니다."),
        ("script.onerror와 API 인증 오류의 차이는 무엇인가요?",
         "script.onerror는 SDK JavaScript 파일 자체를 다운로드하지 못한 경우입니다. 인증 오류는 SDK는 로드됐지만 키, 도메인, API 활성화 설정이 거부된 경우입니다. 문제 원인이 다르므로 사용자 메시지도 구분합니다."),
        ("즐겨찾기를 음식점 이름으로 연결할 때 문제는 없나요?",
         "같은 행정동에 같은 이름의 음식점이 있거나 이름이 변경되면 잘못 연결될 수 있습니다. 현재 구조를 연결하기 위한 실용적인 방식이지만, 데이터에 변하지 않는 고유 restaurantId를 추가하는 것이 더 안전합니다."),
        ("GeoJSON 내부 경계선을 제거하는 원리는 무엇인가요?",
         "여러 행정동 Polygon의 선분을 시작·끝 좌표 조합으로 저장합니다. 같은 선분이 두 번 나오면 두 동이 맞닿은 내부 경계이고, 한 번만 나온 선분은 선택 영역의 바깥 윤곽이므로 그것만 강조합니다."),
        ("API 키 정규식 검사가 보안을 보장하나요?",
         "아닙니다. 정규식은 빈 값이나 형식이 명백히 잘못된 키를 미리 찾는 입력 검증일 뿐입니다. 실제 보안은 허용 도메인·API 제한, 키 재발급, REST 요청의 백엔드 이전으로 확보해야 합니다."),
        ("프로젝트에서 가장 먼저 개선할 한 가지는 무엇인가요?",
         "카카오모빌리티 REST API 호출을 백엔드로 이동하는 것입니다. 현재 브라우저가 REST 키를 직접 사용하면 개발자 도구에서 확인할 수 있으므로, 서버가 환경 변수로 키를 보관하고 필요한 경로 결과만 반환하도록 바꾸는 것이 우선입니다."),
    ]
    for i, (question, answer) in enumerate(detailed, start=number):
        if i == 50:
            story.append(PageBreak())
        qa(story, i, question, answer, True)

    h1(story, "마지막 30초 요약")
    p(story, "카카오 지도는 restaurantMap.js가 담당하며, GeoJSON으로 행정동 경계를 그리고 CSV 음식점을 마커로 표시한다. GPS와 하버사인 공식으로 주변 맛집을 빠르게 찾고, 선택한 출발지·도착지는 카카오모빌리티 REST API로 실제 자동차 경로를 계산한다. 메인·상세 미니 지도는 Google 지도를 사용한다.")
    callout(story, "발표 팁", "기술 이름만 말하기보다 ‘왜 선택했는지’와 ‘어디 화면에서 쓰이는지’를 함께 답하면 이해하기 쉽다.", PALE_GREEN, GREEN)
    h2(story, "상황별 답변 틀")
    templates = [
        ["질문 유형", "답변 순서"],
        ["이 코드는 무엇인가?", "문법 뜻 → 입력값 → 반환값 → 호출 위치"],
        ["왜 이 방식을 썼나?", "해결할 문제 → 선택 이유 → 다른 방식과 차이"],
        ["화면 어디에 쓰이나?", "사용자 동작 → 실행 함수 → 화면 결과"],
        ["오류가 나면?", "검사 조건 → 사용자 메시지 → 복구 또는 개선 방법"],
    ]
    template_table = Table(
        [[Paragraph(str(c), SMALL) for c in row] for row in templates],
        colWidths=[52 * mm, 114 * mm],
    )
    template_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story += [template_table, Spacer(1, 9)]
    callout(story, "헷갈리기 쉬운 세 가지", "GeoJSON·REST query의 좌표는 경도,위도지만 kakao.maps.LatLng는 위도,경도다. 하버사인은 직선거리이며 길찾기는 도로 거리다. setMap(null)은 객체 삭제가 아니라 지도에서 숨기는 동작이다.", PALE_GOLD, GOLD)

    document(path, "지도 API 핵심 Q&A").build(story)
    return path


if __name__ == "__main__":
    outputs = [build_guide(), build_qna()]
    for output in outputs:
        print(output)
