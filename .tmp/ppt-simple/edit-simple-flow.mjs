import fs from "node:fs/promises";
import { FileBlob, PresentationFile } from "@oai/artifact-tool";

const source = "C:/Users/PC/Documents/GitHub/Restaurant_List/봄내로그_프로젝트_흐름도_가로형.pptx";
const output = "C:/Users/PC/Documents/GitHub/Restaurant_List/봄내로그_프로젝트_흐름도_간결본.pptx";
const outDir = "C:/Users/PC/Documents/GitHub/Restaurant_List/.tmp/ppt-simple/final-render";

await fs.mkdir(outDir, { recursive: true });
const presentation = await PresentationFile.importPptx(await FileBlob.load(source));
const replacements = new Map([
  ["주요 탐색 경로를 왼쪽에서 오른쪽으로 표현", "핵심 화면 이동과 회원 기능을 한눈에 정리"],
  ["동네 · 업종 필터", "지역 · 업종 선택"],
  ["식당 목록\n지도 · 마커", "맛집 목록\n지도 확인"],
  ["아이디 · 비밀번호 찾기", "계정 찾기"],
  ["프로필 · 마이페이지", "마이페이지"],
  ["즐겨찾기 · 내 활동", "즐겨찾기 · 활동"],
]);

const snapshot = await presentation.inspect({ kind: "slide,textbox,shape,notes", maxChars: 20000 });
for (const line of snapshot.ndjson.split(/\r?\n/)) {
  if (!line.trim()) continue;
  const item = JSON.parse(line);
  if (!item.id || !item.text || !replacements.has(item.text)) continue;
  presentation.resolve(item.id).text = replacements.get(item.text);
}

const slide = presentation.slides.getItem(0);
const png = await presentation.export({ slide, format: "png", scale: 1.5 });
await fs.writeFile(`${outDir}/slide-1.png`, new Uint8Array(await png.arrayBuffer()));
const layout = await slide.export({ format: "layout" });
await fs.writeFile(`${outDir}/slide-1.layout.json`, await layout.text());
const finalSnapshot = await presentation.inspect({ kind: "slide,textbox,shape,notes,layout", maxChars: 20000 });
await fs.writeFile(`${outDir}/final-inspect.ndjson`, finalSnapshot.ndjson);
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(output);
