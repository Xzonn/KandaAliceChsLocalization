#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import csv
import json
import os

os.chdir(os.path.dirname(os.path.dirname(__file__)))

DIR_ORIGINAL = "master/texts"

languages = os.listdir(DIR_ORIGINAL)

def get_sheet(language: str, sheet_name: str) -> dict[str, str]:
  csvfile = open(f"{language}/{sheet_name}.csv", "r", encoding="utf-8-sig", newline="")
  reader = csv.reader(csvfile)

  row_iter = reader
  next(row_iter)
  msgidx: list[str] = []
  chinese: list[str] = []
  for row in row_iter:
    msgidx.append(str(int(row[3].split(":")[-1])))
    chinese.append(row[2] or "")

  return dict(zip(msgidx, chinese))

for language in languages:
  if language in ["ja", "en"]:
    continue

  files = os.listdir(f"{DIR_ORIGINAL}/{language}")
  for file_name in files:
    if not file_name.endswith(".json"):
      continue

    with open(f"{DIR_ORIGINAL}/ja/{file_name}", "r", -1, "utf-8") as reader:
      original_messages = json.load(reader)
    if len(original_messages) < 1:
      continue

    translated_messages = [_ for _ in original_messages]

    sheet_name = file_name.removesuffix(".json")
    chinese = get_sheet(language, sheet_name)

    for i, line in enumerate(original_messages):
      msgidx = str(i + 1)
      if not msgidx in chinese:
        continue
      new_line = chinese[msgidx]
      translated_messages[i] = new_line

    writer = open(f"{DIR_ORIGINAL}/{language}/{file_name}", "w", -1, "utf-8")
    json.dump(translated_messages, writer, indent=2, ensure_ascii=False)
    writer.close()