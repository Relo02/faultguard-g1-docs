// Click a Mermaid diagram to enlarge it; click again or press Escape to close it.
document.addEventListener("click", (event) => {
  const diagram = event.target.closest && event.target.closest(".mermaid");
  if (diagram) diagram.classList.toggle("fg-zoom");
});
document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  document.querySelectorAll(".mermaid.fg-zoom").forEach((d) => d.classList.remove("fg-zoom"));
});
