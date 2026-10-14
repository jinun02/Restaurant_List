import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/봄내로그_프로젝트_흐름도_상세수정본.pptx";
const PREVIEW = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/detailed-preview.png";
const LAYOUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/detailed-layout.json";

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

const title = slide.shapes.add({
  geometry: "textbox",
  name: "slide-title",
  position: { left: 72, top: 42, width: 1136, height: 50 },
  fill: "none",
  line: { style: "solid", fill: "none", width: 0 },
});
title.text = "봄내로그 페이지 구성과 사용자 흐름";
title.text.style = { fontFamily: "Malgun Gothic", fontSize: 32, bold: true, color: "#17351B", alignment: "center" };

const subtitle = slide.shapes.add({
  geometry: "textbox",
  name: "slide-subtitle",
  position: { left: 280, top: 91, width: 720, height: 30 },
  fill: "none",
  line: { style: "solid", fill: "none", width: 0 },
});
subtitle.text = "메인 화면에서 탐색·상세·회원 기능으로 이어지는 주요 경로";
subtitle.text.style = { fontFamily: "Malgun Gothic", fontSize: 16, color: "#5D755F", alignment: "center" };

function node(name, label, x, y, w, h, kind = "action", fontSize = 17) {
  const colors = {
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
    fill: colors[0],
    line: { style: "solid", fill: colors[1], width: kind === "main" || kind === "core" ? 2.4 : 1.8 },
    borderRadius: "rounded-xl",
    shadow: kind === "main" || kind === "core" ? "shadow-sm" : undefined,
  });
  shape.text = label;
  shape.text.style = {
    fontFamily: "Malgun Gothic",
    fontSize,
    bold: true,
    color: colors[2],
    alignment: "center",
    verticalAlignment: "middle",
  };
  return shape;
}

const home = node("home", "메인 화면", 535, 132, 210, 62, "main", 20);
const content = node("content", "서비스 소개\n소식 · 공지", 80, 132, 180, 62, "side", 16);

const search = node("header-search", "헤더 통합 검색", 290, 238, 190, 58, "action", 17);
const region = node("region-select", "지역 선택", 545, 238, 190, 58, "action", 17);
const auth = node("auth", "로그인 · 회원가입", 925, 238, 210, 58, "side", 17);

const filters = node("filters", "동네 · 업종 필터", 545, 330, 190, 58, "core", 17);
const accountFind = node("account-find", "아이디 · 비밀번호 찾기", 840, 340, 200, 54, "feature", 15);
const profile = node("profile", "프로필 · 마이페이지", 1050, 340, 170, 54, "feature", 15);

const explorer = node("explorer", "식당 목록 · 지도 · 마커", 515, 422, 250, 60, "action", 17);
const detail = node("detail", "식당 상세 정보", 535, 514, 210, 60, "core", 18);

const directions = node("directions", "길찾기", 320, 625, 170, 46, "feature", 16);
const reviews = node("reviews", "리뷰 · 댓글", 555, 625, 170, 46, "feature", 16);
const favorites = node("favorites", "즐겨찾기", 790, 625, 170, 46, "feature", 16);

const arrow = { type: "arrow", width: "med", length: "med" };
const coreLine = { style: "solid", fill: "#57785B", width: 2.4 };
const sideLine = { style: "solid", fill: "#9BB29D", width: 1.9 };

slide.shapes.connect(home, content, { kind: "straight", fromSide: "left", toSide: "right", line: sideLine, tail: arrow });
slide.shapes.connect(home, search, { kind: "elbow", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });
slide.shapes.connect(home, region, { kind: "straight", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });
slide.shapes.connect(home, auth, { kind: "elbow", fromSide: "right", toSide: "top", line: sideLine, tail: arrow });

slide.shapes.connect(search, filters, { kind: "elbow", fromSide: "bottom", toSide: "left", line: coreLine, tail: arrow });
slide.shapes.connect(region, filters, { kind: "straight", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });
slide.shapes.connect(auth, accountFind, { kind: "elbow", fromSide: "bottom", toSide: "top", line: sideLine, tail: arrow });
slide.shapes.connect(auth, profile, { kind: "elbow", fromSide: "bottom", toSide: "top", line: sideLine, tail: arrow });

slide.shapes.connect(filters, explorer, { kind: "straight", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });
slide.shapes.connect(explorer, detail, { kind: "straight", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });

slide.shapes.connect(detail, directions, { kind: "elbow", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });
slide.shapes.connect(detail, reviews, { kind: "straight", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });
slide.shapes.connect(detail, favorites, { kind: "elbow", fromSide: "bottom", toSide: "top", line: coreLine, tail: arrow });

slide.speakerNotes.textFrame.setText(
  "[Sources]\n- Repository README.md: main, search, region/category filtering, restaurant list/map, detail, directions, reviews/comments, favorites, and page routing.\n- Repository docs/auth-guide.md: login/signup, account recovery, profile menu, and My Page flow.\n- User-provided images: preferred diagram density and the green rounded-box visual direction."
);

await writeBlob(PREVIEW, await deck.export({ slide, format: "png", scale: 2 }));
await fs.writeFile(LAYOUT, await (await slide.export({ format: "layout" })).text());
const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(OUT);
console.log(OUT);
