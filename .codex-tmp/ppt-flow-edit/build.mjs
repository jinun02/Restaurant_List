import fs from "node:fs/promises";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const OUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/봄내로그_프로젝트_흐름도_수정본.pptx";
const PREVIEW = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/preview.png";
const LAYOUT = "C:/Users/PC/Documents/GitHub/Restaurant_List/.codex-tmp/ppt-flow-edit/layout.json";

async function writeBlob(path, blob) {
  await fs.writeFile(path, new Uint8Array(await blob.arrayBuffer()));
}

const deck = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const slide = deck.slides.add();
slide.background.fill = "#F7FAF4";

// Reference-inspired green frame, simplified for a cleaner presentation canvas.
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
  position: { left: 72, top: 48, width: 1136, height: 54 },
  fill: "none",
  line: { style: "solid", fill: "none", width: 0 },
});
title.text = "봄내로그 사용자 흐름";
title.text.style = { fontFamily: "Malgun Gothic", fontSize: 34, bold: true, color: "#17351B", alignment: "center" };

const subtitle = slide.shapes.add({
  geometry: "textbox",
  name: "slide-subtitle",
  position: { left: 300, top: 100, width: 680, height: 34 },
  fill: "none",
  line: { style: "solid", fill: "none", width: 0 },
});
subtitle.text = "탐색은 상세 정보로 이어지고, 사용자 기능은 필요한 순간에 연결됩니다";
subtitle.text.style = { fontFamily: "Malgun Gothic", fontSize: 17, color: "#56705A", alignment: "center" };

function node(name, label, x, y, w, h, kind = "main") {
  const palette = {
    main: { fill: "#E2F8C7", line: "#77B93D", color: "#17351B" },
    action: { fill: "#FFFFFF", line: "#9BCB72", color: "#17351B" },
    result: { fill: "#D6F2B7", line: "#5FA331", color: "#17351B" },
    side: { fill: "#F0F8E7", line: "#B2CF99", color: "#34503A" },
  }[kind];
  const shape = slide.shapes.add({
    geometry: "roundRect",
    name,
    position: { left: x, top: y, width: w, height: h },
    fill: palette.fill,
    line: { style: "solid", fill: palette.line, width: kind === "main" ? 2.5 : 2 },
    borderRadius: "rounded-xl",
    shadow: kind === "side" ? undefined : "shadow-sm",
  });
  shape.text = label;
  shape.text.style = {
    fontFamily: "Malgun Gothic",
    fontSize: kind === "side" ? 17 : 20,
    bold: true,
    color: palette.color,
    alignment: "center",
    verticalAlignment: "middle",
  };
  return shape;
}

// Create nodes first to obtain anchors; connectors are immediately sent behind them by the API.
const home = node("home", "메인 화면", 535, 150, 210, 70, "main");
const search = node("search-region", "검색 · 지역 선택", 285, 278, 210, 66, "action");
const explore = node("restaurant-explorer", "맛집 탐색", 535, 278, 210, 66, "result");
const account = node("account", "로그인 · 회원가입", 880, 278, 210, 66, "side");
const listMap = node("list-map", "식당 목록 · 지도", 535, 402, 210, 66, "action");
const info = node("service-info", "서비스 소개\n소식 · 공지", 135, 152, 180, 66, "side");
const myPage = node("mypage", "마이페이지", 990, 420, 190, 76, "side");
const detail = node("restaurant-detail", "식당 상세 정보", 535, 526, 210, 66, "result");
const activities = node("detail-actions", "길찾기 · 리뷰 · 즐겨찾기", 465, 626, 350, 48, "main");

const arrow = { type: "arrow", width: "med", length: "med" };
const primaryLine = { style: "solid", fill: "#5A7B5E", width: 2.5 };
const sideLine = { style: "solid", fill: "#9AB29C", width: 2 };

slide.shapes.connect(home, search, { kind: "elbow", fromSide: "bottom", toSide: "top", line: primaryLine, tail: arrow });
slide.shapes.connect(home, explore, { kind: "straight", fromSide: "bottom", toSide: "top", line: primaryLine, tail: arrow });
slide.shapes.connect(home, account, { kind: "elbow", fromSide: "bottom", toSide: "top", line: sideLine, tail: arrow });
slide.shapes.connect(home, info, { kind: "straight", fromSide: "left", toSide: "right", line: sideLine, tail: arrow });
slide.shapes.connect(search, explore, { kind: "straight", fromSide: "right", toSide: "left", line: primaryLine, tail: arrow });
slide.shapes.connect(explore, listMap, { kind: "straight", fromSide: "bottom", toSide: "top", line: primaryLine, tail: arrow });
slide.shapes.connect(listMap, detail, { kind: "straight", fromSide: "bottom", toSide: "top", line: primaryLine, tail: arrow });
slide.shapes.connect(detail, activities, { kind: "straight", fromSide: "bottom", toSide: "top", line: primaryLine, tail: arrow });
slide.shapes.connect(account, myPage, { kind: "elbow", fromSide: "bottom", toSide: "top", line: sideLine, tail: arrow });
slide.shapes.connect(myPage, detail, { kind: "elbow", fromSide: "left", toSide: "right", line: sideLine, tail: arrow });

slide.speakerNotes.textFrame.setText(
  "[Sources]\n- Repository README.md: page structure, restaurant exploration, map, detail, search, favorites, and routing flow.\n- Repository docs/auth-guide.md: authentication cookie, profile menu, and My Page linkage.\n- User-provided screenshot: green border, rounded node styling, and overall visual direction."
);

await writeBlob(PREVIEW, await deck.export({ slide, format: "png", scale: 2 }));
await fs.writeFile(LAYOUT, await (await slide.export({ format: "layout" })).text());
const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(OUT);

console.log(OUT);
