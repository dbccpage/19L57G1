// AuthorityEffect: None. A finite supplied answer table, not a physical observer.
export function createQuestionModel(ids, questions) {
  if (!Array.isArray(ids) || ids.some(id => typeof id !== "string" || !id) || new Set(ids).size !== ids.length) {
    throw new TypeError("Card identifiers must be distinct nonempty strings.");
  }
  if (!Array.isArray(questions) || new Set(questions.map(q => q.id)).size !== questions.length) {
    throw new TypeError("Question identifiers must be distinct.");
  }
  const rows = new Map();
  for (const q of questions) {
    if (typeof q.id !== "string" || !q.id || !Array.isArray(q.answers) ||
        q.answers.length !== ids.length || q.answers.some(answer => typeof answer !== "boolean")) {
      throw new TypeError("Every question needs one explicit boolean answer per card.");
    }
    rows.set(q.id, Object.freeze([...q.answers]));
  }
  const cardIds = Object.freeze([...ids]);
  const index = new Map(cardIds.map((id, i) => [id, i]));
  function answer(card, question) {
    if (!index.has(card)) throw new RangeError(`Unknown card: ${card}`);
    if (!rows.has(question)) throw new RangeError(`Unknown question: ${question}`);
    return rows.get(question)[index.get(card)];
  }
  function signature(card, selected) {
    if (!index.has(card)) throw new RangeError(`Unknown card: ${card}`);
    for (const question of selected) {
      if (!rows.has(question)) throw new RangeError(`Unknown question: ${question}`);
    }
    return selected.map(question => answer(card, question));
  }
  function groups(selected) {
    // Validate the question list even when the supplied carrier is empty.
    for (const question of selected) {
      if (!rows.has(question)) throw new RangeError(`Unknown question: ${question}`);
    }
    const grouped = new Map();
    for (const id of cardIds) {
      const key = JSON.stringify(signature(id, selected));
      if (!grouped.has(key)) grouped.set(key, []);
      grouped.get(key).push(id);
    }
    return [...grouped.values()];
  }
  function separation(left, right, selected) {
    const l = signature(left, selected), r = signature(right, selected);
    const position = l.findIndex((value, i) => value !== r[i]);
    return position < 0
      ? { separated: false, witness: null, answers: null }
      : { separated: true, witness: selected[position], answers: [l[position], r[position]] };
  }
  function recovery(selected, target) {
    if (!rows.has(target)) throw new RangeError(`Unknown question: ${target}`);
    const grouped = groups(selected);
    for (const group of grouped) {
      for (const id of group.slice(1)) {
        if (answer(group[0], target) !== answer(id, target)) {
          return { possible: false, blocker: [group[0], id], table: [] };
        }
      }
    }
    return { possible: true, blocker: null,
      table: grouped.map(group => ({ pattern: signature(group[0], selected), answer: answer(group[0], target) })) };
  }
  return Object.freeze({ ids: cardIds, answer, signature, groups, separation, recovery });
}
