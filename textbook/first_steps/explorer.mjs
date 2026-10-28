// AuthorityEffect: None. Display names never enter the answer model.
import { createQuestionModel } from "./model.mjs";

const byId = id => document.getElementById(id);
const yesNo = answer => answer ? "Yes" : "No";

try {
  const response = await fetch(new URL("./cards.json", import.meta.url));
  if (!response.ok) throw new Error("The supplied card table could not be loaded.");
  const data = await response.json();
  const model = createQuestionModel(data.cards.map(card => card.id), data.questions);
  const names = new Map(model.ids.map(id => [id, id]));
  const title = id => data.questions.find(q => q.id === id).title;
  const selected = () => ["blue", "triangle"].filter(id => byId(id).checked);
  let observed = null;

  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  function renderCards() {
    byId("cards").replaceChildren();
    for (const card of data.cards) {
      const article = element("article", undefined, "card");
      article.append(element("h3", names.get(card.id), "card-label"), element("p", `Position ${card.id}`, "card-position"));
      const area = element("div", undefined, "shape-area");
      const shape = element("div", undefined, `shape ${card.color} ${card.shape}`);
      shape.setAttribute("aria-hidden", "true"); area.append(shape);
      article.append(area, element("p", `${card.color} ${card.shape}`, "card-description"));
      byId("cards").append(article);
    }
    for (const option of byId("rename-card").options) option.textContent = names.get(option.value);
    for (const option of byId("pair").options) {
      const [left, right] = option.value.split(",");
      option.textContent = `${names.get(left)} and ${names.get(right)}`;
    }
  }
  function clearRecovery() {
    byId("recovery-result").replaceChildren(element("p", observed ? "Choose a requested answer, then check recovery." : "Run the selected questions before checking recovery.", "hint"));
    byId("recovery-result").className = "";
  }
  function clearObservation(message) {
    observed = null;
    byId("results").hidden = true; byId("empty-output").hidden = false;
    byId("run-notice").textContent = message;
    byId("prediction").value = "";
    clearRecovery();
  }
  function renderResults() {
    const table = byId("answer-table"); table.replaceChildren();
    const head = element("thead"), headRow = element("tr");
    for (const text of ["Card", ...observed.map(title), "Pattern"]) {
      const th = element("th", text); th.scope = "col"; headRow.append(th);
    }
    head.append(headRow); table.append(head);
    const body = element("tbody");
    for (const id of model.ids) {
      const row = element("tr");
      const name = element("th", names.get(id)); name.scope = "row"; row.append(name);
      for (const question of observed) row.append(element("td", yesNo(model.answer(id, question))));
      const pattern = model.signature(id, observed).map(yesNo).join(", ") || "No answers recorded";
      row.append(element("td", pattern)); body.append(row);
    }
    table.append(body);
    byId("groups").replaceChildren(...model.groups(observed).map(group => element("span", group.map(id => names.get(id)).join(" + "), "group")));
    const [left, right] = byId("pair").value.split(",");
    const result = model.separation(left, right, observed);
    const correct = (byId("prediction").value === "different") === result.separated;
    const heading = element("strong", correct ? "Your prediction matches the table." : "The table gives a different result. Try explaining why.");
    let explanation;
    if (result.separated) {
      explanation = `${title(result.witness)} witnesses the separation: ${names.get(left)} gives ${yesNo(result.answers[0])}; ${names.get(right)} gives ${yesNo(result.answers[1])}.`;
    } else {
      explanation = observed.length ? `${names.get(left)} and ${names.get(right)} agree on every selected question. They share a pattern for this question list.` : "With no selected questions, the machine has no recorded test that separates this pair.";
    }
    byId("verdict").replaceChildren(heading, element("p", explanation));
    byId("scope").textContent = "These groups describe the selected answers. The three admitted card positions remain separate entries in the supplied list.";
    byId("results").hidden = false; byId("empty-output").hidden = true;
  }
  byId("run").addEventListener("click", () => {
    if (!byId("prediction").value) {
      byId("run-notice").textContent = "Choose a prediction first. Being wrong is useful: it tells you what to inspect.";
      byId("prediction").focus(); return;
    }
    observed = selected(); renderResults(); clearRecovery();
    byId("run-notice").textContent = "Now explain the result using the actual answers.";
  });
  for (const id of ["blue", "triangle", "pair"]) byId(id).addEventListener("change", () => clearObservation("The question list or pair changed. Make a fresh prediction."));
  byId("prediction").addEventListener("change", () => {
    if (observed !== null) {
      observed = null; byId("results").hidden = true; byId("empty-output").hidden = false; clearRecovery();
    }
  });
  byId("rename-form").addEventListener("submit", event => {
    event.preventDefault();
    const next = byId("new-name").value.trim();
    if (!next) return;
    const id = byId("rename-card").value;
    if ([...names.entries()].some(([other, name]) => other !== id && name === next)) {
      byId("rename-notice").textContent = "Choose a distinct display name so the cards remain easy to refer to."; return;
    }
    names.set(id, next); renderCards();
    if (observed !== null) renderResults();
    clearRecovery();
    byId("new-name").value = "";
    byId("rename-notice").textContent = `Position ${id} is now displayed as ${next}. The answer table and selected questions are unchanged.`;
  });
  byId("target").addEventListener("change", clearRecovery);
  byId("recover").addEventListener("click", () => {
    if (observed === null) {
      byId("recovery-result").replaceChildren(element("p", "Make a prediction and run the selected questions first.", "hint")); return;
    }
    const target = byId("target").value, result = model.recovery(observed, target);
    const panel = byId("recovery-result"); panel.className = "recovery-result";
    if (!result.possible) {
      const [left, right] = result.blocker;
      panel.replaceChildren(element("strong", "This answer cannot always be recovered from the recorded pattern."),
        element("p", `${names.get(left)} and ${names.get(right)} share a recorded pattern, but ${title(target)} answers ${yesNo(model.answer(left, target))} and ${yesNo(model.answer(right, target))}. That pair blocks recovery.`));
    } else {
      panel.replaceChildren(element("strong", "One lookup rule works for every card in this supplied list."));
      const list = element("ul");
      for (const row of result.table) list.append(element("li", `${row.pattern.map(yesNo).join(", ") || "No answers recorded"} → ${yesNo(row.answer)}`));
      panel.append(list, element("p", "The rule recovers the supplied target answer. It does not establish that a measurement of a physical object would give that answer.", "hint"));
    }
  });
  byId("reset").addEventListener("click", () => {
    for (const id of model.ids) names.set(id, id);
    byId("blue").checked = true; byId("triangle").checked = false;
    byId("pair").value = "A,B"; byId("target").value = "triangle";
    byId("new-name").value = ""; byId("rename-card").value = "A";
    byId("rename-notice").textContent = "The machine has no question about these display names.";
    renderCards(); clearObservation("Make your prediction before running the machine.");
  });
  renderCards(); clearRecovery();
} catch (error) {
  const notice = document.createElement("p"); notice.className = "error";
  notice.textContent = "The explorer could not load its supplied table. Open it through the documented local server, or read the complete lessons without the explorer.";
  byId("cards").replaceChildren(notice);
  for (const id of ["run", "recover", "reset"]) byId(id).disabled = true;
}
