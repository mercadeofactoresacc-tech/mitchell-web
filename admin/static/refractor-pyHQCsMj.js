import { ao as distExports, ap as Refractor, j as jsxRuntimeExports } from "./sanity-DwlRLi-0.js";
function LazyRefractor(props) {
  const $ = distExports.c(13), {
    language: languageProp,
    value
  } = props, language = typeof languageProp == "string" ? languageProp : void 0;
  let t0;
  $[0] !== language ? (t0 = language ? Refractor.hasLanguage(language) : false, $[0] = language, $[1] = t0) : t0 = $[1];
  const registered = t0;
  let t1;
  $[2] !== language || $[3] !== registered || $[4] !== value ? (t1 = !(language && registered) && /* @__PURE__ */ jsxRuntimeExports.jsx("code", { children: value }), $[2] = language, $[3] = registered, $[4] = value, $[5] = t1) : t1 = $[5];
  let t2;
  $[6] !== language || $[7] !== registered || $[8] !== value ? (t2 = language && registered && /* @__PURE__ */ jsxRuntimeExports.jsx(Refractor, { inline: true, language, value: String(value) }), $[6] = language, $[7] = registered, $[8] = value, $[9] = t2) : t2 = $[9];
  let t3;
  return $[10] !== t1 || $[11] !== t2 ? (t3 = /* @__PURE__ */ jsxRuntimeExports.jsxs(jsxRuntimeExports.Fragment, { children: [
    t1,
    t2
  ] }), $[10] = t1, $[11] = t2, $[12] = t3) : t3 = $[12], t3;
}
LazyRefractor.displayName = "LazyRefractor";
export {
  LazyRefractor as default
};
