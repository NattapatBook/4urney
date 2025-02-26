export function markdownParse(markdownText) {
  const lines = markdownText.split("\n");
  const content = [];
  let currentBlock = null;
  let tableLines = [];
  let codeBlockLines = [];
  let inTable = false;
  let inCodeBlock = false;
  let orderListCounter = 1;
  let lastLineWasOrderList = false;

  for (let i = 0; i < lines.length; i++) {
    let originalLine = lines[i];
    let trimmedLine = originalLine.trim();

    if (trimmedLine.startsWith("```")) {
      if (inCodeBlock) {
        const codeContent = codeBlockLines.join("\n");
        content.push({
          type: `text`,
          content: [
            {
              type: `code`,
              msg: codeContent,
            },
          ],
        });
        codeBlockLines = [];
        inCodeBlock = false;
      } else {
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      codeBlockLines.push(originalLine);
      continue;
    }

    if (trimmedLine === "") {
      if (tableLines.length > 0) {
        const tableBlock = parseTableBlock(tableLines);
        if (tableBlock) {
          content.push(tableBlock);
        }
        tableLines = [];
      }
      if (currentBlock) {
        content.push(currentBlock);
        currentBlock = null;
      }
      inTable = false;
      if (lastLineWasOrderList) {
        orderListCounter = 1;
      }
      lastLineWasOrderList = false;
      continue;
    }

    if (trimmedLine.startsWith("|")) {
      tableLines.push(trimmedLine);
      inTable = true;
      continue;
    } else {
      if (tableLines.length > 0) {
        const tableBlock = parseTableBlock(tableLines);
        if (tableBlock) {
          content.push(tableBlock);
        }
        tableLines = [];
        inTable = false;
      }
    }

    if (!currentBlock) {
      currentBlock = { type: "text", content: [] };
    }

    const textElements = parseTextLine(
      originalLine,
      currentBlock,
      orderListCounter
    );
    currentBlock.content.push(...textElements);

    if (textElements.some((el) => el.type === "orderList")) {
      lastLineWasOrderList = true;
    } else {
      lastLineWasOrderList = false;
    }
  }

  if (tableLines.length > 0) {
    const tableBlock = parseTableBlock(tableLines);
    if (tableBlock) {
      content.push(tableBlock);
    }
  }

  if (currentBlock) {
    content.push(currentBlock);
  }

  return { content: content };
}

function parseTableBlock(tableLines) {
  if (tableLines.length === 0) return null;

  const rows = [];
  let headerRows = [];
  let bodyRows = [];
  let separatorIndex = -1;

  for (let i = 0; i < tableLines.length; i++) {
    const line = tableLines[i].trim();
    const isSeparator = isSeparatorLine(line, i);
    const cells = line
      .split("|")
      .filter((cell) => cell.trim() !== "")
      .map((cell) => cell.trim());

    if (isSeparator) {
      separatorIndex = i;
      continue;
    }

    const rowType =
      separatorIndex < i && separatorIndex !== -1 ? "row" : "header";

    if (rowType === "header") {
      headerRows.push({ type: "header", cells: cells });
    } else {
      bodyRows.push({ type: "row", cells: cells });
    }
  }

  if (headerRows.length === 0 && bodyRows.length === 0) return null;

  rows.push(...headerRows);
  rows.push(...bodyRows);

  return { type: "table", rows: rows };
}

function isSeparatorLine(line, lineIndex) {
  if (!line.startsWith("|")) return false;

  const cells = line.split("|");
  if (cells.length < 2) return false;

  let allCellsAreSeparator = true;

  for (let i = 1; i < cells.length - 1; i++) {
    let cellContent = cells[i].trim();
    cellContent = cellContent
      .replace(/\s/g, "")
      .replace(/[\u0000-\u001F\u007F-\u009F]/g, "");
    if (cellContent === "") continue;
    if (cellContent.split("").some((char) => char !== "-")) {
      allCellsAreSeparator = false;
      return false;
    }
  }
  return allCellsAreSeparator;
}

function removeSeparatorRowsFromTable(jsonOutput) {
  if (!jsonOutput || !jsonOutput.content) return jsonOutput;

  jsonOutput.content.forEach((block) => {
    if (block.type === "table" && block.rows) {
      const filteredRows = [];
      block.rows.forEach((row) => {
        if (row.type === "row") {
          let isSeparatorRow = true;
          if (row.cells) {
            for (const cell of row.cells) {
              const cellContent = cell.trim();
              if (!/^-*$/.test(cellContent)) {
                isSeparatorRow = false;
                break;
              }
            }
          }
          if (!isSeparatorRow) {
            filteredRows.push(row);
          }
        } else {
          filteredRows.push(row);
        }
      });
      block.rows = filteredRows;
    }
  });
  return jsonOutput;
}

function parseTextLine(originalLine, currentBlock, orderListCounter) {
  const elements = [];
  let listType = null;
  let listItemLevel = 0;

  const leadingSpacesMatch = originalLine.match(/^(\s*)/);
  const leadingSpaces = leadingSpacesMatch ? leadingSpacesMatch[1].length : 0;

  const orderListRegex = /^(\d+)\.\s+/;

  if (originalLine.trim().startsWith("- ")) {
    listType = "list";
    listItemLevel = Math.floor(leadingSpaces / 2) + 1;
    elements.push({ type: "list", msg: "•", level: listItemLevel });
    originalLine = originalLine.replace(/^(\s*)- /, "");
  } else if (orderListRegex.test(originalLine.trim())) {
    listType = "orderList";
    listItemLevel = Math.floor(leadingSpaces / 2) + 1;
    const match = originalLine.match(orderListRegex);
    const orderNumber = match[1];
    elements.push({
      type: "orderList",
      msg: `${orderNumber}.`,
      level: listItemLevel,
    });
    originalLine = originalLine.replace(/^(\s*)\d+\.\s/, "");
  }

  let parts = originalLine.split(
    /(\*\*.*?\*\*|\_\_.*?\_\_|\*.*?\*|\_.*?\_|\`\`|\`|\[.*?\]\(.*?\))/g
  );
  for (const part of parts) {
    if (part) {
      if (part.startsWith("**") && part.endsWith("**")) {
        elements.push({ type: "bold_text", msg: part.slice(2, -2) });
      } else if (part.startsWith("*") && part.endsWith("*")) {
        elements.push({ type: "italic_text", msg: part.slice(1, -1) });
      } else if (
        part.startsWith("[") &&
        part.includes("](") &&
        part.endsWith(")")
      ) {
        const linkMatch = part.match(/\[(.*?)\]\((.*?)\)/);
        if (linkMatch) {
          elements.push({ type: "link", msg: linkMatch[1], url: linkMatch[2] });
        }
      } else {
        elements.push({ type: "text", msg: part });
      }
    }
  }

  return elements;
}
// Golden rule เลยนะ อย่าแก้! เขียนแล้วพรุ่งนี้ก็ลืมแล้วจำไม่ได้
// A.Luanjai Jr.

// format Example :
//   content: [
//     {
//       type: "text",
//       content: [
//         { type: "orderList", msg: "1." },
//         { type: "bold", msg: `ตางรางเข้าพบหมอ` },
//       ],
//     },
//     {
//       type: "table",
//       rows: [
//         {
//           type: "header",
//           cells: ["แผนก", "แพทย์", "วันและเวลา"],
//         },
//         {
//           type: "row",
//           cells: ["กุมารเวช", "พญ.ณัฐวดี สุขเกษม", "เสาร์ 08:00 - 12:00"],
//         },
//         {
//           type: "row",
//           cells: [
//             "จิตเวช",
//             "พญ.ดารารัตน์ สุขศรี",
//             "พุธ, เสาร์ 13:00 - 17:00",
//           ],
//         },
//         {
//           type: "row",
//           cells: [
//             "โรคหัวใจ",
//             "นพ.เกียรติศักดิ์ เรืองไกร",
//             "พุธ, เสาร์ 09:00 - 14:00",
//           ],
//         },
//       ],
//     },
//     {
//       type: "text",
//       content: [
//         {
//           type: "orderList",
//           msg: "2.",
//         },
//         { type: "bold", msg: `เวลาทำการของแผนกต่างๆ` },
//       ],
//     },
//     {
//       type: "table",
//       rows: [
//         {
//           type: "header",
//           cells: ["แผนก", "เวลาทำการ", "วันหยุด", "หมายเหตุ"],
//         },
//         {
//           type: "row",
//           cells: [
//             "อายุรกรรม (Internal Medicine)",
//             "จันทร์ - ศุกร์, 08:00 - 17:00",
//             "เสาร์-อาทิตย์",
//             "ปิดวันหยุดนักขัตฤกษ์",
//           ],
//         },
//         {
//           type: "row",
//           cells: [
//             "ศัลยกรรมกระดูก (Orthopedic Surgery)",
//             "อังคาร, พฤหัสบดี, เสาร์ 09:00 - 16:00",
//             "เปิดวันเสาร์เฉพาะ OPD",
//           ],
//         },
//         {
//           type: "row",
//           cells: [
//             "กุมารเวช (Pediatrics)",
//             "เสาร์ 08:00 - 12:00",
//             "เปิดเฉพาะวัคซีนเด็ก",
//           ],
//         },
//         {
//           type: "row",
//           cells: [
//             "โรคหัวใจ (Cardiology)",
//             "จันทร์ - เสาร์ 09:00 - 16:00",
//             "ต้องจองล่วงหน้า",
//           ],
//         },
//         {
//           type: "row",
//           cells: [
//             "ผิวหนัง (Dermatology)",
//             "ทุกวัน 10:00 - 20:00",
//             "เปิดรับ Walk-in",
//           ],
//         },
//       ],
//     },
//     {
//       type: "text",
//       content: [
//         {
//           type: "paragraph",
//           msg: "ข้อความย่อหน้า",
//         },
//         { type: "list", msg: "-" , level:1 },
//         {
//           type: "bold",
//           msg: "ข้อความตัวหนา",
//         },
//         {
//           type: "italic",
//           msg: "ข้อความตัวเอียง",
//         },
//       ],
//     },
//     {
//       type: "text",
//       content: [
//         {
//           type: "link",
//           msg: "คลิกที่นี่เพื่อไปเว็บไซต์",
//           url: "https://www.example.com",
//         },
//       ],
//     },
//   ],
