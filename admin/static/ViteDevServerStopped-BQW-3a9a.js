import { d as distExports, j as jsxRuntimeExports, C as Card, b as Container, S as Stack, T as Text, r as reactExports, H as Heading } from "./sanity-DqWFaXvw.js";
const ERROR_TITLE = "Dev server stopped", ERROR_DESCRIPTION = "The development server has stopped. You may need to restart it to continue working.";
class ViteDevServerStoppedError extends Error {
  constructor() {
    super(ERROR_TITLE), this.name = "ViteDevServerStoppedError", this.ViteDevServerStoppedError = true;
  }
}
const isViteServer = (hot) => false, useDetectViteDevServerStopped = () => {
  const $ = distExports.c(5), [devServerStopped, setDevServerStopped] = reactExports.useState(false);
  let t0;
  $[0] === Symbol.for("react.memo_cache_sentinel") ? (t0 = () => setDevServerStopped(true), $[0] = t0) : t0 = $[0];
  const markDevServerStopped = t0;
  let t1, t2;
  $[1] === Symbol.for("react.memo_cache_sentinel") ? (t1 = () => {
  }, t2 = [markDevServerStopped], $[1] = t1, $[2] = t2) : (t1 = $[1], t2 = $[2]), reactExports.useEffect(t1, t2);
  let t3;
  return $[3] !== devServerStopped ? (t3 = {
    devServerStopped
  }, $[3] = devServerStopped, $[4] = t3) : t3 = $[4], t3;
}, ThrowViteServerStopped = () => {
  const {
    devServerStopped
  } = useDetectViteDevServerStopped();
  if (devServerStopped)
    throw new ViteDevServerStoppedError();
  return null;
}, DetectViteDevServerStopped = () => {
  const $ = distExports.c(1);
  let t0;
  return $[0] === Symbol.for("react.memo_cache_sentinel") ? (t0 = isViteServer() ? /* @__PURE__ */ jsxRuntimeExports.jsx(ThrowViteServerStopped, {}) : null, $[0] = t0) : t0 = $[0], t0;
}, DevServerStoppedErrorScreen = () => {
  const $ = distExports.c(3);
  let t0;
  $[0] === Symbol.for("react.memo_cache_sentinel") ? (t0 = [4, 5, 6, 7], $[0] = t0) : t0 = $[0];
  let t1;
  $[1] === Symbol.for("react.memo_cache_sentinel") ? (t1 = /* @__PURE__ */ jsxRuntimeExports.jsx(Heading, { children: ERROR_TITLE }), $[1] = t1) : t1 = $[1];
  let t2;
  return $[2] === Symbol.for("react.memo_cache_sentinel") ? (t2 = /* @__PURE__ */ jsxRuntimeExports.jsx(Card, { height: "fill", overflow: "auto", paddingY: t0, paddingX: 4, sizing: "border", tone: "critical", children: /* @__PURE__ */ jsxRuntimeExports.jsx(Container, { width: 3, children: /* @__PURE__ */ jsxRuntimeExports.jsxs(Stack, { space: 4, children: [
    t1,
    /* @__PURE__ */ jsxRuntimeExports.jsx(Card, { border: true, radius: 2, overflow: "auto", padding: 4, tone: "inherit", children: /* @__PURE__ */ jsxRuntimeExports.jsx(Stack, { space: 4, children: /* @__PURE__ */ jsxRuntimeExports.jsx(Text, { size: 2, children: ERROR_DESCRIPTION }) }) })
  ] }) }) }), $[2] = t2) : t2 = $[2], t2;
};
export {
  DetectViteDevServerStopped,
  DevServerStoppedErrorScreen,
  ViteDevServerStoppedError
};
