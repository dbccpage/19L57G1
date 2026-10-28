// AuthorityEffect: None. Finite executable checks; no reader-learning claim.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createQuestionModel } from "./model.mjs";

const data = JSON.parse(readFileSync(new URL("./cards.json", import.meta.url)));
const ids = data.cards.map(card => card.id);
const model = createQuestionModel(ids, data.questions);

test("blank, one-question, and joint groups retain the declared card positions", () => {
  assert.deepEqual(model.groups([]), [["A", "B", "C"]]);
  assert.deepEqual(model.groups(["blue"]), [["A", "B"], ["C"]]);
  assert.deepEqual(model.groups(["triangle"]), [["A"], ["B", "C"]]);
  assert.deepEqual(model.groups(["blue", "triangle"]), [["A"], ["B"], ["C"]]);
});

test("a distinguishing question supplies both answers as its witness", () => {
  assert.deepEqual(model.separation("A", "B", ["blue"]), { separated: false, witness: null, answers: null });
  assert.deepEqual(model.separation("A", "B", ["blue", "triangle"]),
    { separated: true, witness: "triangle", answers: [false, true] });
});

test("replacement can lose a distinction while addition retains it", () => {
  assert.equal(model.separation("B", "C", ["blue"]).separated, true);
  assert.equal(model.separation("B", "C", ["blue", "triangle"]).separated, true);
  assert.equal(model.separation("B", "C", ["triangle"]).separated, false);
});

test("recovery either supplies a complete lookup or the actual conflicting pair", () => {
  assert.deepEqual(model.recovery(["blue"], "triangle").blocker, ["A", "B"]);
  assert.deepEqual(model.recovery(["triangle"], "blue").blocker, ["B", "C"]);
  assert.equal(model.recovery(["blue", "triangle"], "triangle").possible, true);
  assert.deepEqual(model.recovery([], "listed").table, [{ pattern: [], answer: true }]);
});

test("renaming a display label has no input to the model and source mutations are isolated", () => {
  const mutable = [{ id: "q", answers: [true, false] }];
  const isolated = createQuestionModel(["left", "right"], mutable);
  mutable[0].answers[0] = false;
  assert.equal(isolated.separation("left", "right", ["q"]).separated, true);
});

test("malformed tables and unknown references are refused rather than filled in", () => {
  assert.throws(() => createQuestionModel(["A", "A"], []));
  assert.throws(() => createQuestionModel(ids, [{ id: "q", answers: [true] }]));
  assert.throws(() => createQuestionModel(ids, [{ id: "q", answers: [true, 0, false] }]));
  assert.throws(() => model.signature("unknown", []));
  assert.throws(() => model.groups(["unknown"]));
  assert.throws(() => model.recovery([], "unknown"));
});

test("all 64 two-question tables: recovery matches independent enumeration of lookup functions", () => {
  for (let bits = 0; bits < 64; bits++) {
    const qs = [0, 1].map(k => ({ id: `q${k}`, answers: ids.map((_, i) => !!(bits & (1 << (k * 3 + i)))) }));
    const m = createQuestionModel(ids, qs);
    for (const selected of [[], ["q0"], ["q1"], ["q0", "q1"]]) {
      const patterns = ids.map(id => JSON.stringify(m.signature(id, selected)));
      const distinct = [...new Set(patterns)];
      for (const target of ["q0", "q1"]) {
        let found = false;
        for (let assignment = 0; assignment < 2 ** distinct.length; assignment++) {
          if (ids.every((id, i) => !!(assignment & (1 << distinct.indexOf(patterns[i]))) === m.answer(id, target))) found = true;
        }
        assert.equal(m.recovery(selected, target).possible, found);
      }
      for (const l of ids) for (const r of ids) {
        if (m.separation(l, r, selected).separated) {
          assert.equal(m.separation(l, r, [...selected, "q0", "q1"]).separated, true);
        }
      }
    }
  }
});
