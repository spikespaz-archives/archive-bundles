import arsd.nanovega;
import arsd.color;
public import themes;
public import utilities;

/// Draw a simple rectangle the color of `BACKGROUND_COLOR` on the NanoVega context.
public void drawBackground(NVGContext nvgc, PointF pos, SizeF size) {
    nvgc.beginPath();
    nvgc.fillColor = BACKGROUND_COLOR.getNVGColor();
    nvgc.rect(pos.x, pos.y, size.width, size.height);
    nvgc.fill();
}

/// Draw a check box to a NanoVega context, according to the active theme at `CHECK_BOX_THEME`.
public void drawCheckBox(NVGContext nvgc, const PointF pos, const SizeF size = const SizeF(14f, 14f), const ushort state = UNCHECKED) {
    nvgc.beginPath();

    if (checkFlag(state, ACTIVE)) {
        nvgc.fillColor = CHECK_BOX_THEME.activeFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.activeBorderColor;
    } else if (checkFlag(state, HOVERED)) {
        nvgc.fillColor = CHECK_BOX_THEME.hoveredFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.hoveredBorderColor;

    } else if (checkFlag(state, CHECKED)) {
        nvgc.fillColor = CHECK_BOX_THEME.checkedFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.checkedBorderColor;
    } else if (checkFlag(state, UNCHECKED) || checkFlag(state, ZEROFLAG)) {
        nvgc.fillColor = CHECK_BOX_THEME.uncheckedFillColor;
        nvgc.strokeColor = CHECK_BOX_THEME.uncheckedBorderColor;
    }

    nvgc.strokeWidth = CHECK_BOX_THEME.borderWidth;

    if (!CHECK_BOX_THEME.borderRadius)
        nvgc.rect(pos.x, pos.y, size.width, size.height);
    else
        nvgc.roundedRect(pos.x, pos.y, size.width, size.height, CHECK_BOX_THEME.borderRadius);

    nvgc.fill();

    if (CHECK_BOX_THEME.borderWidth)
        nvgc.stroke();
}

/// Draw a text button to the NanoVega context, according to the theme at `TEXT_BUTTON_THEME`.
public void drawButton(NVGContext nvgc, const string text, const PointF pos, const SizeF size = SizeF(50f, 26f),
        const ushort state = CENTER_HORIZONTAL) {
    nvgc.beginPath();

    if (checkFlag(state, ACTIVE)) {
        nvgc.fillColor = TEXT_BUTTON_THEME.activeFillColor;
        nvgc.strokeColor = TEXT_BUTTON_THEME.activeBorderColor;
    } else if (checkFlag(state, HOVERED)) {
        nvgc.fillColor = TEXT_BUTTON_THEME.hoveredFillColor;
        nvgc.strokeColor = TEXT_BUTTON_THEME.hoveredBorderColor;
    } else if (checkFlag(state, ZEROFLAG)) {
        nvgc.fillColor = TEXT_BUTTON_THEME.defaultFillColor;
        nvgc.strokeColor = TEXT_BUTTON_THEME.defaultBorderColor;
    }

    nvgc.strokeWidth = TEXT_BUTTON_THEME.borderWidth;

    if (!TEXT_BUTTON_THEME.borderRadius)
        nvgc.rect(pos.x, pos.y, size.width, size.height);
    else
        nvgc.roundedRect(pos.x, pos.y, size.width, size.height, TEXT_BUTTON_THEME.borderRadius);

    nvgc.fill();

    if (TEXT_BUTTON_THEME.borderWidth)
        nvgc.stroke();
}

/// Draw a text label to the NanoVega context. There is no theme for text labels.
public void drawTextLabel(NVGContext nvgc, const string text, const PointF pos, const SizeF size = SizeF(50f, 26f),
        const ushort state = CENTER_HORIZONTAL) {

}
