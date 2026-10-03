import { d as distExports, r as reactExports, aq as useI18nText, ar as reactIsExports, j as jsxRuntimeExports, K as Pane, l as gt, q as useStructureTool, w as Button, as as ArrowLeftIcon, N as BackLink, a8 as PaneHeader$1, at as usePane, B as Box, au as PaneHeaderActions } from "./sanity-DqWFaXvw.js";
const Root = gt(Box)`
  position: relative;
`;
function UserComponentPaneContent(props) {
  const $ = distExports.c(3), {
    children
  } = props, {
    collapsed
  } = usePane();
  let t0;
  return $[0] !== children || $[1] !== collapsed ? (t0 = /* @__PURE__ */ jsxRuntimeExports.jsx(Root, { hidden: collapsed, height: "fill", overflow: "auto", children }), $[0] = children, $[1] = collapsed, $[2] = t0) : t0 = $[2], t0;
}
function UserComponentPaneHeader(props) {
  const $ = distExports.c(11), {
    actionHandlers,
    index,
    menuItems,
    menuItemGroups,
    title
  } = props, {
    features
  } = useStructureTool();
  if (!(menuItems == null ? void 0 : menuItems.length) && !title)
    return null;
  let t0;
  $[0] !== actionHandlers || $[1] !== menuItemGroups || $[2] !== menuItems ? (t0 = /* @__PURE__ */ jsxRuntimeExports.jsx(PaneHeaderActions, { menuItems, menuItemGroups, actionHandlers }), $[0] = actionHandlers, $[1] = menuItemGroups, $[2] = menuItems, $[3] = t0) : t0 = $[3];
  let t1;
  $[4] !== features.backButton || $[5] !== index ? (t1 = features.backButton && index > 0 && /* @__PURE__ */ jsxRuntimeExports.jsx(Button, { as: BackLink, "data-as": "a", icon: ArrowLeftIcon, mode: "bleed", tooltipProps: {
    content: "Back"
  } }), $[4] = features.backButton, $[5] = index, $[6] = t1) : t1 = $[6];
  let t2;
  return $[7] !== t0 || $[8] !== t1 || $[9] !== title ? (t2 = /* @__PURE__ */ jsxRuntimeExports.jsx(PaneHeader$1, { actions: t0, backButton: t1, title }), $[7] = t0, $[8] = t1, $[9] = title, $[10] = t2) : t2 = $[10], t2;
}
function UserComponentPane(props) {
  const $ = distExports.c(37);
  let index, pane, paneKey, restProps;
  $[0] !== props ? ({
    index,
    pane,
    paneKey,
    ...restProps
  } = props, $[0] = props, $[1] = index, $[2] = pane, $[3] = paneKey, $[4] = restProps) : (index = $[1], pane = $[2], paneKey = $[3], restProps = $[4]);
  let UserComponent, child, menuItemGroups, menuItems, restPane;
  if ($[5] !== pane) {
    const {
      child: t02,
      component: t12,
      menuItems: t22,
      menuItemGroups: t32,
      type: _unused,
      ...t42
    } = pane;
    child = t02, UserComponent = t12, menuItems = t22, menuItemGroups = t32, restPane = t42, $[5] = pane, $[6] = UserComponent, $[7] = child, $[8] = menuItemGroups, $[9] = menuItems, $[10] = restPane;
  } else
    UserComponent = $[6], child = $[7], menuItemGroups = $[8], menuItems = $[9], restPane = $[10];
  const [ref, setRef] = reactExports.useState(null), {
    title: t0
  } = useI18nText(pane), title = t0 === void 0 ? "" : t0;
  let componentProps, key;
  $[11] !== restPane || $[12] !== restProps ? ({
    key,
    ...componentProps
  } = {
    ...restProps,
    ...restPane
  }, $[11] = restPane, $[12] = restProps, $[13] = componentProps, $[14] = key) : (componentProps = $[13], key = $[14]);
  const t1 = ref == null ? void 0 : ref.actionHandlers;
  let t2;
  $[15] !== index || $[16] !== menuItemGroups || $[17] !== menuItems || $[18] !== t1 || $[19] !== title ? (t2 = /* @__PURE__ */ jsxRuntimeExports.jsx(UserComponentPaneHeader, { actionHandlers: t1, index, menuItems, menuItemGroups, title }), $[15] = index, $[16] = menuItemGroups, $[17] = menuItems, $[18] = t1, $[19] = title, $[20] = t2) : t2 = $[20];
  let t3;
  $[21] !== UserComponent || $[22] !== child || $[23] !== componentProps || $[24] !== key || $[25] !== paneKey ? (t3 = reactIsExports.isValidElementType(UserComponent) && /* @__PURE__ */ jsxRuntimeExports.jsx(UserComponent, { ...componentProps, ref: setRef, child, paneKey }, key), $[21] = UserComponent, $[22] = child, $[23] = componentProps, $[24] = key, $[25] = paneKey, $[26] = t3) : t3 = $[26];
  let t4;
  $[27] !== UserComponent ? (t4 = reactExports.isValidElement(UserComponent) && UserComponent, $[27] = UserComponent, $[28] = t4) : t4 = $[28];
  let t5;
  $[29] !== t3 || $[30] !== t4 ? (t5 = /* @__PURE__ */ jsxRuntimeExports.jsxs(UserComponentPaneContent, { children: [
    t3,
    t4
  ] }), $[29] = t3, $[30] = t4, $[31] = t5) : t5 = $[31];
  let t6;
  return $[32] !== paneKey || $[33] !== restProps.isSelected || $[34] !== t2 || $[35] !== t5 ? (t6 = /* @__PURE__ */ jsxRuntimeExports.jsxs(Pane, { id: paneKey, minWidth: 320, selected: restProps.isSelected, children: [
    t2,
    t5
  ] }), $[32] = paneKey, $[33] = restProps.isSelected, $[34] = t2, $[35] = t5, $[36] = t6) : t6 = $[36], t6;
}
export {
  UserComponentPane as default
};
