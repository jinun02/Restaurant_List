import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/봄내로그_사용자_여정_흐름도.pptx";
const PREVIEW = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/journey-preview.png";
const LAYOUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/journey-layout.json";

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}

const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const slide = deck.slides.add();
slide.background.fill = "#F7FAF4";

slide.shapes.add({
  geometry: "rect",
  name: "green-frame",
  position: { left: 26, top: 24, width: 1228, height: 672 },
  fill: "none",
  line: { style: "solid", fill: "#86C94A", width: 16 },
});

function textBox(name, text, x, y, w, h, size, color, bold = false, align = "left") {
  const box = slide.shapes.add({
    geometry: "textbox",
    name,
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = text;
  box.text.style = {
    fontFamily: "Malgun Gothic",
    fontSize: size,
    color,
    bold,
    alignment: align,
    verticalAlignment: "middle",
  };
  return box;
}

textBox("title", "맛집을 발견하고 기록하기까지", 72, 47, 1136, 48, 32, "#17351B", true, "center");
textBox("subtitle", "봄내로그의 핵심 사용자 여정", 400, 96, 480, 26, 16, "#5F7762", false, "center");

const stages = [
  { n: "01", title: "발견", page: "메인 화면", detail: "추천 맛집\n지역·소식 확인" },
  { n: "02", title: "검색과 필터", page: "통합 검색", detail: "동네 선택\n업종별 필터" },
  { n: "03", title: "탐색", page: "맛집 탐색", detail: "식당 목록\n지도·마커 비교" },
  { n: "04", title: "상세 확인", page: "식당 상세", detail: "메뉴·사진·평점\n리뷰·위치 확인" },
  { n: "05", title: "행동과 기록", page: "사용자 활동", detail: "길찾기·즐겨찾기\n리뷰·댓글 작성" },
];

const xs = [70, 305, 540, 775, 1010];
const cards = [];

for (let i = 0; i < stages.length; i += 1) {
  const x = xs[i];
  const isFinal = i === stages.length - 1;
  const card = slide.shapes.add({
    geometry: "roundRect",
    name: `stage-${i + 1}`,
    position: { left: x, top: 198, width: 200, height: 222 },
    fill: isFinal ? "#DCF4C1" : i === 2 || i === 3 ? "#E9F8D8" : "#FFFFFF",
    line: { style: "solid", fill: isFinal ? "#65AA32" : "#9BCB72", width: isFinal ? 2.6 : 2 },
    borderRadius: "rounded-2xl",
    shadow: "shadow-sm",
  });
  cards.push(card);

  const badge = slide.shapes.add({
    geometry: "ellipse",
    name: `badge-${i + 1}`,
    position: { left: x + 74, top: 176, width: 52, height: 52 },
    fill: isFinal ? "#65AA32" : "#7DBC45",
    line: { style: "solid", fill: "#F7FAF4", width: 4 },
  });
  badge.text = stages[i].n;
  badge.text.style = { fontFamily: "Malgun Gothic", fontSize: 15, bold: true, color: "#FFFFFF", alignment: "center", verticalAlignment: "middle" };

  textBox(`stage-title-${i + 1}`, stages[i].title, x + 18, 238, 164, 34, 19, "#17351B", true, "center");
  textBox(`stage-page-${i + 1}`, stages[i].page, x + 18, 282, 164, 34, 16, "#57922F", true, "center");
  textBox(`stage-detail-${i + 1}`, stages[i].detail, x + 20, 325, 160, 70, 15, "#516255", false, "center");
}

const arrow = { type: "arrow", width: "med", length: "med" };
for (let i = 0; i < cards.length - 1; i += 1) {
  slide.shapes.connect(cards[i], cards[i + 1], {
    kind: "straight",
    fromSide: "right",
    toSide: "left",
    line: { style: "solid", fill: "#5E7D62", width: 2.5 },
    tail: arrow,
  });
}

// Persistent account layer supporting the journey without interrupting the main path.
slide.shapes.add({
  geometry: "roundRect",
  name: "account-lane",
  position: { left: 70, top: 475, width: 1140, height: 152 },
  fill: "#EFF7E9",
  line: { style: "solid", fill: "#B2CF9A", width: 1.5 },
  borderRadius: "rounded-xl",
});
textBox("account-label", "회원 기능", 92, 493, 150, 31, 18, "#34523A", true, "left");
textBox("account-caption", "탐색은 비회원도 가능하고, 로그인하면 개인 기록이 이어집니다", 245, 493, 690, 31, 15, "#657768", false, "left");

function laneNode(name, label, x, w) {
  const shape = slide.shapes.add({
    geometry: "roundRect",
    name,
    position: { left: x, top: 546, width: w, height: 54 },
    fill: "#FFFFFF",
    line: { style: "solid", fill: "#A5C88A", width: 1.8 },
    borderRadius: "rounded-xl",
  });
  shape.text = label;
  shape.text.style = { fontFamily: "Malgun Gothic", fontSize: 16, bold: true, color: "#35513A", alignment: "center", verticalAlignment: "middle" };
  return shape;
}

const join = laneNode("join", "회원가입 · 로그인", 270, 210);
const profile = laneNode("profile", "프로필 · 마이페이지", 535, 210);
const history = laneNode("history", "즐겨찾기 · 내 활동", 800, 210);

const joinToProfile = slide.shapes.connect(join, profile, {
  kind: "straight", fromSide: "right", toSide: "left",
  line: { style: "solid", fill: "#78917B", width: 2 }, tail: arrow,
});
joinToProfile.bringToFront();
const profileToHistory = slide.shapes.connect(profile, history, {
  kind: "straight", fromSide: "right", toSide: "left",
  line: { style: "solid", fill: "#78917B", width: 2 }, tail: arrow,
});
profileToHistory.bringToFront();

textBox("footer-note", "공통 헤더 검색은 어느 화면에서든 다시 탐색 흐름으로 연결됩니다", 280, 646, 720, 25, 14, "#6A7E6D", false, "center");

slide.speakerNotes.textFrame.setText(
  "[Sources]\n- Repository README.md: main page, search, region/category filtering, restaurant list and maps, restaurant detail, directions, reviews/comments, favorites, and My Page.\n- Repository docs/auth-guide.md: signup/login, profile menu, session state, and user activity linkage.\n- Earlier user-provided slide image: retained green visual family only; the journey structure is newly composed."
);

await writeBlob(PREVIEW, await deck.export({ slide, format: "png", scale: 2 }));
await fs.writeFile(LAYOUT, await (await slide.export({ format: "layout" })).text());
const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(OUT);
console.log(OUT);
