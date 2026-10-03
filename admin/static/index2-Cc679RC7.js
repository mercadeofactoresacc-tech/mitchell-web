import { d as distExports, aq as useI18nText, j as jsxRuntimeExports, K as Pane, l as gt, av as _DEBUG, q as useStructureTool, at as usePane, w as Button, as as ArrowLeftIcon, N as BackLink, a8 as PaneHeader$1, M as usePaneLayout, aw as useGetI18nText, ax as CommandList, a9 as PaneContent, B as Box, T as Text, ay as PaneItem, au as PaneHeaderActions } from "./sanity-D_nH2OOZ.js";
const DividerContainer = gt(Box)`
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0.75rem 0 0.25rem 0;
`, Divider = gt.hr`
  flex: 1;
  background-color: var(--card-border-color);
  height: 1px;
  margin: 0;
  border: none;
`, DividerTitle = gt(Text)`
  padding-bottom: 0.75rem;
  padding-left: 0.5rem;
  padding-right: 0.5rem;
`;
function DividerItem(t0) {
  const $ = distExports.c(5), {
    item
  } = t0, {
    title: dividerTitle
  } = useI18nText(item);
  let t1;
  $[0] !== dividerTitle ? (t1 = /* @__PURE__ */ jsxRuntimeExports.jsx(DividerTitle, { weight: "semibold", muted: true, size: 1, children: dividerTitle }), $[0] = dividerTitle, $[1] = t1) : t1 = $[1];
  let t2;
  $[2] === Symbol.for("react.memo_cache_sentinel") ? (t2 = /* @__PURE__ */ jsxRuntimeExports.jsx(Divider, {}), $[2] = t2) : t2 = $[2];
  let t3;
  return $[3] !== t1 ? (t3 = /* @__PURE__ */ jsxRuntimeExports.jsxs(DividerContainer, { children: [
    t1,
    t2
  ] }), $[3] = t1, $[4] = t3) : t3 = $[4], t3;
}
function ListPaneContent(props) {
  const $ = distExports.c(20), {
    childItemId,
    items,
    isActive,
    layout,
    showIcons,
    title
  } = props, {
    collapsed: layoutCollapsed
  } = usePaneLayout();
  let t0;
  $[0] !== items ? (t0 = items == null ? void 0 : items.filter(_temp), $[0] = items, $[1] = t0) : t0 = $[1];
  const getI18nText = useGetI18nText(t0);
  let t1;
  $[2] !== items ? (t1 = (itemIndex) => {
    var _a;
    return ((_a = items == null ? void 0 : items.find((_, i) => i === itemIndex)) == null ? void 0 : _a.type) === "divider";
  }, $[2] = items, $[3] = t1) : t1 = $[3];
  const getItemDisabled = t1;
  let t2;
  $[4] !== showIcons ? (t2 = (item_0) => {
    var _a;
    const itemShowIcon = (_a = item_0.displayOptions) == null ? void 0 : _a.showIcon;
    return typeof itemShowIcon < "u" ? itemShowIcon !== false : showIcons !== false;
  }, $[4] = showIcons, $[5] = t2) : t2 = $[5];
  const shouldShowIconForItem = t2;
  let t3;
  $[6] !== childItemId || $[7] !== getI18nText || $[8] !== isActive || $[9] !== layout || $[10] !== shouldShowIconForItem ? (t3 = (item_1, ctx) => {
    const {
      virtualIndex: itemIndex_0
    } = ctx;
    if (item_1.type === "divider")
      return /* @__PURE__ */ jsxRuntimeExports.jsx(Box, { marginBottom: 1, children: item_1.title ? /* @__PURE__ */ jsxRuntimeExports.jsx(DividerItem, { item: item_1 }) : /* @__PURE__ */ jsxRuntimeExports.jsx(Divider, {}) }, `divider-${itemIndex_0}`);
    const pressed = !isActive && childItemId === item_1.id, selected = isActive && childItemId === item_1.id, value = item_1._id && item_1.schemaType ? {
      _id: item_1._id,
      _type: item_1.schemaType.name,
      title: item_1.title
    } : void 0;
    return /* @__PURE__ */ jsxRuntimeExports.jsx(PaneItem, { icon: shouldShowIconForItem(item_1) ? item_1.icon : false, id: item_1.id, layout, marginBottom: 1, pressed, schemaType: item_1.schemaType, selected, title: getI18nText(item_1).title, value }, item_1.id);
  }, $[6] = childItemId, $[7] = getI18nText, $[8] = isActive, $[9] = layout, $[10] = shouldShowIconForItem, $[11] = t3) : t3 = $[11];
  const renderItem = t3, t4 = layoutCollapsed ? "hidden" : "auto";
  let t5;
  $[12] !== getItemDisabled || $[13] !== items || $[14] !== renderItem || $[15] !== title ? (t5 = items && items.length > 0 && /* @__PURE__ */ jsxRuntimeExports.jsx(CommandList, { activeItemDataAttr: "data-hovered", ariaLabel: title, canReceiveFocus: true, getItemDisabled, itemHeight: 51, items, onlyShowSelectionWhenActive: true, paddingBottom: 1, paddingX: 3, renderItem, wrapAround: false }), $[12] = getItemDisabled, $[13] = items, $[14] = renderItem, $[15] = title, $[16] = t5) : t5 = $[16];
  let t6;
  return $[17] !== t4 || $[18] !== t5 ? (t6 = /* @__PURE__ */ jsxRuntimeExports.jsx(PaneContent, { overflow: t4, children: t5 }), $[17] = t4, $[18] = t5, $[19] = t6) : t6 = $[19], t6;
}
function _temp(item) {
  return item.type !== "divider";
}
const ListPaneHeader = (t0) => {
  const $ = distExports.c(11), {
    index,
    menuItems,
    menuItemGroups,
    title
  } = t0, {
    features
  } = useStructureTool(), {
    collapsed,
    isLast
  } = usePane(), tabIndex = isLast && !collapsed ? -1 : 0;
  let t1;
  $[0] !== menuItemGroups || $[1] !== menuItems ? (t1 = /* @__PURE__ */ jsxRuntimeExports.jsx(PaneHeaderActions, { menuItems, menuItemGroups }), $[0] = menuItemGroups, $[1] = menuItems, $[2] = t1) : t1 = $[2];
  let t2;
  $[3] !== features.backButton || $[4] !== index ? (t2 = features.backButton && index > 0 && /* @__PURE__ */ jsxRuntimeExports.jsx(Button, { as: BackLink, "data-as": "a", icon: ArrowLeftIcon, mode: "bleed", tooltipProps: {
    content: "Back"
  } }), $[3] = features.backButton, $[4] = index, $[5] = t2) : t2 = $[5];
  let t3;
  return $[6] !== t1 || $[7] !== t2 || $[8] !== tabIndex || $[9] !== title ? (t3 = /* @__PURE__ */ jsxRuntimeExports.jsx(PaneHeader$1, { actions: t1, backButton: t2, tabIndex, title }), $[6] = t1, $[7] = t2, $[8] = tabIndex, $[9] = title, $[10] = t3) : t3 = $[10], t3;
};
function ListPane(props) {
  const $ = distExports.c(21), {
    childItemId,
    index,
    isActive,
    isSelected,
    pane,
    paneKey
  } = props, {
    defaultLayout,
    displayOptions,
    items,
    menuItems,
    menuItemGroups
  } = pane, showIcons = (displayOptions == null ? void 0 : displayOptions.showIcons) !== false, {
    title
  } = useI18nText(pane);
  let t0;
  $[0] !== pane.source ? (t0 = _DEBUG, $[0] = pane.source, $[1] = t0) : t0 = $[1];
  let t1;
  $[2] !== index || $[3] !== menuItemGroups || $[4] !== menuItems || $[5] !== title ? (t1 = /* @__PURE__ */ jsxRuntimeExports.jsx(ListPaneHeader, { index, menuItems, menuItemGroups, title }), $[2] = index, $[3] = menuItemGroups, $[4] = menuItems, $[5] = title, $[6] = t1) : t1 = $[6];
  let t2;
  $[7] !== childItemId || $[8] !== defaultLayout || $[9] !== isActive || $[10] !== items || $[11] !== paneKey || $[12] !== showIcons || $[13] !== title ? (t2 = /* @__PURE__ */ jsxRuntimeExports.jsx(ListPaneContent, { childItemId, isActive, items, layout: defaultLayout, showIcons, title }, paneKey), $[7] = childItemId, $[8] = defaultLayout, $[9] = isActive, $[10] = items, $[11] = paneKey, $[12] = showIcons, $[13] = title, $[14] = t2) : t2 = $[14];
  let t3;
  return $[15] !== isSelected || $[16] !== paneKey || $[17] !== t0 || $[18] !== t1 || $[19] !== t2 ? (t3 = /* @__PURE__ */ jsxRuntimeExports.jsxs(Pane, { currentMaxWidth: 350, "data-testid": "structure-tool-list-pane", "data-ui": "ListPane", id: paneKey, maxWidth: 640, minWidth: 320, selected: isSelected, children: [
    t0,
    t1,
    t2
  ] }), $[15] = isSelected, $[16] = paneKey, $[17] = t0, $[18] = t1, $[19] = t2, $[20] = t3) : t3 = $[20], t3;
}
export {
  ListPane as default
};
