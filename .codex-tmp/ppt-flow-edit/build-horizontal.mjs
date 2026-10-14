import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/봄내로그_프로젝트_흐름도_가로형.pptx";
const PREVIEW = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/horizontal-preview.png";
const LAYOUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/horizontal-layout.json";

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

function textBox(name, text, x, y, w, h, size, color, bold = false, align = "center") {
  const box = slide.shapes.add({
    geometry: "textbox",
    name,
    position: { left: x, top: y, width: w, height: h },
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = text;
  box.text.style = { fontFamily: "Malgun Gothic", fontSize: size, color, bold, alignment: align, verticalAlignment: "middle" };
  return box;
}

textBox("title", "봄내로그 페이지 구성과 사용자 흐름", 72, 48, 1136, 48, 32, "#17351B", true);
textBox("subtitle", "주요 탐색 경로를 왼쪽에서 오른쪽으로 표현", 350, 97, 580, 28, 16, "#637865");

function node(name, label, x, y, w, h, kind = "action", size = 16) {
  const c = {
    main: ["#E2F8C7", "#6FB339", "#17351B"],
    core: ["#D6F2B7", "#5FA331", "#17351B"],
    action: ["#FFFFFF", "#93C867", "#17351B"],
    side: ["#F0F8E7", "#AECF92", "#35523A"],
    feature: ["#F8FCF4", "#B9D7A0", "#35523A"],
  }[kind];
  const shape = slide.shapes.add({
    geometry: "roundRect",
    name,
    position: { left: x, top: y, width: w, height: h },
    fill: c[0],
    line: { style: "solid", fill: c[1], width: kind === "main" || kind === "core" ? 2.4 : 1.8 },
    borderRadius: "rounded-xl",
    shadow: kind === "main" || kind === "core" ? "shadow-sm" : undefined,
  });
  shape.text = label;
  shape.text.style = { fontFamily: "Malgun Gothic", fontSize: size, bold: true, color: c[2], alignment: "center", verticalAlignment: "middle" };
  return shape;
}

// Main horizontal path.
const home = node("home", "메인 화면", 60, 290, 160, 72, "main", 19);
const search = node("search", "헤더 통합 검색", 270, 238, 180, 58, "action", 16);
const region = node("region", "지역 선택", 270, 356, 180, 58, "action", 16);
const filter = node("filter", "동네 · 업종 필터", 500, 290, 180, 72, "core", 16);
const explorer = node("explorer", "식당 목록\n지도 · 마커", 730, 290, 180, 72, "action", 16);
const detail = node("detail", "식당 상세 정보", 960, 290, 180, 72, "core", 17);

// Detail outcomes are stacked to keep the main route compact.
const directions = node("directions", "길찾기", 1150, 226, 90, 48, "feature", 15);
const reviews = node("reviews", "리뷰 · 댓글", 1150, 302, 90, 48, "feature", 14);
const favorites = node("favorites", "즐겨찾기", 1150, 378, 90, 48, "feature", 15);

// Supporting content and account branches.
const content = node("content", "서비스 소개\n소식 · 공지", 60, 158, 160, 66, "side", 15);
const auth = node("auth", "로그인 · 회원가입", 60, 470, 180, 60, "side", 16);
const accountFind = node("account-find", "아이디 · 비밀번호 찾기", 300, 455, 205, 52, "feature", 14);
const profile = node("profile", "프로필 · 마이페이지", 300, 530, 205, 52, "feature", 14);
const activity = node("activity", "즐겨찾기 · 내 활동", 565, 530, 190, 52, "feature", 14);

const arrow = { type: "arrow", width: "med", length: "med" };
const coreLine = { style: "solid", fill: "#57785B", width: 2.5 };
const sideLine = { style: "solid", fill: "#99B09B", width: 1.9 };

slide.shapes.connect(home, search, { kind: "elbow", fromSide: "right", toSide: "left", line: coreLine, tail: arrow });
slide.shapes.connect(home, region, { kind: "elbow", fromSide: "right", toSide: "left", line: coreLine, tail: arrow });
slide.shapes.connect(search, filter, { kind: "elbow", fromSide: "right", toSide: "top", line: coreLine, tail: arrow });
slide.shapes.connect(region, filter, { kind: "elbow", fromSide: "right", toSide: "bottom", line: coreLine, tail: arrow });
slide.shapes.connect(filter, explorer, { kind: "straight", fromSide: "right", toSide: "left", line: coreLine, tail: arrow });
slide.shapes.connect(explorer, detail, { kind: "straight", fromSide: "right", toSide: "left", line: coreLine, tail: arrow });
slide.shapes.connect(detail, directions, { kind: "elbow", fromSide: "right", toSide: "left", line: coreLine, tail: arrow });
slide.shapes.connect(detail, reviews, { kind: "straight", fromSide: "right", toSide: "left", line: coreLine, tail: arrow });
slide.shapes.connect(detail, favorites, { kind: "elbow", fromSide: "right", toSide: "left", line: coreLine, tail: arrow });

slide.shapes.connect(home, content, { kind: "straight", fromSide: "top", toSide: "bottom", line: sideLine, tail: arrow });
slide.shapes.connect(home, auth, { kind: "straight", fromSide: "bottom", toSide: "top", line: sideLine, tail: arrow });
slide.shapes.connect(auth, accountFind, { kind: "elbow", fromSide: "right", toSide: "left", line: sideLine, tail: arrow });
slide.shapes.connect(auth, profile, { kind: "elbow", fromSide: "right", toSide: "left", line: sideLine, tail: arrow });
slide.shapes.connect(profile, activity, { kind: "straight", fromSide: "right", toSide: "left", line: sideLine, tail: arrow });

textBox("guide-core", "핵심 탐색 흐름", 510, 198, 160, 25, 14, "#5E785F", true);
textBox("guide-account", "회원 기능 보조 흐름", 60, 604, 695, 24, 14, "#6A7D6C", false, "left");

slide.speakerNotes.textFrame.setText(
  "[Sources]\n- Repository README.md: main page, search, region/category filtering, restaurant list/map, restaurant detail, directions, reviews/comments, favorites, and supporting content.\n- Repository docs/auth-guide.md: login/signup, account recovery, profile menu, My Page, and user activity.\n- Previous generated version supplied in this task: retained its information hierarchy and green styling while changing the central orientation to horizontal."
);

await writeBlob(PREVIEW, await deck.export({ slide, format: "png", scale: 2 }));
await fs.writeFile(LAYOUT, await (await slide.export({ format: "layout" })).text());
const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(OUT);
console.log(OUT);
